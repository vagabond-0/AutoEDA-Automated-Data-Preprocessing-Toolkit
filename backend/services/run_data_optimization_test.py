import pandas as pd
import logging
import os
import sys

# Add the autoeda directory to the Python path
# This is needed to import the optimize_data function
# Assuming the script is in backend/services and autoeda is at the root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from autoeda.notebook_data_optimization import optimize_data

def setup_logging(log_file_path):
    """Configures logging to file and console."""
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    # Log confirmation of file handler setup
    # This initial log might go to console if stream handler is added first or if not configured yet for file
    # For it to reliably go to file, it needs to be after addHandler, but let's see
    # We will get a specific logger for this initial message.
    init_logger = logging.getLogger("init_setup")
    init_logger.info(f"FileHandler configured for {log_file_path}. Stream: {file_handler.stream}")


    # Add stream handler (for console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)

    return file_handler # Return file_handler to be closed later

def main():
    # Define file paths
    input_csv_path = os.path.join(project_root, 'backend', 'output', 'sample_input_for_optimization.csv')
    output_csv_path = os.path.join(project_root, 'backend', 'output', 'optimized_sample_output.csv')
    log_file_path = os.path.join(project_root, 'backend', 'output', 'data_optimization_run.txt')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Setup logging for this script and get the file handler
    file_handler_to_close = setup_logging(log_file_path)
    
    logger = logging.getLogger(__name__) # Get a logger for the current module

    logger.info(f"Script started. Input CSV: {input_csv_path}, Output CSV: {output_csv_path}, Log File: {log_file_path}")

    # Check if input CSV exists
    if not os.path.exists(input_csv_path):
        logger.error(f"Input CSV file not found at {input_csv_path}")
        return

    try:
        # Load the sample CSV
        logger.info(f"Loading data from {input_csv_path}")
        df = pd.read_csv(input_csv_path)
        logger.info("Data loaded successfully.")
        logger.info(f"Original memory usage: {df.memory_usage(deep=True).sum()} bytes")
        logger.info("Original dtypes:\n%s", df.dtypes)

        # Call the optimize_data function
        logger.info("Optimizing data...")
        df_optimized = optimize_data(df.copy()) # Use .copy() if optimize_data modifies inplace
        logger.info("Data optimization complete.")
        logger.info(f"Optimized memory usage: {df_optimized.memory_usage(deep=True).sum()} bytes")
        logger.info("Optimized dtypes:\n%s", df_optimized.dtypes)


        # Save the optimized DataFrame
        logger.info(f"Saving optimized data to {output_csv_path}")
        df_optimized.to_csv(output_csv_path, index=False)
        logger.info("Optimized data saved successfully.")

    except FileNotFoundError:
        logger.error(f"Error: The file {input_csv_path} was not found.")
    except pd.errors.EmptyDataError:
        logger.error(f"Error: The file {input_csv_path} is empty.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

    logger.info("Script finished.")

    if file_handler_to_close:
        logger.info(f"Closing log file handler for {file_handler_to_close.baseFilename}")
        file_handler_to_close.close()

if __name__ == '__main__':
    main()
