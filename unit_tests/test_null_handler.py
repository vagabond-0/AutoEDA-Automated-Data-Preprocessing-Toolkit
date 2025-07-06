import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
import numpy as np
import tempfile
from pandas import testing as tm
from autoeda import null_handler
# Assuming autoeda is in PYTHONPATH or installed
# If autoeda is a local directory and not installed, Python might not find it
# without adjusting sys.path. For now, let's assume it's discoverable.

# Specifically import all functions to be tested
from autoeda.null_handler import (
    drop_nulls,
    replace_with_fixed,
    replace_with_mean,
    replace_with_median,
    replace_with_mode,
    forward_fill,
    backward_fill,
    evaluate_methods,
    process_csv
)

# region Fixtures
@pytest.fixture
def empty_df():
    """DataFrame that is completely empty."""
    return pd.DataFrame()

@pytest.fixture
def no_nulls_df():
    """DataFrame with no null values."""
    data = {'col_a': [1, 2, 3], 'col_b': ['x', 'y', 'z'], 'col_c': [4.0, 5.1, 6.2]}
    return pd.DataFrame(data)

@pytest.fixture
def numeric_nulls_df():
    """DataFrame with nulls only in numeric columns."""
    data = {'num_col1': [1.0, np.nan, 3.0, np.nan],
            'num_col2': [np.nan, 2.2, 3.3, 4.4],
            'cat_col1': ['a', 'b', 'c', 'd']}
    return pd.DataFrame(data)

@pytest.fixture
def categorical_nulls_df():
    """DataFrame with nulls only in categorical columns."""
    data = {'num_col1': [1.0, 2.0, 3.0, 4.0],
            'cat_col1': ['a', np.nan, 'c', np.nan],
            'cat_col2': [np.nan, 'x', 'y', 'z']}
    return pd.DataFrame(data)

@pytest.fixture
def all_null_column_df():
    """DataFrame with at least one column containing all nulls."""
    data = {'num_col_all_null': [np.nan, np.nan, np.nan],
            'cat_col_all_null': [np.nan, np.nan, np.nan],
            'mixed_col': [1, np.nan, 'a']}
    return pd.DataFrame(data)

@pytest.fixture
def mixed_nulls_df():
    """DataFrame with a mix of numeric and categorical columns, and nulls in various places."""
    data = {'A_num': [1.0, np.nan, 3.0, 4.0, 5.0],
            'B_cat': ['apple', 'banana', np.nan, 'cherry', 'banana'],
            'C_num_with_nan': [10.0, 20.0, np.nan, np.nan, 50.0],
            'D_cat_with_nan': [None, 'dog', 'cat', None, 'dog'],
            'E_all_nan_numeric': [np.nan, np.nan, np.nan, np.nan, np.nan],
            'F_all_nan_cat': [np.nan, np.nan, np.nan, np.nan, np.nan]}
    return pd.DataFrame(data)

@pytest.fixture
def all_nan_object_col_df():
    """DataFrame with a single column of object dtype that is all NaN."""
    return pd.DataFrame({'obj_all_nan': pd.Series([np.nan, np.nan, np.nan], dtype=object)})

# endregion Fixtures

# region Tests for drop_nulls
def test_drop_nulls_with_numeric_nulls(numeric_nulls_df):
    """Test drop_nulls with nulls in numeric columns."""
    original_shape = numeric_nulls_df.shape
    cleaned_df = drop_nulls(numeric_nulls_df.copy())
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape[0] < original_shape[0] # Rows should be dropped
    assert cleaned_df.shape[1] == original_shape[1] # Columns should remain the same

def test_drop_nulls_with_categorical_nulls(categorical_nulls_df):
    """Test drop_nulls with nulls in categorical columns."""
    original_shape = categorical_nulls_df.shape
    cleaned_df = drop_nulls(categorical_nulls_df.copy())
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape[0] < original_shape[0]
    assert cleaned_df.shape[1] == original_shape[1]

def test_drop_nulls_with_all_null_column(all_null_column_df):
    """Test drop_nulls with a column that is entirely null.
    Pandas dropna by default drops rows if ANY value in the row is NaN.
    If a column is all NaN, and other columns have data, rows might not be dropped
    unless all columns for a row are NaN, or if how='all' is used.
    The current implementation of drop_nulls uses default dropna(),
    so it drops rows with any NA.
    """
    # This df has:
    # 'num_col_all_null': [np.nan, np.nan, np.nan],
    # 'cat_col_all_null': [np.nan, np.nan, np.nan],
    # 'mixed_col': [1, np.nan, 'a']
    # Expected: row 1 (1, nan, nan) -> nan in mixed_col, nan in all_null cols -> dropped
    # row 2 (nan, nan, nan) -> all nan -> dropped.
    # So the resulting df should be empty.
    cleaned_df = drop_nulls(all_null_column_df.copy())
    assert cleaned_df.empty # All rows should be dropped

def test_drop_nulls_with_mixed_nulls(mixed_nulls_df):
    """Test drop_nulls with a mix of nulls."""
    original_shape = mixed_nulls_df.shape
    cleaned_df = drop_nulls(mixed_nulls_df.copy())
    assert cleaned_df.isnull().sum().sum() == 0
    # In mixed_nulls_df, every row has at least one NaN, so all rows should be dropped.
    assert cleaned_df.empty
    assert cleaned_df.shape[0] < original_shape[0]

def test_drop_nulls_on_empty_df(empty_df):
    """Test drop_nulls on an already empty DataFrame."""
    cleaned_df = drop_nulls(empty_df.copy())
    assert cleaned_df.empty
    assert cleaned_df.shape == (0,0)

def test_drop_nulls_on_no_nulls_df(no_nulls_df):
    """Test drop_nulls on a DataFrame with no nulls."""
    original_df_copy = no_nulls_df.copy()
    cleaned_df = drop_nulls(original_df_copy)
    tm.assert_frame_equal(cleaned_df, no_nulls_df)
    assert cleaned_df.shape == no_nulls_df.shape

# endregion Tests for drop_nulls

# region Tests for replace_with_fixed
def test_replace_with_fixed_numeric_default(numeric_nulls_df):
    """Test replace_with_fixed on numeric nulls with default value (0)."""
    df_copy = numeric_nulls_df.copy()
    cleaned_df = replace_with_fixed(df_copy) # Default value is 0
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == numeric_nulls_df.shape
    # Check if NaNs in numeric columns were replaced by 0
    assert (cleaned_df['num_col1'][[1, 3]] == 0).all()
    assert (cleaned_df['num_col2'][[0]] == 0).all()
    # Check non-null values remained
    assert cleaned_df['num_col1'][0] == numeric_nulls_df['num_col1'][0]
    assert cleaned_df['cat_col1'].equals(numeric_nulls_df['cat_col1'])

