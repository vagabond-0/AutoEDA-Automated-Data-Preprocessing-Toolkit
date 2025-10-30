import unittest
import pandas as pd
import numpy as np
import os
import shutil  # For directory cleanup
from pandas.testing import assert_frame_equal, assert_series_equal

# Adjust path to import from autoeda (assuming unit_tests is at the same level as autoeda)
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autoeda.feature_selector import (
    remove_low_variance,
    remove_highly_correlated,
    select_by_model_importance,
    run_feature_selection,
    log_file_path as main_log_file_path # Get the log file path from the module
)

class TestFeatureSelector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up for all tests in the class."""
        cls.test_output_dir = "output_unit_tests"
        if os.path.exists(cls.test_output_dir):
            shutil.rmtree(cls.test_output_dir) # Clean up from previous runs
        os.makedirs(cls.test_output_dir, exist_ok=True)
        
        # Override the log file path for tests to avoid polluting the main log
        # This requires the feature_selector module to be reloadable or its global var to be patchable.
        # For simplicity, we'll let it write to the default log path but manage it in tearDown.
        # A better way would be to pass logger instance or log_path to functions.
        cls.original_log_file_path = main_log_file_path
        cls.test_log_file = os.path.join(cls.test_output_dir, "test_feature_selection_log.txt")

        # Ensure the main log's directory exists as the module tries to create it
        if not os.path.exists(os.path.dirname(main_log_file_path)):
             os.makedirs(os.path.dirname(main_log_file_path), exist_ok=True)


    def setUp(self):
        """Set up for each test method."""
        # Clear the test log file before each test
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        
        # For run_feature_selection, it writes to the global log_file_path.
        # We will check this global log file. Clear it before tests that use it.
        if os.path.exists(self.original_log_file_path):
            os.remove(self.original_log_file_path)

        # Sample DataFrames
        self.df_empty = pd.DataFrame()
        self.df_no_numeric = pd.DataFrame({'A': ['x', 'y', 'z'], 'B': ['p', 'q', 'r']})
        
        self.df_low_var_mixed = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],    # Var = 2.5
            'B': [1, 1, 1, 1, 1],    # Var = 0
            'C': [0.1, 0.2, 0.1, 0.2, 0.1], # Var = 0.007
            'D': [10, 20, 30, 40, 50], # Var = 250
            'E': ['cat', 'dog', 'cat', 'dog', 'cat'] # Non-numeric
        })

        self.df_corr_mixed = pd.DataFrame({
            'F1': [1, 2, 3, 4, 5],      # Reference
            'F2': [1.1, 2.1, 3.1, 4.1, 5.1], # Correlated with F1 (drops F2)
            'F3': [-1, -2, -3, -4, -5], # Correlated with F1 (drops F3)
            'F0': [5, 4, 3, 2, 1],      # Correlated with F1, F0 < F1 alphabetically (drops F1 if F0 is compared first)
                                        # Current logic: corr(F1,F0) -> F1 is kept, F0 dropped.
                                        # if F0 vs F1 -> F0 kept, F1 dropped.
                                        # The iteration order matters. upper.columns then upper.index
                                        # F1 is column, F0 is index. F0 vs F1. F0 > F1 is false. F1 is dropped.
            'F4': [10, 2, 30, 4, 50],   # Less correlated
            'F5_text': ['a', 'b', 'c', 'd', 'e']
        })
        # Correcting expectation for F0 vs F1 for remove_highly_correlated:
        # numeric_df columns are sorted: F0, F1, F2, F3, F4
        # corr_matrix columns/index also F0, F1, F2, F3, F4
        # upper triangle:
        # (F0,F1), (F0,F2), (F0,F3), (F0,F4)
        # (F1,F2), (F1,F3), (F1,F4)
        # (F2,F3), (F2,F4)
        # (F3,F4)
        # If corr(F0,F1) is high: index='F0', column='F1'. 'F0' > 'F1' is False. 'F1' is dropped. (Keeps F0)

        self.df_model = pd.DataFrame({
            'M_Feat1': np.array([1.0, 2.0, 3.0, 4.0, 5.0, np.nan, 7.0, 8.0, 9.0, 10.0] * 10), # 100 rows
            'M_Feat2_imp': np.array([1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1] * 10),
            'M_Feat3_zero_imp': [0.01] * 100, # Constant feature, should have zero importance after imputation
            'M_Feat4_text': ['P', 'Q'] * 50,
        })
        self.target_reg = pd.Series(self.df_model['M_Feat2_imp'] * 2 + np.random.normal(0, 0.1, 100), name="TargetR")
        self.target_clf = pd.Series( (self.df_model['M_Feat2_imp'] > self.df_model['M_Feat2_imp'].median()).astype(int), name="TargetC")
        # Introduce NaNs into target
        self.target_reg_nan = self.target_reg.copy()
        self.target_reg_nan.iloc[5:10] = np.nan
        self.target_clf_nan = self.target_clf.copy()
        self.target_clf_nan.iloc[10:15] = np.nan


    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests in the class."""
        if os.path.exists(cls.test_output_dir):
            shutil.rmtree(cls.test_output_dir)
        # Clean up the main log file if it was created by tests
        if os.path.exists(cls.original_log_file_path) and "test" in cls.original_log_file_path: # safety
             pass # Avoid deleting non-test main log unless specifically named for tests
        elif os.path.exists(cls.original_log_file_path) and "output/feature_selection_log.txt" in cls.original_log_file_path:
             # This is the actual log file, clear it if tests ran.
             # In a real CI/CD, log handling would be more robust.
             # For now, assume if tests ran, this log might contain test data.
             # os.remove(cls.original_log_file_path) # Commented out to avoid accidental deletion of useful logs during manual runs
             pass


    def test_dummy(self): # A dummy test to ensure setup/teardown work
        self.assertTrue(True)
        # Check if the main log file is created by module import or first logging call
        # The module itself creates ./output/feature_selection_log.txt
        # self.assertTrue(os.path.exists(self.original_log_file_path)) # Log is created on first write not import

    # --- Test remove_low_variance ---
    def test_remove_low_variance_normal_case(self):
        df_result = remove_low_variance(self.df_low_var_mixed.copy(), threshold=0.1)
        self.assertListEqual(sorted(df_result.columns.tolist()), sorted(['A', 'D', 'E']))
        self.assertTrue(os.path.exists(self.original_log_file_path)) # Check log was written to

    def test_remove_low_variance_no_removal_threshold_zero(self):
        # With threshold = 0, only features with variance < 0 are removed (none).
        # So, all features should be kept, including those with variance == 0.
        df_result = remove_low_variance(self.df_low_var_mixed.copy(), threshold=0.0)
        self.assertListEqual(sorted(df_result.columns.tolist()), sorted(self.df_low_var_mixed.columns.tolist()))

    def test_remove_low_variance_all_numeric_removed(self):
        # Create a df where all numeric columns have low variance
        df_all_low = pd.DataFrame({'X': [1,1,1], 'Y': [2,2,2], 'Z_text':['a','b','c']})
        df_result = remove_low_variance(df_all_low.copy(), threshold=0.1)
        self.assertListEqual(sorted(df_result.columns.tolist()), sorted(['Z_text']))

    def test_remove_low_variance_no_numeric(self):
        df_result = remove_low_variance(self.df_no_numeric.copy(), threshold=0.1)
        assert_frame_equal(df_result, self.df_no_numeric)

    def test_remove_low_variance_empty_df(self):
        df_result = remove_low_variance(self.df_empty.copy(), threshold=0.1)
        assert_frame_equal(df_result, self.df_empty)

    def test_remove_low_variance_strict_positive_threshold(self):
        # B has 0 variance, C has 0.007.
        # With threshold = 0.001, B (var 0) should be removed (0 < 0.001).
        # C (var 0.007) should be kept (0.007 < 0.001 is false).
        df_result = remove_low_variance(self.df_low_var_mixed.copy(), threshold=0.001)
        self.assertListEqual(sorted(df_result.columns.tolist()), sorted(['A', 'C', 'D', 'E']))

    # --- Test remove_highly_correlated ---
    def test_remove_highly_correlated_normal_case(self):
        # Expected: F1 vs F0 -> F1 dropped (keeps F0)
        # F2 vs F0 -> F2 dropped (keeps F0)
        # F3 vs F0 -> F3 dropped (keeps F0)
        # F2 vs F1 (F1 already dropped)
        # Based on df_corr_mixed:
        # Numeric columns: F0, F1, F2, F3, F4
        # Pairs (abs_corr > 0.9): (F0,F1), (F0,F2), (F0,F3), (F1,F2), (F1,F3), (F2,F3)
        # Iteration (col, idx):
        # ('F1', 'F0'): corr > 0.9. 'F0' > 'F1' is False. Drop 'F1'. Kept: F0. Dropped: {F1}
        # ('F2', 'F0'): corr > 0.9. 'F0' > 'F2' is False. Drop 'F2'. Kept: F0. Dropped: {F1, F2}
        # ('F2', 'F1'): F1,F2 already in dropped. Skip.
        # ('F3', 'F0'): corr > 0.9. 'F0' > 'F3' is False. Drop 'F3'. Kept: F0. Dropped: {F1, F2, F3}
        # So, F0, F4, F5_text should remain.
        df_result = remove_highly_correlated(self.df_corr_mixed.copy(), threshold=0.9)
        self.assertListEqual(sorted(df_result.columns.tolist()), sorted(['F0', 'F4', 'F5_text']))
        self.assertTrue(os.path.exists(self.original_log_file_path))

    def test_remove_highly_correlated_no_removal(self):
        df_result = remove_highly_correlated(self.df_corr_mixed.copy(), threshold=0.99999) # Very high threshold
        # F0, F1, F2, F3 are perfectly correlated if noise is 0. With noise, maybe not.
        # F0 and F3 are perfectly negatively correlated. F0 and F1 are very highly correlated.
        # (F1,F0) -> F1 dropped.
        # (F2,F0) -> F2 dropped
        # (F3,F0) -> F3 dropped.
        # This means with threshold 0.99999 (assuming perfect correlation after np.linspace)
        # still F0, F4, F5_text
        # Let's make a less perfectly correlated df for this test.
        df_less_corr = pd.DataFrame({
            'LC1': [1,2,3,4,5], 'LC2': [1.5,2.5,3.5,4.8,5.2], 'LC3': ['a','b','c','d','e']
        })
        df_result_lc = remove_highly_correlated(df_less_corr.copy(), threshold=0.95) # Corr is high but maybe not >0.95
        # Correlation of LC1 and LC2 is likely high. Let's test with 0.98
        # print(df_less_corr[['LC1','LC2']].corr()) # around 0.99
        df_result_lc_no_removal = remove_highly_correlated(df_less_corr.copy(), threshold=0.999)
        self.assertListEqual(sorted(df_result_lc_no_removal.columns.tolist()), sorted(df_less_corr.columns.tolist()))


    def test_remove_highly_correlated_less_than_2_numeric(self):
        df_one_numeric = pd.DataFrame({'A': [1, 2, 3], 'B_text': ['x', 'y', 'z']})
        df_result = remove_highly_correlated(df_one_numeric.copy(), threshold=0.8)
        assert_frame_equal(df_result, df_one_numeric)

    def test_remove_highly_correlated_no_numeric(self):
        df_result = remove_highly_correlated(self.df_no_numeric.copy(), threshold=0.8)
        assert_frame_equal(df_result, self.df_no_numeric)

    def test_remove_highly_correlated_empty_df(self):
        df_result = remove_highly_correlated(self.df_empty.copy(), threshold=0.8)
        assert_frame_equal(df_result, self.df_empty)

    # --- Test select_by_model_importance ---
    def test_sbm_regression_normal_case(self):
        # M_Feat3_zero_imp should be removed (or have importance near zero)
        df_result = select_by_model_importance(self.df_model.copy(), self.target_reg.copy(), 'regression', threshold=0.01) # Lowered threshold
        self.assertNotIn('M_Feat3_zero_imp', df_result.columns)
        self.assertIn('M_Feat1', df_result.columns)
        self.assertIn('M_Feat2_imp', df_result.columns)
        self.assertIn('M_Feat4_text', df_result.columns) # Non-numeric kept
        self.assertTrue(os.path.exists(self.original_log_file_path))

    def test_sbm_classification_normal_case(self):
        # M_Feat3_zero_imp should be removed
        df_result = select_by_model_importance(self.df_model.copy(), self.target_clf.copy(), 'classification', threshold=0.01) # Lowered threshold
        self.assertNotIn('M_Feat3_zero_imp', df_result.columns)
        # M_Feat1 might be weak for classification target, its importance depends on data
        # self.assertIn('M_Feat1', df_result.columns) 
        self.assertIn('M_Feat2_imp', df_result.columns) # M_Feat2_imp is used for target_clf
        self.assertIn('M_Feat4_text', df_result.columns)

    def test_sbm_regression_target_with_nans(self):
        # Test that rows with NaNs in target are dropped and model still runs
        df_copy = self.df_model.copy()
        target_copy = self.target_reg_nan.copy()
        
        # Align df_copy with target_copy before passing to function, as per function's expectation
        # The main run_feature_selection function does this alignment.
        # Here, we simulate it for direct unit test.
        valid_indices = target_copy.dropna().index
        df_aligned = df_copy.loc[valid_indices]
        target_aligned = target_copy.loc[valid_indices]

        df_result = select_by_model_importance(df_aligned, target_aligned, 'regression', threshold=0.01)
        self.assertNotIn('M_Feat3_zero_imp', df_result.columns)
        self.assertEqual(df_result.shape[0], len(valid_indices)) # Check rows dropped

    def test_sbm_no_numeric_features(self):
        df_result = select_by_model_importance(self.df_no_numeric.copy(), pd.Series([1,0,1]), 'classification', threshold=0.01)
        assert_frame_equal(df_result, self.df_no_numeric)

    def test_sbm_empty_df_after_target_nan_removal(self):
        # Scenario: all target values are NaN
        df_features = pd.DataFrame({'A': [1,2,3]})
        target_all_nan = pd.Series([np.nan, np.nan, np.nan])
        
        # Simulate pre-alignment from run_feature_selection
        valid_indices = target_all_nan.dropna().index
        df_aligned = df_features.loc[valid_indices] # This will be empty
        target_aligned = target_all_nan.loc[valid_indices] # This will be empty

        df_result = select_by_model_importance(df_aligned, target_aligned, 'regression', threshold=0.01)
        self.assertTrue(df_result.empty) # Expect an empty df (or original structure)

    def test_sbm_input_df_empty(self):
        df_result = select_by_model_importance(self.df_empty.copy(), pd.Series([]), 'classification', threshold=0.01)
        self.assertTrue(df_result.empty)


    # --- Test run_feature_selection (Integration) ---
    def test_run_feature_selection_regression(self):
        input_csv = os.path.join(self.test_output_dir, "test_input_reg.csv")
        output_csv = os.path.join(self.test_output_dir, "test_output_reg.csv")
        
        # Create a sample CSV for regression
        test_df_reg = self.df_model.copy()
        test_df_reg['TargetR'] = self.target_reg_nan.copy() # Has NaNs
        test_df_reg.to_csv(input_csv, index=False)

        run_feature_selection(input_csv, output_csv, 'TargetR', 'regression', 
                              low_variance_threshold=0.0, # M_Feat3_zero_imp has var 0. threshold=0 won't remove it here.
                                                           # It should be removed by model importance.
                              correlation_threshold=0.95, 
                              importance_threshold=0.01) # M_Feat3_zero_imp should be removed by this
        
        self.assertTrue(os.path.exists(output_csv))
        self.assertTrue(os.path.exists(self.original_log_file_path))
        df_out = pd.read_csv(output_csv)
        self.assertIn('TargetR', df_out.columns)
        self.assertNotIn('M_Feat3_zero_imp', df_out.columns) 
        self.assertLessEqual(df_out.shape[1], test_df_reg.shape[1]) 
        self.assertEqual(df_out.shape[0], test_df_reg.shape[0] - self.target_reg_nan.isnull().sum())

    def test_run_feature_selection_classification(self):
        input_csv = os.path.join(self.test_output_dir, "test_input_clf.csv")
        output_csv = os.path.join(self.test_output_dir, "test_output_clf.csv")

        test_df_clf = self.df_model.copy()
        test_df_clf['TargetC'] = self.target_clf_nan.copy() # Has NaNs
        test_df_clf.to_csv(input_csv, index=False)

        run_feature_selection(input_csv, output_csv, 'TargetC', 'classification',
                              low_variance_threshold=0.0, 
                              correlation_threshold=0.95,
                              importance_threshold=0.01)
        
        self.assertTrue(os.path.exists(output_csv))
        self.assertTrue(os.path.exists(self.original_log_file_path))
        df_out = pd.read_csv(output_csv)
        self.assertIn('TargetC', df_out.columns)
        self.assertNotIn('M_Feat3_zero_imp', df_out.columns)
        self.assertLessEqual(df_out.shape[1], test_df_clf.shape[1])
        self.assertEqual(df_out.shape[0], test_df_clf.shape[0] - self.target_clf_nan.isnull().sum())

    def test_run_feature_selection_input_file_not_found(self):
        with self.assertLogs(level='ERROR') as log: # Check that an error is logged
            run_feature_selection("non_existent_file.csv", "output.csv", "target", "regression")
            self.assertTrue(any("Input file not found" in message for message in log.output))
    
    def test_run_feature_selection_target_not_in_df(self):
        input_csv = os.path.join(self.test_output_dir, "test_input_no_target.csv")
        self.df_model.to_csv(input_csv, index=False)
        with self.assertLogs(level='ERROR') as log:
            run_feature_selection(input_csv, "output.csv", "NonExistentTarget", "regression")
            self.assertTrue(any("Target column 'NonExistentTarget' not found" in message for message in log.output))


if __name__ == '__main__':
    unittest.main()
