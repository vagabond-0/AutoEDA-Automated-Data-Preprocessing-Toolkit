import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimizes the data types of columns in a Pandas DataFrame.

    Args:
        df: The input DataFrame.

    Returns:
        The DataFrame with optimized data types.
    """
    df_optimized = df.copy()

    for col in df_optimized.columns:
        col_type = df_optimized[col].dtype

        if col_type == 'object':
            # Attempt to convert columns with 'date', 'time', or 'timestamp' in their names to datetime FIRST
            if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp']):
                try:
                    df_optimized[col] = pd.to_datetime(df_optimized[col])
                    logging.info(f"Column '{col}' converted to datetime.")
                except ValueError:
                    logging.warning(f"Could not convert column '{col}' to datetime. It might not be a valid date/time format.")
                except Exception as e:
                    logging.error(f"Error converting column '{col}' to datetime: {e}")
            # Then, if not converted to datetime, try converting to 'category' if nunique < 50
            elif df_optimized[col].nunique() < 50 and df_optimized[col].dtype == 'object': # check dtype again in case it was converted by previous step
                try:
                    df_optimized[col] = df_optimized[col].astype('category')
                    logging.info(f"Column '{col}' converted to category.")
                except Exception as e:
                    logging.error(f"Error converting column '{col}' to category: {e}")

        # Downcast float64 columns to float32
        elif col_type == 'float64':
            try:
                df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
                logging.info(f"Column '{col}' downcasted to float32.")
            except Exception as e:
                logging.error(f"Error downcasting column '{col}' to float32: {e}")

        # Downcast int64 columns to the smallest possible integer subtype
        elif col_type == 'int64':
            try:
                df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
                logging.info(f"Column '{col}' downcasted to smallest possible integer subtype.")
            except Exception as e:
                logging.error(f"Error downcasting column '{col}' to smaller integer: {e}")

    return df_optimized


def optimize_csv(input_path: str, output_path: str) -> None:
    """
    Reads a CSV, optimizes its data types, and saves it to a new CSV.

    Args:
        input_path: Path to the input CSV file.
        output_path: Path to save the optimized CSV file.
    """
    try:
        df = pd.read_csv(input_path)
        logging.info(f"Successfully read CSV from '{input_path}'.")
    except FileNotFoundError:
        logging.error(f"Error: Input CSV file not found at '{input_path}'.")
        return
    except Exception as e:
        logging.error(f"Error reading CSV from '{input_path}': {e}")
        return

    original_memory_usage = df.memory_usage(deep=True).sum()
    logging.info(f"Original memory usage: {original_memory_usage / (1024 * 1024):.2f} MB")

    df_optimized = optimize_dtypes(df)

    optimized_memory_usage = df_optimized.memory_usage(deep=True).sum()
    logging.info(f"Optimized memory usage: {optimized_memory_usage / (1024 * 1024):.2f} MB")
    logging.info(f"Memory usage reduced by {original_memory_usage - optimized_memory_usage} bytes ({(original_memory_usage - optimized_memory_usage) / original_memory_usage * 100:.2f}%).")

    try:
        df_optimized.to_csv(output_path, index=False)
        logging.info(f"Successfully saved optimized CSV to '{output_path}'.")
    except Exception as e:
        logging.error(f"Error saving optimized CSV to '{output_path}': {e}")