def test_replace_with_fixed_numeric_custom_value(numeric_nulls_df):
    """Test replace_with_fixed on numeric nulls with a custom value."""
    df_copy = numeric_nulls_df.copy()
    custom_val = -99
    cleaned_df = replace_with_fixed(df_copy, value=custom_val)
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == numeric_nulls_df.shape
    assert (cleaned_df['num_col1'][[1, 3]] == custom_val).all()
    assert (cleaned_df['num_col2'][[0]] == custom_val).all()

def test_replace_with_fixed_categorical_default(categorical_nulls_df):
    """Test replace_with_fixed on categorical nulls with default value (0)."""
    # This will convert categorical columns with NaNs to mixed type if 0 is used,
    # or object type. Pandas handles this by making the column dtype object.
    df_copy = categorical_nulls_df.copy()
    cleaned_df = replace_with_fixed(df_copy, value=0) # Default value
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == categorical_nulls_df.shape
    assert (cleaned_df['cat_col1'][[1, 3]] == 0).all()
    assert (cleaned_df['cat_col2'][[0]] == 0).all()
    assert cleaned_df['num_col1'].equals(categorical_nulls_df['num_col1'])

def test_replace_with_fixed_categorical_custom_string(categorical_nulls_df):
    """Test replace_with_fixed on categorical nulls with a custom string value."""
    df_copy = categorical_nulls_df.copy()
    custom_val = 'Unknown'
    cleaned_df = replace_with_fixed(df_copy, value=custom_val)
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == categorical_nulls_df.shape
    assert (cleaned_df['cat_col1'][[1, 3]] == custom_val).all()
    assert (cleaned_df['cat_col2'][[0]] == custom_val).all()

def test_replace_with_fixed_mixed_nulls(mixed_nulls_df):
    """Test replace_with_fixed on mixed nulls with a specific value."""
    df_copy = mixed_nulls_df.copy()
    custom_val = -1
    cleaned_df = replace_with_fixed(df_copy, value=custom_val)
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == mixed_nulls_df.shape
    # Check a few specific replacements
    assert cleaned_df.loc[1, 'A_num'] == custom_val
    assert cleaned_df.loc[2, 'B_cat'] == custom_val # This will change dtype of B_cat
    assert cleaned_df.loc[2, 'C_num_with_nan'] == custom_val
    assert cleaned_df.loc[0, 'D_cat_with_nan'] == custom_val
    assert (cleaned_df['E_all_nan_numeric'] == custom_val).all()
    assert (cleaned_df['F_all_nan_cat'] == custom_val).all()

def test_replace_with_fixed_empty_df(empty_df):
    """Test replace_with_fixed on an empty DataFrame."""
    cleaned_df = replace_with_fixed(empty_df.copy(), value=123)
    assert cleaned_df.empty
    tm.assert_frame_equal(cleaned_df, empty_df)

def test_replace_with_fixed_no_nulls_df(no_nulls_df):
    """Test replace_with_fixed on a DataFrame with no nulls."""
    df_copy = no_nulls_df.copy()
    cleaned_df = replace_with_fixed(df_copy, value=123)
    tm.assert_frame_equal(cleaned_df, no_nulls_df)
    assert cleaned_df.shape == no_nulls_df.shape

# endregion Tests for replace_with_fixed

# region Tests for replace_with_mean
def test_replace_with_mean_numeric_nulls(numeric_nulls_df):
    """Test replace_with_mean on a DataFrame with only numeric nulls."""
    df_copy = numeric_nulls_df.copy()
    cleaned_df = replace_with_mean(df_copy)

    assert cleaned_df.isnull().sum().sum() == 0 # All nulls should be filled
    assert cleaned_df.shape == numeric_nulls_df.shape # Shape should be preserved

    # Calculate expected means for columns with NaNs
    mean_num_col1 = numeric_nulls_df['num_col1'].mean()
    mean_num_col2 = numeric_nulls_df['num_col2'].mean()

    # Check that NaNs were replaced with the mean
    # Original: num_col1: [1.0, np.nan, 3.0, np.nan] -> mean is (1+3)/2 = 2.0
    # Original: num_col2: [np.nan, 2.2, 3.3, 4.4] -> mean is (2.2+3.3+4.4)/3 = 9.9/3 = 3.3
    assert cleaned_df.loc[1, 'num_col1'] == pytest.approx(mean_num_col1)
    assert cleaned_df.loc[3, 'num_col1'] == pytest.approx(mean_num_col1)
    assert cleaned_df.loc[0, 'num_col2'] == pytest.approx(mean_num_col2)

    # Check that non-NaN values and other columns are unchanged
    assert cleaned_df.loc[0, 'num_col1'] == numeric_nulls_df.loc[0, 'num_col1']
    assert cleaned_df['cat_col1'].equals(numeric_nulls_df['cat_col1'])


def test_replace_with_mean_mixed_nulls(mixed_nulls_df):
    """Test replace_with_mean on a mixed-type DataFrame with various nulls."""
    df_copy = mixed_nulls_df.copy()
    cleaned_df = replace_with_mean(df_copy)
    assert cleaned_df.shape == mixed_nulls_df.shape

    # Numeric columns that had NaNs should now be filled
    assert cleaned_df['A_num'].isnull().sum() == 0
    assert cleaned_df['C_num_with_nan'].isnull().sum() == 0
    
    # E_all_nan_numeric will be all NaNs after mean(), as mean of all NaNs is NaN.
    # The function fillna(mean) will thus not change it.
    assert cleaned_df['E_all_nan_numeric'].isnull().all()


    # Categorical columns should remain unchanged (still have their NaNs)
    assert cleaned_df['B_cat'].isnull().sum() == mixed_nulls_df['B_cat'].isnull().sum()
    assert cleaned_df['D_cat_with_nan'].isnull().sum() == mixed_nulls_df['D_cat_with_nan'].isnull().sum()
    assert cleaned_df['F_all_nan_cat'].isnull().all() # This was all NaNs, should remain so

    # Verify specific mean replacements
    mean_A_num = mixed_nulls_df['A_num'].mean() # (1+3+4+5)/4 = 13/4 = 3.25
    assert cleaned_df.loc[1, 'A_num'] == pytest.approx(mean_A_num)

    mean_C_num = mixed_nulls_df['C_num_with_nan'].mean() # (10+20+50)/3 = 80/3
    assert cleaned_df.loc[2, 'C_num_with_nan'] == pytest.approx(mean_C_num)
    assert cleaned_df.loc[3, 'C_num_with_nan'] == pytest.approx(mean_C_num)

    # Non-numeric columns data should be preserved where not null
    assert cleaned_df.loc[0, 'B_cat'] == mixed_nulls_df.loc[0, 'B_cat']


