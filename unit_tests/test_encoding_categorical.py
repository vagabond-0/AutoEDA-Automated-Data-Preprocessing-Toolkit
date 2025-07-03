import pytest
import pandas as pd
import os

from autoeda.encoding_categorical import label_encode, one_hot_encode


def test_label_encode_object_columns(tmp_path):
    df = pd.DataFrame({
        "color": ["red", "green", "blue", "green"],
        "size": ["S", "M", "L", "M"]
    })
    result = label_encode(df, ["color", "size"])
    assert result["color"].dtype == "int32" or result["color"].dtype == "int64"
    assert result["size"].dtype == "int32" or result["size"].dtype == "int64"
    assert set(result["color"].unique()) == {0, 1, 2}

def test_label_encode_skips_numeric_column(caplog):
    df = pd.DataFrame({
        "color": ["red", "green", "blue"],
        "price": [10, 20, 30]
    })
    result = label_encode(df, ["price"])
    # Should skip and keep it unchanged
    assert result["price"].equals(df["price"])
    # Log should mention skipping
    assert any("Skipped column (non-object dtype)" in message for message in caplog.text.splitlines())

def test_label_encode_invalid_column():
    df = pd.DataFrame({"brand": ["A", "B", "C"]})
    with pytest.raises(KeyError):
        label_encode(df, ["nonexistent_column"])

def test_one_hot_encode_basic():
    df = pd.DataFrame({
        "color": ["red", "green", "blue"],
        "size": ["S", "M", "L"]
    })
    result = one_hot_encode(df, ["color"])
    expected_columns = {"size", "color_blue", "color_green", "color_red"}
    assert expected_columns.issubset(set(result.columns))
    assert "color" not in result.columns

def test_one_hot_encode_multiple_columns():
    df = pd.DataFrame({
        "color": ["red", "green", "blue"],
        "size": ["S", "M", "S"]
    })
    result = one_hot_encode(df, ["color", "size"])
    assert "color" not in result.columns
    assert "size" not in result.columns
    assert all(any(col.startswith(prefix) for col in result.columns) for prefix in ["color_", "size_"])

def test_one_hot_encode_invalid_column():
    df = pd.DataFrame({"brand": ["Nike", "Adidas", "Puma"]})
    with pytest.raises(KeyError):
        one_hot_encode(df, ["nonexistent_column"])
