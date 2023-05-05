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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///luna.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

cloudinary.config(
            cloud_name='dexc98myq',
            api_key='872169569198661',
            api_secret='AC9O0BiDuGNyfF5iipr-cBl9Gvo'
        )
# user  routes

@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(users=user_list)

@app.route('/user/<int:user_id>', methods=["GET"])
def user_profile(user_id):
    profile = db.session.query(User).get(user_id)
    if profile:
        return jsonify(profile.to_dict())
    else:
        return jsonify({'error': 'Profile not found.'}), 404



@app.route('/users/register', methods=["POST"])
def register_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    profile = request.json['profile']
    
    if 'name' not in request.json:
     return jsonify({'error': 'Name field is missing.'}), 400
    if 'email' not in request.json:
     return jsonify({'error': 'Email field is missing.'}), 400
    if 'password' not in request.json:
     return jsonify({'error': 'Password field is missing.'}), 400
    if 'profile' not in request.json:
     return jsonify({'error': 'Profile field is missing.'}), 400

    # upload profile image
    result =  cloudinary.uploader.upload(profile)
    profileImageUrl = result['secure_url']
    print(profileImageUrl)
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create a new user with the hashed password
    new_user = User(name=name, email=email, password=hashed_password, profile=profileImageUrl)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User added successfully.', 'user': new_user.to_dict()}), 201


@app.route('/users/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'message': 'Login successful.', 'user': user.to_dict()})
    else:
        return jsonify({'error': 'Invalid email or password.'}), 401


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.query(User).get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'user deleted successfully.'})
    else:
        return jsonify({'error': 'user not found.'}), 404

@app.route('/users/<int:id>', methods=['PUT'])
def update_user_info(id):
    user = db.session.query(User).get(id)
    if user:
       user.name = request.json['name']
       user.profile = request.json['profile']
       user.email = request.json['email']
       db.session.commit()
       return jsonify({'message': 'user updated successfully.', 'user': user.to_dict()})
    else:
        return jsonify({'error': 'user not found.'}), 404



if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)