def test_replace_with_mean_all_null_numeric_column(all_null_column_df):
    """Test replace_with_mean where a numeric column is entirely null."""
    # Fixture: {'num_col_all_null': [nan, nan, nan], 'cat_col_all_null': [nan,nan,nan], 'mixed_col': [1, nan, 'a']}
    df_copy = all_null_column_df.copy()
    cleaned_df = replace_with_mean(df_copy)

    # The mean of an all-NaN column is NaN. So, fillna(NaN) doesn't change anything.
    assert cleaned_df['num_col_all_null'].isnull().all()
    # Categorical columns are not affected by replace_with_mean
    assert cleaned_df['cat_col_all_null'].isnull().all()
    # Mixed column - numeric parts are not touched if not NaN, NaNs in object col are not touched
    assert cleaned_df.loc[0,'mixed_col'] == 1
    assert pd.isna(cleaned_df.loc[1,'mixed_col']) # This was NaN, part of an object column, not touched
    assert cleaned_df.loc[2,'mixed_col'] == 'a'

    assert cleaned_df.shape == all_null_column_df.shape

def test_replace_with_mean_empty_df(empty_df):
    """Test replace_with_mean on an empty DataFrame."""
    cleaned_df = replace_with_mean(empty_df.copy())
    assert cleaned_df.empty
    tm.assert_frame_equal(cleaned_df, empty_df)

def test_replace_with_mean_no_nulls_df(no_nulls_df):
    """Test replace_with_mean on a DataFrame with no nulls."""
    df_copy = no_nulls_df.copy()
    cleaned_df = replace_with_mean(df_copy)
    tm.assert_frame_equal(cleaned_df, no_nulls_df)
    assert cleaned_df.shape == no_nulls_df.shape

# endregion Tests for replace_with_mean

# region Tests for replace_with_median
def test_replace_with_median_numeric_nulls(numeric_nulls_df):
    """Test replace_with_median on a DataFrame with only numeric nulls."""
    df_copy = numeric_nulls_df.copy()
    cleaned_df = replace_with_median(df_copy)

    assert cleaned_df.isnull().sum().sum() == 0 # All nulls in numeric columns should be filled
    assert cleaned_df.shape == numeric_nulls_df.shape

    # Calculate expected medians
    median_num_col1 = numeric_nulls_df['num_col1'].median() # [1.0, nan, 3.0, nan] -> median of [1.0, 3.0] is 2.0
    median_num_col2 = numeric_nulls_df['num_col2'].median() # [nan, 2.2, 3.3, 4.4] -> median of [2.2, 3.3, 4.4] is 3.3

    assert cleaned_df.loc[1, 'num_col1'] == pytest.approx(median_num_col1)
    assert cleaned_df.loc[3, 'num_col1'] == pytest.approx(median_num_col1)
    assert cleaned_df.loc[0, 'num_col2'] == pytest.approx(median_num_col2)

    assert cleaned_df.loc[0, 'num_col1'] == numeric_nulls_df.loc[0, 'num_col1']
    assert cleaned_df['cat_col1'].equals(numeric_nulls_df['cat_col1'])

def test_replace_with_median_mixed_nulls(mixed_nulls_df):
    """Test replace_with_median on a mixed-type DataFrame."""
    df_copy = mixed_nulls_df.copy()
    cleaned_df = replace_with_median(df_copy)
    assert cleaned_df.shape == mixed_nulls_df.shape

    assert cleaned_df['A_num'].isnull().sum() == 0
    assert cleaned_df['C_num_with_nan'].isnull().sum() == 0
    # E_all_nan_numeric will be all NaNs, as median of all NaNs is NaN.
    assert cleaned_df['E_all_nan_numeric'].isnull().all()

    assert cleaned_df['B_cat'].isnull().sum() == mixed_nulls_df['B_cat'].isnull().sum()
    assert cleaned_df['D_cat_with_nan'].isnull().sum() == mixed_nulls_df['D_cat_with_nan'].isnull().sum()
    assert cleaned_df['F_all_nan_cat'].isnull().all()

    median_A_num = mixed_nulls_df['A_num'].median() # [1.0, nan, 3.0, 4.0, 5.0] -> median of [1,3,4,5] is 3.5
    assert cleaned_df.loc[1, 'A_num'] == pytest.approx(median_A_num)

    median_C_num = mixed_nulls_df['C_num_with_nan'].median() # [10.0, 20.0, nan, nan, 50.0] -> median of [10,20,50] is 20.0
    assert cleaned_df.loc[2, 'C_num_with_nan'] == pytest.approx(median_C_num)
    assert cleaned_df.loc[3, 'C_num_with_nan'] == pytest.approx(median_C_num)

    assert cleaned_df.loc[0, 'B_cat'] == mixed_nulls_df.loc[0, 'B_cat']

def test_replace_with_median_all_null_numeric_column(all_null_column_df):
    """Test replace_with_median where a numeric column is entirely null."""
    df_copy = all_null_column_df.copy()
    cleaned_df = replace_with_median(df_copy)

    assert cleaned_df['num_col_all_null'].isnull().all() # Median is NaN, so no change
    assert cleaned_df['cat_col_all_null'].isnull().all() # Not affected
    assert cleaned_df.loc[0,'mixed_col'] == 1
    assert pd.isna(cleaned_df.loc[1,'mixed_col']) # This was NaN, part of an object column, not touched
    assert cleaned_df.loc[2,'mixed_col'] == 'a'
    assert cleaned_df.shape == all_null_column_df.shape

def test_replace_with_median_empty_df(empty_df):
    """Test replace_with_median on an empty DataFrame."""
    cleaned_df = replace_with_median(empty_df.copy())
    assert cleaned_df.empty
    tm.assert_frame_equal(cleaned_df, empty_df)

def test_replace_with_median_no_nulls_df(no_nulls_df):
    """Test replace_with_median on a DataFrame with no nulls."""
    df_copy = no_nulls_df.copy()
    cleaned_df = replace_with_median(df_copy)
    tm.assert_frame_equal(cleaned_df, no_nulls_df)
    assert cleaned_df.shape == no_nulls_df.shape

# endregion Tests for replace_with_median

# region Tests for replace_with_mode
def test_replace_with_mode_numeric_nulls(numeric_nulls_df):
    """Test replace_with_mode on numeric nulls."""
    # num_col1: [1.0, np.nan, 3.0, np.nan], mode is 1.0 or 3.0 (pandas takes first) -> 1.0
    # num_col2: [np.nan, 2.2, 3.3, 4.4], modes are 2.2, 3.3, 4.4 (pandas takes first) -> 2.2
    # cat_col1: ['a', 'b', 'c', 'd'] (no nulls)
    df_copy = numeric_nulls_df.copy()
    cleaned_df = replace_with_mode(df_copy)

    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == numeric_nulls_df.shape

    mode_num_col1 = numeric_nulls_df['num_col1'].mode().iloc[0] if not numeric_nulls_df['num_col1'].mode().empty else 0
    mode_num_col2 = numeric_nulls_df['num_col2'].mode().iloc[0] if not numeric_nulls_df['num_col2'].mode().empty else 0
    
    assert cleaned_df.loc[1, 'num_col1'] == pytest.approx(mode_num_col1)
    assert cleaned_df.loc[3, 'num_col1'] == pytest.approx(mode_num_col1)
    assert cleaned_df.loc[0, 'num_col2'] == pytest.approx(mode_num_col2)
    assert cleaned_df['cat_col1'].equals(numeric_nulls_df['cat_col1'])

