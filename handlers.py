from flask import Flask, jsonify, request
from models import db, User
from flask_cors import CORS
import bcrypt
import cloudinary
import cloudinary.uploader



app = Flask(__name__)
CORS(app)  # Apply CORS settings to the Flask app

@app.after_request
def add_cors_headers(response):
    # Add CORS headers to the response
    response.headers.add('Access-Control-Allow-Origin', '*') # Allow requests from this origin
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization') # Allow specific headers
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE') # Allow specific HTTP methods
    return response
# Configure the database connection settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oasis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

cloudinary.config(
            cloud_name='dexc98myq',
            api_key='872169569198661',
            api_secret='AC9O0BiDuGNyfF5iipr-cBl9Gvo'
        )
# user  routes





if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)