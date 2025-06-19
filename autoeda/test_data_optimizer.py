import pandas as pd
import numpy as np
import os
import unittest
from data_optimizer import optimize_dtypes, optimize_csv
import logging
from io import StringIO

class TestDataOptimizer(unittest.TestCase):

    def test_optimize_dtypes_categorical(self):
        data = {
            'col_cat': ['A'] * 25 + ['B'] * 25 + ['C'] * 10,  # 3 unique values, length 60
            'col_obj': [f'item_{i}' for i in range(60)]  # 60 unique values, length 60
        }
        df = pd.DataFrame(data)
        df_optimized = optimize_dtypes(df.copy())
        self.assertEqual(df_optimized['col_cat'].dtype, 'category')
        self.assertEqual(df_optimized['col_obj'].dtype, 'object')

    def test_optimize_dtypes_numeric(self):
        data = {
            'col_float64': np.random.rand(10).astype('float64'),
            'col_int64': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype='int64') # length 10
        }
        df = pd.DataFrame(data)
        df_optimized = optimize_dtypes(df.copy())
        self.assertEqual(df_optimized['col_float64'].dtype, 'float32')
        # Check if int64 was downcast to a smaller int type
        self.assertTrue(str(df_optimized['col_int64'].dtype).startswith('int'))
        self.assertNotEqual(df_optimized['col_int64'].dtype, 'int64')


    def test_optimize_dtypes_datetime(self):
        data = {'event_date': ['2023-01-01', '2023-01-02', '2023-01-03']}
        df = pd.DataFrame(data)
        df_optimized = optimize_dtypes(df.copy())
        self.assertEqual(df_optimized['event_date'].dtype, 'datetime64[ns]')

    def test_optimize_dtypes_datetime_error(self):
        data = {'creation_time': ['2023-01-01', 'not-a-date', '2023-01-03']}
        df = pd.DataFrame(data)

        # Capture logs
        # Ensure the logger used by data_optimizer is clean and we can capture its output
        # For simplicity, we'll capture from the root logger, assuming no complex logging setup in data_optimizer
        log_stream = StringIO()
        # Get the root logger
        logger = logging.getLogger()
        # Store original handlers and level
        original_handlers = list(logger.handlers)
        original_level = logger.level

        # Clear existing handlers for a clean capture, if any specific to root
        for h in original_handlers:
            logger.removeHandler(h)

        handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # Match format in data_optimizer
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO) # Capture INFO, WARNING, ERROR

        df_optimized = optimize_dtypes(df.copy())

        # Restore original logger state
        logger.removeHandler(handler)
        for h in original_handlers: # Re-add original handlers
            logger.addHandler(h)
        logger.setLevel(original_level)

        self.assertNotEqual(df_optimized['creation_time'].dtype, 'datetime64[ns]')
        log_output = log_stream.getvalue()
        self.assertIn("Could not convert column 'creation_time' to datetime", log_output)
        # Check that it's a WARNING level message
        self.assertIn("WARNING", log_output)


    def setUp(self):
        self.sample_data = {
            'ID': range(100),
            'Category': ['TypeA'] * 30 + ['TypeB'] * 70, # < 50 unique, should be category
            'Value_Float': np.random.rand(100).astype('float64'),
            'Value_Int': np.random.randint(0, 1000, 100).astype('int64'),
            'Timestamp_Str': (pd.to_datetime('2023-01-01') + pd.to_timedelta(np.arange(100), 'D')).astype(str) # ensure string for CSV
        }
        df_sample = pd.DataFrame(self.sample_data)

        self.sample_input_csv = 'sample_input_for_test.csv'
        self.sample_output_csv = 'sample_output_for_test.csv'
        df_sample.to_csv(self.sample_input_csv, index=False)

        # Setup logger for capturing logs from optimize_csv
        self.log_stream_csv_test = StringIO()
        # Get the root logger as optimize_csv uses logging.info directly
        self.csv_test_logger = logging.getLogger()
        self.csv_test_original_handlers = list(self.csv_test_logger.handlers)
        self.csv_test_original_level = self.csv_test_logger.level

        # Clear existing handlers for a clean capture
        for h_csv in self.csv_test_original_handlers:
            self.csv_test_logger.removeHandler(h_csv)
        
        self.csv_test_handler = logging.StreamHandler(self.log_stream_csv_test)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # Match format
        self.csv_test_handler.setFormatter(formatter)
        self.csv_test_logger.addHandler(self.csv_test_handler)
        self.csv_test_logger.setLevel(logging.INFO)


    def tearDown(self):
        if os.path.exists(self.sample_input_csv):
            os.remove(self.sample_input_csv)
        if os.path.exists(self.sample_output_csv):
            os.remove(self.sample_output_csv)

        # Restore original logger state for csv_test_logger
        self.csv_test_logger.removeHandler(self.csv_test_handler)
        for h_csv_orig in self.csv_test_original_handlers:
            self.csv_test_logger.addHandler(h_csv_orig)
        self.csv_test_logger.setLevel(self.csv_test_original_level)


    def test_optimize_csv_creates_output_and_optimizes(self):
        optimize_csv(self.sample_input_csv, self.sample_output_csv)
        self.assertTrue(os.path.exists(self.sample_output_csv))

        # Instruct read_csv to parse the 'Timestamp_Str' column as dates
        df_loaded = pd.read_csv(self.sample_output_csv, parse_dates=['Timestamp_Str'])

        # After re-reading from CSV:
        # - Category columns will be 'object' as CSV doesn't store 'category' dtype.
        # - Float columns will typically be 'float64' by default by read_csv.
        # - Int columns will typically be 'int64' by default by read_csv.
        # - Datetime columns if in ISO format are often correctly inferred.
        self.assertEqual(df_loaded['Category'].dtype, 'object')
        self.assertEqual(df_loaded['Value_Float'].dtype, 'float64')
        self.assertEqual(df_loaded['Value_Int'].dtype, 'int64')
        self.assertEqual(df_loaded['Timestamp_Str'].dtype, 'datetime64[ns]') # pandas read_csv is good at parsing this

        log_output = self.log_stream_csv_test.getvalue()
        self.assertIn("Original memory usage:", log_output)
        self.assertIn("Optimized memory usage:", log_output)
        self.assertIn("Successfully read CSV from 'sample_input_for_test.csv'", log_output)
        self.assertIn("Successfully saved optimized CSV to 'sample_output_for_test.csv'", log_output)
        self.assertIn("INFO", log_output) # Check log level

if __name__ == '__main__':
    unittest.main()
