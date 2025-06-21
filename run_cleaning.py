from autoeda.null_handler import process_csv

process_csv(
    input_path="notebooks/sample_csv/sample_input.csv",
    output_path="backend/output/cleaned_sample_input.csv"
)


process_csv(
    input_path="notebooks/sample_csv/titanic.csv",
    output_path="backend/output/cleaned_titanic.csv"
)
