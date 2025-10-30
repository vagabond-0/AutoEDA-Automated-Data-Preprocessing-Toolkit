import os
import json
import pandas as pd
import numpy as np
import pytest
from autoeda.feat_scaling import process_scaling

@pytest.fixture
def sample_df():
    # DataFrame with numeric, binary, and NaN values
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, np.nan, 40, 50],
        'C': [1, 1, 0, 0, 1],  # binary, should be ignored
        'D': [np.nan, np.nan, np.nan, 1, 2],  #  too many NaNs, should be ignored
        'E': [100, 200, 300, 400, 500]
    })

def test_output_files_created(tmp_path, sample_df):
    output_dir = tmp_path / "output"
    process_scaling(sample_df, output_dir=str(output_dir))

    scaled_path = output_dir / "autoEDA_scaled_output.csv"
    report_path = output_dir / "scaling_report.json"

    assert scaled_path.exists()
    assert report_path.exists()

def test_scaling_report_content(tmp_path, sample_df):
    output_dir = tmp_path / "output"
    process_scaling(sample_df, output_dir=str(output_dir))

    report_path = output_dir / "scaling_report.json"
    with open(report_path) as f:
        report = json.load(f)

    # Only columns 'A', 'B', 'E' should be present (non-binary, <50% NaN)
    assert set(report.keys()) == {'A', 'B', 'E'}
    assert all(v in ['StandardScaler', 'MinMaxScaler', 'RobustScaler'] for v in report.values())

def test_scaled_output_shape(tmp_path, sample_df):
    output_dir = tmp_path / "output"
    process_scaling(sample_df, output_dir=str(output_dir))

    scaled_path = output_dir / "autoEDA_scaled_output.csv"
    scaled_df = pd.read_csv(scaled_path)

    # Only columns 'A', 'B', 'E' should be present
    assert list(scaled_df.columns) == ['A', 'B', 'E']
    assert scaled_df.shape == (5, 3)

def test_handles_all_nan_column(tmp_path):
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [np.nan, np.nan, np.nan, np.nan, np.nan]
    })
    output_dir = tmp_path / "output"
    process_scaling(df, output_dir=str(output_dir))

    scaled_path = output_dir / "autoEDA_scaled_output.csv"
    scaled_df = pd.read_csv(scaled_path)
    # Only 'A' should be present
    assert list(scaled_df.columns) == ['A']

def test_no_numeric_columns(tmp_path):
    df = pd.DataFrame({
        'X': ['a', 'b', 'c'],
        'Y': ['foo', 'bar', 'baz']
    })
    output_dir = tmp_path / "output"
    process_scaling(df, output_dir=str(output_dir))

    scaled_path = output_dir / "autoEDA_scaled_output.csv"
    report_path = output_dir / "scaling_report.json"

    
    assert scaled_path.exists()
    assert report_path.exists()

    
    with open(report_path, 'r') as f:
        report = json.load(f)
    assert report == {}

    # Assert the scaled CSV file is essentially empty (no data rows, maybe just a header or empty)
    # Reading as text is safer than pd.read_csv for this case.
    with open(scaled_path, 'r') as f:
        content = f.read().strip() 
    assert content == "" 