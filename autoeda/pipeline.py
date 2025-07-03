"""
pipeline.py: Outlier Processing Pipeline for AutoEDA

This module provides a high-level function to orchestrate outlier detection, flagging, capping, and removal using the logic from outliers.py. It is designed for integration with CLI, backend, or notebook workflows.
"""

import os
import pandas as pd


def run_outlier_pipeline(scaled_csv_path, output_dir):
    """
    Run the full outlier processing pipeline on a scaled dataset.

    Parameters
    ----------
    scaled_csv_path : str
        Path to the scaled CSV file (input dataset).
    output_dir : str
        Directory to store all output files (flagged, capped, removed datasets, and reports).

    Returns
    -------
    dict
        Dictionary containing:
            - 'flagged_csv': Path to flagged dataset
            - 'capped_csv': Path to capped dataset
            - 'removed_csv': Path to dataset with outliers removed
            - 'summary_report_json': Path to outlier summary report (JSON)
            - 'summary_report_csv': Path to outlier summary report (CSV)
            - 'outlier_stats': Outlier statistics/metadata (dict)

    Raises
    ------
    FileNotFoundError: If the input file does not exist.
    ValueError: If the input file is malformed or cannot be loaded.

    Example
    -------
    >>> result = run_outlier_pipeline('output-files/autoEDA_scaled_output.csv', 'output-files/outlier_results')
    >>> print(result['flagged_csv'])
    """
    if not os.path.isfile(scaled_csv_path):
        raise FileNotFoundError(f"Input file not found: {scaled_csv_path}")

    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_csv(scaled_csv_path)
    except Exception as e:
        raise ValueError(f"Failed to load input CSV: {e}")

    # Call the main orchestration function from the refactored outliers.py
    # outliers.process_outliers now handles saving files and returns paths and summary.
    # Import here to avoid circular dependency if outliers.py also imports pipeline.
    from autoeda import outliers
    outlier_processing_results = outliers.process_outliers(df, output_dir)

    # The process_outliers function already saves the files.
    # We just need to return the paths and summary provided by it.
    # The keys in outlier_processing_results['paths'] are:
    # 'flagged_csv', 'capped_csv', 'removed_csv', 'report_json', 'summary_csv'
    # The key in outlier_processing_results['summary'] is the summary dict itself.

    return {
        'flagged_csv': outlier_processing_results['paths']['flagged_csv'],
        'capped_csv': outlier_processing_results['paths']['capped_csv'],
        'removed_csv': outlier_processing_results['paths']['removed_csv'],
        'summary_report_json': outlier_processing_results['paths']['report_json'],
        'summary_report_csv': outlier_processing_results['paths']['summary_csv'],
        'outlier_stats': outlier_processing_results.get('summary', {})
    }


def run_pca_pipeline(input_csv_path, output_dir, n_components=None):
    """
    Run the PCA transformation pipeline.

    Parameters
    ----------
    input_csv_path : str
        Path to the input CSV file.
    output_dir : str
        Directory to store all output files.
    n_components : int, optional
        Number of principal components to keep. If None, all components are retained.

    Returns
    -------
    dict
        Dictionary containing:
            - 'pca_transformed_csv': Path to the transformed dataset.
            - 'pca_summary': Path to the PCA summary report (JSON).

    Raises
    ------
    FileNotFoundError: If the input file does not exist.
    ValueError: If the input file is malformed or cannot be loaded.
    """
    if not os.path.isfile(input_csv_path):
        raise FileNotFoundError(f"Input file not found: {input_csv_path}")

    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_csv(input_csv_path)
    except Exception as e:
        raise ValueError(f"Failed to load input CSV: {e}")

    from autoeda.pca_transformer import apply_pca  # Import here to avoid circular dependency
    import json
    import logging

    # --- Simplified logger setup for PCA to test file creation ---
    log_file_path = os.path.join(output_dir, 'pca_pipeline.log')

    # Ensure any previous handlers for the root logger are removed if we are re-configuring.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Attempting with force=True for Python 3.8+
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
            filename=log_file_path,
            filemode='a',  # 'a' to append
            force=True
        )
    except TypeError:  # Fallback for Python < 3.8 where force is not an argument
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
            filename=log_file_path,
            filemode='a'
        )
    # --- End of simplified logger setup ---

    logging.info(f"Starting PCA transformation for {input_csv_path}...")  # Using the root logger
    transformed_df, metadata = apply_pca(df, n_components=n_components)

    pca_transformed_csv = os.path.join(output_dir, 'pca_transformed.csv')
    transformed_df.to_csv(pca_transformed_csv, index=False)
    logging.info(f"Transformed data saved to: {pca_transformed_csv}")

    pca_summary_path = os.path.join(output_dir, 'pca_summary.json')
    with open(pca_summary_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logging.info(f"PCA summary saved to: {pca_summary_path}")

    logging.info("PCA transformation completed.")

    return {
        'pca_transformed_csv': pca_transformed_csv,
        'pca_summary': pca_summary_path,
        'pca_log_file': log_file_path
    }


if __name__ == "__main__":
    # Example usage of the outlier pipeline
    # Ensure you have a scaled CSV file at this path or change it accordingly
    sample_scaled_csv = 'backend/output/autoEDA_outliers_removed.csv'  # Replace with your actual scaled data path
    outlier_output_directory = 'backend/output/outlier_pipeline_results'

    # Create a dummy input file if it doesn't exist for example purposes
    if not os.path.exists(sample_scaled_csv):
        os.makedirs(os.path.dirname(sample_scaled_csv), exist_ok=True)
        dummy_df = pd.DataFrame({'A': [1, 2, 3, 100], 'B': [4, 5, 6, 200], 'C': [7, 8, 9, 300]})
        dummy_df.to_csv(sample_scaled_csv, index=False)
        print(f"Created dummy input file: {sample_scaled_csv}")


    print(f"Running outlier pipeline with input: {sample_scaled_csv} and output dir: {outlier_output_directory}")
    outlier_results = run_outlier_pipeline(sample_scaled_csv, outlier_output_directory)
    print("Outlier pipeline completed. Results:")
    for key, value in outlier_results.items():
        print(f"  {key}: {value}")

    print("\n" + "="*50 + "\n")

    # Example usage of the PCA pipeline
    # This will use the output of the outlier removal, or the dummy file created above
    input_for_pca = outlier_results.get('removed_csv', sample_scaled_csv)
    pca_output_directory = 'backend/output/pca_pipeline_results'

    print(f"Running PCA pipeline with input: {input_for_pca} and output dir: {pca_output_directory}")
    pca_results = run_pca_pipeline(input_for_pca, pca_output_directory, n_components=2)  # Example: retain 2 components
    print("PCA pipeline completed. Results:")
    for key, value in pca_results.items():
        print(f"  {key}: {value}")
    if 'pca_log_file' in pca_results:
        print(f"  PCA logs saved to: {pca_results['pca_log_file']}")