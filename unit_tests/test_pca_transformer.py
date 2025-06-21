

import pytest
import pandas as pd
import numpy as np
from autoeda.pca_transformer import apply_pca  # Adjust path if needed

@pytest.fixture
def dummy_df():
    """Fixture to provide a reproducible dummy DataFrame with numeric features."""
    np.random.seed(42)
    return pd.DataFrame({
        "feature1": np.random.rand(10),
        "feature2": np.random.rand(10),
        "feature3": np.random.rand(10)
    })

def test_standard_pca_shape(dummy_df):
    """Test that PCA returns the correct shape when all components are used."""
    transformed_df, meta = apply_pca(dummy_df)
    assert transformed_df.shape == dummy_df.shape
    assert meta["n_components"] == dummy_df.shape[1]

def test_metadata_integrity(dummy_df):
    """Check that the metadata dictionary contains accurate and expected fields."""
    _, meta = apply_pca(dummy_df)
    assert "explained_variance_ratio" in meta
    assert isinstance(meta["explained_variance_ratio"], list)
    assert len(meta["explained_variance_ratio"]) == dummy_df.shape[1]
    assert meta["original_columns"] == ["feature1", "feature2", "feature3"]
    assert meta["pca_columns"] == [f"PC{i+1}" for i in range(dummy_df.shape[1])]

def test_variance_sum_close_to_1(dummy_df):
    """Verify that the total explained variance is approximately 1 for full components."""
    _, meta = apply_pca(dummy_df)
    total_variance = sum(meta["explained_variance_ratio"])
    assert np.isclose(total_variance, 1.0, atol=1e-5)

def test_reduced_components(dummy_df):
    """Test PCA with fewer components than total features."""
    transformed_df, meta = apply_pca(dummy_df, n_components=2)
    assert transformed_df.shape[1] == 2
    assert meta["n_components"] == 2
    assert len(meta["explained_variance_ratio"]) == 2
    assert meta["pca_columns"] == ["PC1", "PC2"]

def test_edge_case_more_components_than_features(dummy_df):
    """Test that PCA raises an error if requested components exceed number of features."""
    with pytest.raises(ValueError):
        apply_pca(dummy_df, n_components=5)  # dummy_df has only 3 features