def test_replace_with_mode_categorical_nulls(categorical_nulls_df):
    """Test replace_with_mode on categorical nulls."""
    # num_col1: [1.0, 2.0, 3.0, 4.0] (no nulls)
    # cat_col1: ['a', np.nan, 'c', np.nan], modes are 'a', 'c' -> 'a'
    # cat_col2: [np.nan, 'x', 'y', 'z'], modes are 'x','y','z' -> 'x'
    df_copy = categorical_nulls_df.copy()
    cleaned_df = replace_with_mode(df_copy)

    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == categorical_nulls_df.shape

    mode_cat_col1 = categorical_nulls_df['cat_col1'].mode().iloc[0] if not categorical_nulls_df['cat_col1'].mode().empty else "Unknown"
    mode_cat_col2 = categorical_nulls_df['cat_col2'].mode().iloc[0] if not categorical_nulls_df['cat_col2'].mode().empty else "Unknown"

    assert cleaned_df.loc[1, 'cat_col1'] == mode_cat_col1
    assert cleaned_df.loc[3, 'cat_col1'] == mode_cat_col1
    assert cleaned_df.loc[0, 'cat_col2'] == mode_cat_col2
    assert cleaned_df['num_col1'].equals(categorical_nulls_df['num_col1'])


def test_replace_with_mode_mixed_nulls(mixed_nulls_df):
    """Test replace_with_mode on a mixed-type DataFrame."""
    # A_num: [1.0, np.nan, 3.0, 4.0, 5.0], mode is 1.0 (or 3,4,5) -> 1.0
    # B_cat: ['apple', 'banana', np.nan, 'cherry', 'banana'], mode is 'banana'
    # C_num_with_nan: [10.0, 20.0, np.nan, np.nan, 50.0], modes 10,20,50 -> 10.0
    # D_cat_with_nan: [None, 'dog', 'cat', None, 'dog'], mode is 'dog'
    # E_all_nan_numeric: [nan, nan, nan, nan, nan], mode is empty, fill with 0
    # F_all_nan_cat: [nan, nan, nan, nan, nan], mode is empty, fill with "Unknown"
    df_copy = mixed_nulls_df.copy()
    cleaned_df = replace_with_mode(df_copy)

    assert cleaned_df.isnull().sum().sum() == 0 # All nulls should be handled
    assert cleaned_df.shape == mixed_nulls_df.shape

    mode_A_num = mixed_nulls_df['A_num'].mode().iloc[0]
    assert cleaned_df.loc[1, 'A_num'] == pytest.approx(mode_A_num)

    mode_B_cat = mixed_nulls_df['B_cat'].mode().iloc[0]
    assert cleaned_df.loc[2, 'B_cat'] == mode_B_cat
    
    mode_C_num = mixed_nulls_df['C_num_with_nan'].mode().iloc[0]
    assert cleaned_df.loc[2, 'C_num_with_nan'] == pytest.approx(mode_C_num)
    assert cleaned_df.loc[3, 'C_num_with_nan'] == pytest.approx(mode_C_num)

    mode_D_cat = mixed_nulls_df['D_cat_with_nan'].mode().iloc[0]
    assert cleaned_df.loc[0, 'D_cat_with_nan'] == mode_D_cat
    assert cleaned_df.loc[3, 'D_cat_with_nan'] == mode_D_cat
    
    assert (cleaned_df['E_all_nan_numeric'] == 0).all() # Default for numeric when mode is empty
    # F_all_nan_cat is float64 because it's all np.nan, so it will also be filled with 0 by current logic
    assert (cleaned_df['F_all_nan_cat'] == 0).all()


def test_replace_with_mode_all_null_columns(all_null_column_df):
    """Test replace_with_mode for columns that are entirely null."""
    # num_col_all_null: [nan, nan, nan] -> fill with 0
    # cat_col_all_null: [nan, nan, nan] (this is float64) -> fill with 0
    # mixed_col: [1, np.nan, 'a'] -> mode is 1 (or 'a') -> 1
    df_copy = all_null_column_df.copy()
    cleaned_df = replace_with_mode(df_copy)
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == all_null_column_df.shape

    assert (cleaned_df['num_col_all_null'] == 0).all()
    # cat_col_all_null is float64 because it's all np.nan, filled with 0 by current logic
    assert (cleaned_df['cat_col_all_null'] == 0).all()
    
    mode_mixed_col = all_null_column_df['mixed_col'].mode().iloc[0] # Should be 1
    assert cleaned_df.loc[1, 'mixed_col'] == mode_mixed_col


def test_replace_with_mode_multiple_modes_takes_first(no_nulls_df):
    """Test that replace_with_mode uses the first mode if multiple exist."""
    # Create a df with multiple modes specifically for this test
    data = {'multi_mode_col': [1, 1, 2, 2, 3, np.nan, np.nan]}
    df = pd.DataFrame(data)
    # Pandas mode() for [1,1,2,2,3] returns a Series [1,2]. iloc[0] takes 1.
    expected_mode = df['multi_mode_col'].mode().iloc[0] # Should be 1

    cleaned_df = replace_with_mode(df.copy())
    assert cleaned_df.loc[5, 'multi_mode_col'] == expected_mode
    assert cleaned_df.loc[6, 'multi_mode_col'] == expected_mode
    assert cleaned_df.isnull().sum().sum() == 0


def test_replace_with_mode_empty_df(empty_df):
    """Test replace_with_mode on an empty DataFrame."""
    cleaned_df = replace_with_mode(empty_df.copy())
    assert cleaned_df.empty
    tm.assert_frame_equal(cleaned_df, empty_df)

def test_replace_with_mode_no_nulls_df(no_nulls_df):
    """Test replace_with_mode on a DataFrame with no nulls."""
    df_copy = no_nulls_df.copy()
    cleaned_df = replace_with_mode(df_copy)
    tm.assert_frame_equal(cleaned_df, no_nulls_df)
    assert cleaned_df.shape == no_nulls_df.shape

def test_replace_with_mode_all_nan_object_column(all_nan_object_col_df):
    """Test replace_with_mode for an all-NaN object column (should use 'Unknown')."""
    df_copy = all_nan_object_col_df.copy()
    cleaned_df = replace_with_mode(df_copy)
    assert (cleaned_df['obj_all_nan'] == "Unknown").all()
    assert cleaned_df.isnull().sum().sum() == 0
    assert cleaned_df.shape == all_nan_object_col_df.shape

# endregion Tests for replace_with_mode

