import pandas as pd
import numpy as np
import os
from typing import Dict, Callable
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')



# --------------*NULL HANDLING STRATEGIES*------------------


def drop_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Drop all rows containing any null values."""
    return df.dropna()

def replace_with_fixed(df: pd.DataFrame, value=0) -> pd.DataFrame:
    """Replace all nulls with a fixed value (default: 0)."""
    return df.fillna(value)

def replace_with_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Replace nulls in numeric columns with column means."""
    df_filled = df.copy()
    for col in df_filled.select_dtypes(include=[np.number]):
        df_filled[col].fillna(df_filled[col].mean(), inplace=True)
    return df_filled

def replace_with_median(df: pd.DataFrame) -> pd.DataFrame:
    """Replace nulls in numeric columns with column medians."""
    df_filled = df.copy()
    for col in df_filled.select_dtypes(include=[np.number]):
        df_filled[col].fillna(df_filled[col].median(), inplace=True)
    return df_filled

def replace_with_mode(df: pd.DataFrame) -> pd.DataFrame:
    """Replace nulls with the most frequent value per column."""
    df_filled = df.copy()
    for col in df.columns:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df_filled[col].fillna(mode_val.iloc[0], inplace=True)
            elif df[col].dtype in ['object', 'category']:
                df_filled[col].fillna("Unknown", inplace=True)
            else:
                df_filled[col].fillna(0, inplace=True)
    return df_filled

def forward_fill(df: pd.DataFrame) -> pd.DataFrame:
    """Fill nulls with previous valid value (forward fill)."""
    return df.ffill()

def backward_fill(df: pd.DataFrame) -> pd.DataFrame:
    """Fill nulls with next valid value (backward fill)."""
    return df.bfill()



# -----------------------*EVALUATION & STRATEGY SELECTION*----------------------------------------------


def evaluate_methods(original_df: pd.DataFrame, cleaned_versions: Dict[str, pd.DataFrame]) -> str:
    """
    Evaluate methods based on:
    - % of nulls eliminated
    - Shape retention
    - Return the name of the best method
    """
    original_nulls = original_df.isnull().sum().sum()
    original_shape = original_df.shape
    best_score = float("-inf")
    best_method = None

    for name, df in cleaned_versions.items():
        remaining_nulls = df.isnull().sum().sum()
        nulls_removed = original_nulls - remaining_nulls
        row_ratio = df.shape[0] / original_shape[0] if original_shape[0] else 0
        col_ratio = df.shape[1] / original_shape[1] if original_shape[1] else 0

        score = (
            (nulls_removed / original_nulls if original_nulls > 0 else 1.0) * 0.5
            + row_ratio * 0.25
            + col_ratio * 0.25
        )

        logging.info(f"Method: {name}, Score: {score:.4f}, Nulls Remaining: {remaining_nulls}, Shape: {df.shape}")
        
        if score > best_score:
            best_score = score
            best_method = name

    return best_method



#--------------------------* MAIN ENTRYPOINT *-----------------------------------------


def process_csv(input_path: str, output_path: str) -> None:
    """
    Pipeline to read CSV, apply strategies, evaluate, and save best-cleaned version.
    """
    if not os.path.exists(input_path):
        logging.error(f"Input file not found: {input_path}")
        return

    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        return

    if df.empty:
        logging.warning("Input CSV is empty. No processing done.")
        return

    logging.info(f"Input CSV loaded: {input_path}")
    logging.info(f"Initial Shape: {df.shape}, Null Count: {df.isnull().sum().sum()}")

    strategies: Dict[str, Callable[[pd.DataFrame], pd.DataFrame]] = {
        "drop_nulls": drop_nulls,
        "replace_with_fixed": lambda d: replace_with_fixed(d, 0),
        "replace_with_mean": replace_with_mean,
        "replace_with_median": replace_with_median,
        "replace_with_mode": replace_with_mode,
        "forward_fill": forward_fill,
        "backward_fill": backward_fill,
    }

    cleaned_versions = {name: func(df.copy()) for name, func in strategies.items()}

    best_method = evaluate_methods(df, cleaned_versions)
    best_df = cleaned_versions[best_method]

    logging.info(f"Best strategy selected: {best_method}")
    logging.info(f"Cleaned Data Shape: {best_df.shape}, Nulls Remaining: {best_df.isnull().sum().sum()}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    best_df.to_csv(output_path, index=False)

    logging.info(f"Cleaned CSV saved at: {output_path}")
