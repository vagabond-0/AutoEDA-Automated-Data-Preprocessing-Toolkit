from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import chardet
app = Flask(__name__)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://auto-eda-automated-data-preprocessing-toolkit.vercel.app"
]

CORS(app, resources={r"/upload": {"origins": ALLOWED_ORIGINS}}, supports_credentials=True)

@app.route('/')
def home():
    return "Welcome to the AutoEDA Backend API!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    filename = file.filename
    if not filename.lower().endswith(".csv"):
        return jsonify({'status':"error",'error': "Only CSV files can be uploaded"}), 400
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    save_path = f"./uploaded_files/{filename}"
    file.seek(0)
    file.save(save_path)
    file.seek(0)

    try:
        df = pd.read_csv(file, encoding=encoding)
        return jsonify({ "status": "success", "filename": filename,'message': 'File processed successfully!', "preview": df.head(5).to_dict(), "columns": df.columns.tolist(),"shape": df.shape}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