# region Tests for forward_fill
def test_forward_fill_numeric_nulls(numeric_nulls_df):
    """Test forward_fill on numeric nulls."""
    # num_col1: [1.0, np.nan, 3.0, np.nan] -> ffill -> [1.0, 1.0, 3.0, 3.0]
    # num_col2: [np.nan, 2.2, 3.3, 4.4] -> ffill -> [np.nan, 2.2, 3.3, 4.4] (leading NaN remains)
    # cat_col1: ['a', 'b', 'c', 'd']
    df_copy = numeric_nulls_df.copy()
    cleaned_df = forward_fill(df_copy)

    assert cleaned_df.shape == numeric_nulls_df.shape
    # Check num_col1
    expected_num_col1 = pd.Series([1.0, 1.0, 3.0, 3.0], name='num_col1')
    tm.assert_series_equal(cleaned_df['num_col1'], expected_num_col1, check_dtype=False)
    # Check num_col2 (leading NaN)
    assert pd.isna(cleaned_df.loc[0, 'num_col2'])
    assert cleaned_df.loc[1, 'num_col2'] == 2.2
    # Check cat_col1 (should be unchanged)
    tm.assert_series_equal(cleaned_df['cat_col1'], numeric_nulls_df['cat_col1'])
    # Overall null count
    assert cleaned_df.isnull().sum().sum() == 1 # One leading NaN in num_col2

def test_forward_fill_categorical_nulls(categorical_nulls_df):
    """Test forward_fill on categorical nulls."""
    # cat_col1: ['a', np.nan, 'c', np.nan] -> ffill -> ['a', 'a', 'c', 'c']
    # cat_col2: [np.nan, 'x', 'y', 'z'] -> ffill -> [np.nan, 'x', 'y', 'z'] (leading NaN)
    df_copy = categorical_nulls_df.copy()
    cleaned_df = forward_fill(df_copy)

    assert cleaned_df.shape == categorical_nulls_df.shape
    expected_cat_col1 = pd.Series(['a', 'a', 'c', 'c'], name='cat_col1')
    tm.assert_series_equal(cleaned_df['cat_col1'], expected_cat_col1, check_dtype=False)
    
    assert pd.isna(cleaned_df.loc[0, 'cat_col2'])
    assert cleaned_df.loc[1, 'cat_col2'] == 'x'
    tm.assert_series_equal(cleaned_df['num_col1'], categorical_nulls_df['num_col1'])
    assert cleaned_df.isnull().sum().sum() == 1 # One leading NaN in cat_col2


def test_forward_fill_mixed_leading_nulls(mixed_nulls_df):
    """Test forward_fill with various nulls, including leading ones."""
    # A_num: [1.0, np.nan, 3.0, 4.0, 5.0] -> [1.0, 1.0, 3.0, 4.0, 5.0]
    # B_cat: ['apple', 'banana', np.nan, 'cherry', 'banana'] -> ['apple', 'banana', 'banana', 'cherry', 'banana']
    # C_num_with_nan: [10.0, 20.0, np.nan, np.nan, 50.0] -> [10.0, 20.0, 20.0, 20.0, 50.0]
    # D_cat_with_nan: [None, 'dog', 'cat', None, 'dog'] -> [None, 'dog', 'cat', 'cat', 'dog'] (leading None remains)
    # E_all_nan_numeric: [nan, nan, nan, nan, nan] -> all nan
    # F_all_nan_cat: [nan, nan, nan, nan, nan] -> all nan
    df_copy = mixed_nulls_df.copy()
    cleaned_df = forward_fill(df_copy)
    assert cleaned_df.shape == mixed_nulls_df.shape

    assert cleaned_df.loc[1, 'A_num'] == 1.0
    assert cleaned_df.loc[2, 'B_cat'] == 'banana'
    assert cleaned_df.loc[2, 'C_num_with_nan'] == 20.0
    assert cleaned_df.loc[3, 'C_num_with_nan'] == 20.0
    
    assert pd.isna(cleaned_df.loc[0, 'D_cat_with_nan']) # Leading NaN
    assert cleaned_df.loc[3, 'D_cat_with_nan'] == 'cat'
    
    assert cleaned_df['E_all_nan_numeric'].isnull().all() # All NaNs remain
    assert cleaned_df['F_all_nan_cat'].isnull().all()     # All NaNs remain

    # Count total nulls remaining: 1 in D_cat_with_nan, 5 in E, 5 in F = 11
    assert cleaned_df.isnull().sum().sum() == (1 + mixed_nulls_df['E_all_nan_numeric'].shape[0] + mixed_nulls_df['F_all_nan_cat'].shape[0])


def test_forward_fill_all_null_column(all_null_column_df):
    """Test forward_fill on a DataFrame with all-null columns."""
    df_copy = all_null_column_df.copy()
    cleaned_df = forward_fill(df_copy)

    # All-NaN columns should remain all-NaN
    assert cleaned_df['num_col_all_null'].isnull().all()
    assert cleaned_df['cat_col_all_null'].isnull().all() # This is float64, remains all NaN

    # mixed_col should be forward filled: [1, np.nan, 'a'] -> [1, 1, 'a']
    expected_mixed_col = pd.Series([1, 1, 'a'], name='mixed_col', dtype=object)
    tm.assert_series_equal(cleaned_df['mixed_col'], expected_mixed_col)
    assert cleaned_df.shape == all_null_column_df.shape


def test_forward_fill_empty_df(empty_df):
    """Test forward_fill on an empty DataFrame."""
    cleaned_df = forward_fill(empty_df.copy())
    assert cleaned_df.empty
    tm.assert_frame_equal(cleaned_df, empty_df)

def test_forward_fill_no_nulls_df(no_nulls_df):
    """Test forward_fill on a DataFrame with no nulls."""
    df_copy = no_nulls_df.copy()
    cleaned_df = forward_fill(df_copy)
    tm.assert_frame_equal(cleaned_df, no_nulls_df)
    assert cleaned_df.shape == no_nulls_df.shape

# endregion Tests for forward_fill

# region Tests for backward_fill
def test_backward_fill_numeric_nulls(numeric_nulls_df):
    """Test backward_fill on numeric nulls."""
    # num_col1: [1.0, np.nan, 3.0, np.nan] -> bfill -> [1.0, 3.0, 3.0, np.nan] (trailing NaN)
    # num_col2: [np.nan, 2.2, 3.3, 4.4] -> bfill -> [2.2, 2.2, 3.3, 4.4]
    # cat_col1: ['a', 'b', 'c', 'd']
    df_copy = numeric_nulls_df.copy()
    cleaned_df = backward_fill(df_copy)

    assert cleaned_df.shape == numeric_nulls_df.shape
    # Check num_col1 (trailing NaN)
    assert cleaned_df.loc[1, 'num_col1'] == 3.0
    assert pd.isna(cleaned_df.loc[3, 'num_col1'])
    # Check num_col2
    expected_num_col2 = pd.Series([2.2, 2.2, 3.3, 4.4], name='num_col2')
    tm.assert_series_equal(cleaned_df['num_col2'], expected_num_col2, check_dtype=False)
    # Check cat_col1
    tm.assert_series_equal(cleaned_df['cat_col1'], numeric_nulls_df['cat_col1'])
    assert cleaned_df.isnull().sum().sum() == 1 # One trailing NaN in num_col1

