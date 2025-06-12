from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import chardet
import re
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import timedelta
import uuid
import os 

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/autoeda")
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()
users_collection = db.users

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://auto-eda-automated-data-preprocessing-toolkit.vercel.app"
]

CORS(app, resources={
    r"/upload": {"origins": ALLOWED_ORIGINS},
    r"/login": {"origins": ALLOWED_ORIGINS},
    r"/signup": {"origins": ALLOWED_ORIGINS},
    r"/me": {"origins": ALLOWED_ORIGINS},
}, supports_credentials=True)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not any(c.isalpha() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'status': 'error', 'message': 'Email and password required'}), 400
    
    email = data['email'].lower()
    password = data['password']
    
    if not is_valid_email(email):
        return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
    
    if not is_strong_password(password):
        return jsonify({'status': 'error', 'message': 'Password must be at least 8 characters and contain both letters and numbers'}), 400
    
    if users_collection.find_one({'email': email}):
        return jsonify({'status': 'error', 'message': 'Email already registered'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = {
        'user_id': str(uuid.uuid4()),
        'email': email,
        'password': hashed_password,
        'created_at': pd.Timestamp.now().isoformat()
    }
    
    users_collection.insert_one(new_user)
    
    return jsonify({
        'status': 'success',
        'message': 'User registered successfully'
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'status': 'error', 'message': 'Email and password required'}), 400
    
    email = data['email'].lower()
    password = data['password']
    
    user = users_collection.find_one({'email': email})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=user['user_id'])
    
    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'token': access_token,
        'user': {
            'email': user['email'],
            'user_id': user['user_id']
        }
    }), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({
        'status': 'success',
        'message': 'Logged out successfully'
    }), 200


@app.route('/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get the current user's profile"""
    current_user_id = get_jwt_identity()
    
    user = users_collection.find_one({'user_id': current_user_id}, {'password': 0})  # Exclude password
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    user['_id'] = str(user['_id'])
    
    return jsonify({
        'status': 'success',
        'user': user
    }), 200


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