def test_backward_fill_categorical_nulls(categorical_nulls_df):
    """Test backward_fill on categorical nulls."""
    # cat_col1: ['a', np.nan, 'c', np.nan] -> bfill -> ['a', 'c', 'c', np.nan] (trailing NaN)
    # cat_col2: [np.nan, 'x', 'y', 'z'] -> bfill -> ['x', 'x', 'y', 'z']
    df_copy = categorical_nulls_df.copy()
    cleaned_df = backward_fill(df_copy)

    assert cleaned_df.shape == categorical_nulls_df.shape
    assert cleaned_df.loc[1, 'cat_col1'] == 'c'
    assert pd.isna(cleaned_df.loc[3, 'cat_col1'])
    
    expected_cat_col2 = pd.Series(['x', 'x', 'y', 'z'], name='cat_col2', dtype=object)
    tm.assert_series_equal(cleaned_df['cat_col2'], expected_cat_col2, check_dtype=False)
    
    tm.assert_series_equal(cleaned_df['num_col1'], categorical_nulls_df['num_col1'])
    assert cleaned_df.isnull().sum().sum() == 1 # One trailing NaN in cat_col1


def test_backward_fill_mixed_trailing_nulls(mixed_nulls_df):
    """Test backward_fill with various nulls, including trailing ones."""
    # A_num: [1.0, np.nan, 3.0, 4.0, 5.0] -> [1.0, 3.0, 3.0, 4.0, 5.0]
    # B_cat: ['apple', 'banana', np.nan, 'cherry', 'banana'] -> ['apple', 'banana', 'cherry', 'cherry', 'banana']
    # C_num_with_nan: [10.0, 20.0, np.nan, np.nan, 50.0] -> [10.0, 20.0, 50.0, 50.0, 50.0]
    # D_cat_with_nan: [None, 'dog', 'cat', None, 'dog'] -> ['dog', 'dog', 'cat', 'dog', 'dog']
    # E_all_nan_numeric: [nan, nan, nan, nan, nan] -> all nan (trailing NaNs remain)
    # F_all_nan_cat: [nan, nan, nan, nan, nan] -> all nan (trailing NaNs remain)
    df_copy = mixed_nulls_df.copy()
    cleaned_df = backward_fill(df_copy)
    assert cleaned_df.shape == mixed_nulls_df.shape

    assert cleaned_df.loc[1, 'A_num'] == 3.0
    assert cleaned_df.loc[2, 'B_cat'] == 'cherry'
    assert cleaned_df.loc[2, 'C_num_with_nan'] == 50.0
    assert cleaned_df.loc[3, 'C_num_with_nan'] == 50.0
    assert cleaned_df.loc[0, 'D_cat_with_nan'] == 'dog'
    assert cleaned_df.loc[3, 'D_cat_with_nan'] == 'dog'
        
    assert cleaned_df['E_all_nan_numeric'].isnull().all()
    assert cleaned_df['F_all_nan_cat'].isnull().all()

    # Count total nulls remaining: 5 in E, 5 in F = 10
    # (Original mixed_nulls_df has 1+1+2+2+5+5 = 16 nulls)
    # After bfill, A_num (0), B_cat (0), C_num(0), D_cat(0), E(5), F(5) -> 10 nulls
    assert cleaned_df.isnull().sum().sum() == (mixed_nulls_df['E_all_nan_numeric'].shape[0] + mixed_nulls_df['F_all_nan_cat'].shape[0])


def test_backward_fill_all_null_column(all_null_column_df):
    """Test backward_fill on a DataFrame with all-null columns."""
    df_copy = all_null_column_df.copy()
    cleaned_df = backward_fill(df_copy)

    # All-NaN columns should remain all-NaN
    assert cleaned_df['num_col_all_null'].isnull().all()
    assert cleaned_df['cat_col_all_null'].isnull().all() # This is float64, remains all NaN

    # mixed_col should be backward filled: [1, np.nan, 'a'] -> [1, 'a', 'a']
    expected_mixed_col = pd.Series([1, 'a', 'a'], name='mixed_col', dtype=object)
    tm.assert_series_equal(cleaned_df['mixed_col'], expected_mixed_col)
    assert cleaned_df.shape == all_null_column_df.shape

def test_backward_fill_empty_df(empty_df):
    """Test backward_fill on an empty DataFrame."""
    cleaned_df = backward_fill(empty_df.copy())
    assert cleaned_df.empty
    tm.assert_frame_equal(cleaned_df, empty_df)

def test_backward_fill_no_nulls_df(no_nulls_df):
    """Test backward_fill on a DataFrame with no nulls."""
    df_copy = no_nulls_df.copy()
    cleaned_df = backward_fill(df_copy)
    tm.assert_frame_equal(cleaned_df, no_nulls_df)
    assert cleaned_df.shape == no_nulls_df.shape

# endregion Tests for backward_fill

# region Tests for evaluate_methods

@pytest.fixture
def sample_eval_dfs():
    """Provides sample DataFrames for evaluate_methods tests."""
    original = pd.DataFrame({
        'A': [1, np.nan, 3, np.nan, 5],
        'B': [np.nan, 'x', 'y', 'z', np.nan],
        'C': [10, 20, 30, 40, 50] # No nulls
    }) # Total 4 nulls, shape (5,3)

    # Method1: Drops rows with any nulls
    # Row 0 (1, nan, 10) -> dropped
    # Row 1 (nan, 'x', 20) -> dropped
    # Row 3 (nan, 'z', 40) -> dropped
    # Row 4 (5, nan, 50) -> dropped
    # Remaining: Row 2 (3, 'y', 30)
    method1_cleaned = original.dropna() # Shape (1,3), 0 nulls, 4 nulls removed

    # Method2: Fills numeric with mean, categorical with mode
    # A: mean of (1,3,5) is 3. NaNs at idx 1, 3 become 3. [1,3,3,3,5]
    # B: mode of ('x','y','z') is 'x'. NaNs at idx 0, 4 become 'x'. ['x','x','y','z','x']
    method2_cleaned = original.copy()
    method2_cleaned['A'] = method2_cleaned['A'].fillna(method2_cleaned['A'].mean())
    method2_cleaned['B'] = method2_cleaned['B'].fillna(method2_cleaned['B'].mode().iloc[0])
    # Shape (5,3), 0 nulls, 4 nulls removed

    # Method3: Fills all with a fixed value (e.g., 0), keeps shape
    method3_cleaned = original.fillna(0) # Shape (5,3), 0 nulls, 4 nulls removed
    
    # Method4: Less effective, leaves some nulls, e.g. ffill
    method4_cleaned = original.ffill()
    # A: [1,1,3,3,5] (0 nulls)
    # B: [nan, 'x', 'y', 'z', 'z'] (1 null) -> total 1 null, 3 nulls removed. Shape (5,3)

    cleaned_versions = {
        "drop_all_null_rows": method1_cleaned, # score: (4/4)*0.5 + (1/5)*0.25 + (3/3)*0.25 = 0.5 + 0.05 + 0.25 = 0.80
        "mean_mode_fill": method2_cleaned,   # score: (4/4)*0.5 + (5/5)*0.25 + (3/3)*0.25 = 0.5 + 0.25 + 0.25 = 1.0
        "fixed_fill": method3_cleaned,       # score: (4/4)*0.5 + (5/5)*0.25 + (3/3)*0.25 = 0.5 + 0.25 + 0.25 = 1.0
        "forward_fill": method4_cleaned      # score: (3/4)*0.5 + (5/5)*0.25 + (3/3)*0.25 = 0.375 + 0.25 + 0.25 = 0.875
    }
    return original, cleaned_versions

def test_evaluate_methods_selects_best(sample_eval_dfs):
    """Test that evaluate_methods selects the method with the highest score."""
    original_df, cleaned_versions = sample_eval_dfs
    log_lines = []
    # mean_mode_fill and fixed_fill both have score 1.0. evaluate_methods will pick the one it encounters first.
    # In the fixture, mean_mode_fill is before fixed_fill if dict insertion order is preserved (Python 3.7+)
    # Let's ensure the test doesn't depend on this by slightly adjusting one score or testing for either.
    # For simplicity, let's assume fixed_fill appears first if scores are equal or make one slightly better.
    # The current logic picks the *last* one if scores are equal. So fixed_fill (score 1.0) would be chosen over mean_mode_fill (score 1.0)
    # if it came after it in the dict iteration.
    # To make it deterministic, let's make one score clearly higher for this test if needed,
    # or accept any of the top-scoring methods.
    # The current scores are: drop: 0.80, mean_mode: 1.0, fixed: 1.0, ffill: 0.875
    # So, either "mean_mode_fill" or "fixed_fill" can be chosen.
    best_method = evaluate_methods(original_df, cleaned_versions, log_lines)
    assert best_method in ["mean_mode_fill", "fixed_fill"]
    assert "Best strategy selected: " in log_lines[-1] # Last log line should announce best
    assert len(log_lines) == (len(cleaned_versions) * 5 + 1) # 5 lines per method + 1 overall line


def test_evaluate_methods_prefers_completeness_and_shape(sample_eval_dfs):
    """Test that score prioritizes null removal and then shape retention."""
    original_df, cleaned_versions = sample_eval_dfs
    log_lines = []
    # "mean_mode_fill" and "fixed_fill" are best (score 1.0)
    # "forward_fill" (score 0.875) is better than "drop_all_null_rows" (score 0.80)
    # because it preserves all rows even if it doesn't remove all nulls.
    
    # Modify cleaned_versions to make one clearly superior
    # Let method2 remove all nulls and keep shape (Score 1.0)
    # Let method1 remove all nulls but lose many rows (Score ~0.80 for sample_eval_dfs)
    # Let method4 remove fewer nulls but keep shape (Score ~0.875 for sample_eval_dfs)
    
    test_versions = {
        "drop_rows": cleaned_versions["drop_all_null_rows"], # Score 0.80
        "fill_most_keep_shape": cleaned_versions["forward_fill"], # Score 0.875
        "fill_all_keep_shape": cleaned_versions["mean_mode_fill"] # Score 1.0
    }
    best_method = evaluate_methods(original_df, test_versions, log_lines)
    assert best_method == "fill_all_keep_shape"


def test_evaluate_methods_no_nulls_original(no_nulls_df):
    """Test evaluate_methods when the original DataFrame has no nulls."""
    cleaned_versions = {
        "method_A": no_nulls_df.copy(), # No change
        "method_B": no_nulls_df.copy().assign(col_a = no_nulls_df['col_a'] * 2) # Changed data but no nulls
    }
    log_lines = []
    # original_nulls = 0. Score = (1.0)*0.5 + row_ratio*0.25 + col_ratio*0.25
    # For method_A: 0.5 + 0.25 + 0.25 = 1.0
    # For method_B: 0.5 + 0.25 + 0.25 = 1.0
    # It will pick the first one encountered with the best score if tied.
    best_method = evaluate_methods(no_nulls_df, cleaned_versions, log_lines)
    assert best_method == "method_A" 
    assert "Original DataFrame has no nulls. Scores reflect shape retention." not in "".join(log_lines) # No special message for this
    # Check score calculation: nulls_removed / original_nulls becomes 1.0 if original_nulls is 0.
    # This is (1.0 * 0.5) + (1.0 * 0.25) + (1.0 * 0.25) = 1.0 for both.
    # The log should reflect scores of 1.0 for methods that preserve shape.
    assert any(f"Strategy score: {1.0:.4f}" in line for line in log_lines)


def test_evaluate_methods_empty_original(empty_df):
    """Test evaluate_methods when the original DataFrame is empty."""
    cleaned_versions = {
        "method_X": empty_df.copy(),
        "method_Y": pd.DataFrame({'a':[1]}) # A method that creates data
    }
    log_lines = []
    # original_nulls = 0, original_shape = (0,0)
    # row_ratio and col_ratio will involve division by zero for original_shape.
    # The code has original_shape[0] if original_shape[0] else 0, so ratio is 0 if original dim is 0.
    # Score for method_X (empty): (0/0 if 0 > 0 else 1.0)*0.5 + (0/0 if 0 else 0)*0.25 + (0/0 if 0 else 0)*0.25
    # = 1.0 * 0.5 + 0 * 0.25 + 0 * 0.25 = 0.5
    # Score for method_Y (non-empty): (0/0 if 0 > 0 else 1.0)*0.5 + (1/0 if 0 else 0)*0.25 + (1/0 if 0 else 0)*0.25
    # = 1.0 * 0.5 + 0 * 0.25 + 0 * 0.25 = 0.5
    # Both would have score 0.5. It will pick the first one.
    best_method = evaluate_methods(empty_df, cleaned_versions, log_lines)
    assert best_method == "method_X" 
    assert any(f"Strategy score: {0.5:.4f}" in line for line in log_lines)


def test_evaluate_methods_log_content(sample_eval_dfs):
    """Test the content and structure of log lines from evaluate_methods."""
    original_df, cleaned_versions = sample_eval_dfs
    log_lines = []
    evaluate_methods(original_df, cleaned_versions, log_lines)

    assert len(log_lines) > 0
    assert "Method tried: drop_all_null_rows" in log_lines[0]
    assert " - Nulls removed: " in log_lines[1]
    assert " - Remaining nulls: " in log_lines[2]
    assert " - Shape after cleaning: " in log_lines[3]
    assert " - Strategy score: " in log_lines[4] # includes newline
    
    # forward_fill is the 4th method, its block starts at index 15 (0-indexed)
    assert "Method tried: forward_fill" in log_lines[15] 
    assert "✅ Best strategy selected: " in log_lines[-1]

# endregion Tests for evaluate_methods

# region Integration Tests for process_csv

def test_process_csv_integration_basic(mixed_nulls_df):
    """Basic integration test for process_csv with a DataFrame having nulls."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_csv_path = os.path.join(tmpdir, "input.csv")
        output_csv_path = os.path.join(tmpdir, "output.csv")
        log_file_path = os.path.join(tmpdir, "null_handling_log.txt")

        # Save the mixed_nulls_df to a temporary CSV file
        mixed_nulls_df.to_csv(input_csv_path, index=False)

        process_csv(input_csv_path, output_csv_path)

        assert os.path.exists(output_csv_path)
        assert os.path.exists(log_file_path)

        processed_df = pd.read_csv(output_csv_path)
        # The best method for mixed_nulls_df according to evaluate_methods
        # (using the sample_eval_dfs logic as a guide) would likely be one that fills all nulls
        # and preserves shape, e.g., mean/mode fill or fixed fill.
        # We expect no nulls in the output if a fill strategy is chosen.
        # If drop_nulls was chosen, it would be empty.
        # The key is that *some* processing happened and an output was generated.
        # A more robust check would be to replicate the logic of evaluate_methods here,
        # but for an integration test, checking for non-null output (or specific known output) is good.
        
        # Let's verify the output isn't empty and has fewer or equal nulls than input
        assert not processed_df.empty
        assert processed_df.isnull().sum().sum() < mixed_nulls_df.isnull().sum().sum() or \
               (mixed_nulls_df.isnull().sum().sum() == 0 and processed_df.isnull().sum().sum() == 0)


        with open(log_file_path, "r") as f:
            log_content = f.read()
        assert "Processing file: " + input_csv_path in log_content
        assert "Initial shape: " in log_content
        assert "Total null values: " in log_content
        assert "Best strategy selected: " in log_content
        # The following are standard log messages, not in the specific log file
        assert "Cleaned CSV saved at: " not in log_content
        assert "Decision-making log saved at: " not in log_content

def test_process_csv_no_nulls_input(no_nulls_df):
    """Test process_csv with an input CSV that has no null values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_csv_path = os.path.join(tmpdir, "input_no_nulls.csv")
        output_csv_path = os.path.join(tmpdir, "output_no_nulls.csv")
        
        no_nulls_df.to_csv(input_csv_path, index=False)
        process_csv(input_csv_path, output_csv_path)

        assert os.path.exists(output_csv_path)
        processed_df = pd.read_csv(output_csv_path)
        tm.assert_frame_equal(processed_df, no_nulls_df) # Output should be identical to input

        log_file_path = os.path.join(tmpdir, "null_handling_log.txt")
        assert os.path.exists(log_file_path)
        with open(log_file_path, "r") as f:
            log_content = f.read()
        assert "Total null values: 0" in log_content
        # Best strategy might still be identified, e.g., one that preserves shape perfectly.

def test_process_csv_empty_input_csv(empty_df):
    """Test process_csv with an empty input CSV file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_csv_path = os.path.join(tmpdir, "empty_input.csv")
        output_csv_path = os.path.join(tmpdir, "empty_output.csv")
        log_file_path = os.path.join(tmpdir, "null_handling_log.txt")

        empty_df.to_csv(input_csv_path, index=False) # Creates an empty file with headers if df has columns
        
        # If empty_df fixture is truly empty (no columns), to_csv creates an empty file.
        # If it has columns but no rows, it creates a file with only headers.
        # Let's ensure it's a truly empty file for one variant of this test.
        with open(input_csv_path, 'w') as f:
            f.write("") # Create a truly empty file

        process_csv(input_csv_path, output_csv_path)

        # For a truly empty CSV, pandas read_csv might raise EmptyDataError or return empty DF
        # The `process_csv` function logs "Input CSV is empty. No processing done." and returns.
        # So, no output CSV or log file should be created by `process_csv` itself in this case.
        # However, the logging in process_csv is to python's logging, not the log file it creates.
        # The log file is only created if processing proceeds.
        assert not os.path.exists(output_csv_path) # No output CSV should be created
        assert not os.path.exists(log_file_path) # No custom log file from the function

def test_process_csv_empty_input_with_headers(empty_df):
    """Test process_csv with an input CSV that has headers but no data."""
    df_with_cols_no_rows = pd.DataFrame(columns=['col1', 'col2'])
    with tempfile.TemporaryDirectory() as tmpdir:
        input_csv_path = os.path.join(tmpdir, "empty_data.csv")
        output_csv_path = os.path.join(tmpdir, "empty_data_output.csv")
        log_file_path = os.path.join(tmpdir, "null_handling_log.txt")

        df_with_cols_no_rows.to_csv(input_csv_path, index=False)
        process_csv(input_csv_path, output_csv_path)
        
        # df.empty is true. Function should log "Input CSV is empty." and return.
        assert not os.path.exists(output_csv_path)
        assert not os.path.exists(log_file_path)


def test_process_csv_non_existent_input():
    """Test process_csv with a non-existent input CSV file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_csv_path = os.path.join(tmpdir, "non_existent_input.csv")
        output_csv_path = os.path.join(tmpdir, "output.csv")
        log_file_path = os.path.join(tmpdir, "null_handling_log.txt")

        process_csv(input_csv_path, output_csv_path)

        # Function should log "Input file not found" and return.
        assert not os.path.exists(output_csv_path)
        assert not os.path.exists(log_file_path) # Log file is only created on successful processing path

def test_process_csv_output_directory_creation():
    """Test that process_csv creates the output directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a dummy input CSV
        input_csv_path = os.path.join(tmpdir, "input.csv")
        dummy_df = pd.DataFrame({'a':[1,2,np.nan]})
        dummy_df.to_csv(input_csv_path, index=False)

        # Define an output path in a subdirectory that doesn't exist yet
        output_subdir = os.path.join(tmpdir, "new_output_dir")
        output_csv_path = os.path.join(output_subdir, "output.csv")
        log_file_path = os.path.join(output_subdir, "null_handling_log.txt") # log also goes here

        assert not os.path.exists(output_subdir) # Ensure subdir does not exist

        process_csv(input_csv_path, output_csv_path)

        assert os.path.exists(output_subdir) # Subdir should be created
        assert os.path.exists(output_csv_path) # Output CSV should exist in subdir
        assert os.path.exists(log_file_path) # Log file should also exist in subdir
        
        processed_df = pd.read_csv(output_csv_path)
        assert processed_df['a'].isnull().sum() == 0 # e.g. filled with mean or mode or fixed

# endregion Integration Tests for process_csv
