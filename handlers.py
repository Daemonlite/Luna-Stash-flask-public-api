from flask import Flask, jsonify, request
from models import db, User,Posts,Comments,Photos,Todos
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
    print(len(users))
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


# post routes
@app.route('/posts', methods=['GET'])
def get_posts():
    all_posts = Posts.query.all()
    result = []
    for post in all_posts:
        result.append(post.to_dict())
    print(len(all_posts))
    return jsonify(result)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Posts.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'})
    return jsonify(post.to_dict())

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Posts(user_id=data['user_id'], title=data['title'], body=data['body'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'})

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = db.session.query(Posts).get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'})
    data = request.get_json()
    post.user_id = data['user_id']
    post.title = data['title']
    post.body = data['body']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = db.session.query(Posts).get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'})
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})


#comment routes 

@app.route('/comments', methods=['POST'])
def create_comment():
    post_id = request.json['post_id']
    username = request.json['username']
    userprofile = request.json['userprofile']
    content = request.json['content']
    comment = Comments(post_id=post_id, username=username, userprofile=userprofile, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict())

@app.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    comment = db.session.query(Comments).get(id)
    comment.post_id = request.json.get('post_id', comment.post_id)
    comment.username = request.json.get('username', comment.username)
    comment.userprofile = request.json.get('userprofile', comment.userprofile)
    comment.content = request.json.get('content', comment.content)
    db.session.commit()
    return jsonify(comment.to_dict())

@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = db.session.query(Comments).get(id)
    db.session.delete(comment)
    db.session.commit()
    return '', 204

@app.route('/comments/<int:id>',methods=['GET'])
def get_comment(id):
    comment = db.session.query(Comments).get(id)
    return jsonify(comment.to_dict())

@app.route('/comments',methods=['GET'])
def get_comments():
    comments = Comments.query.all()
    return jsonify([comment.to_dict() for comment in comments])


@app.route('/photos',methods=['GET'])
def get_Photos():
    images = Photos.query.all()
    image_list = [img.to_dict() for img in images]
    print(len(images))
    return jsonify(photos=image_list)



# Define the routes
@app.route('/photos', methods=['GET'])
def get_photos():
   photos = Photos.query.all()
   return jsonify([photo.to_dict() for photo in photos])

@app.route('/photos/<int:id>', methods=['GET'])
def get_photo(id):
   photo = db.session.query(Photos).get(id)
   return jsonify(photo.to_dict())

@app.route('/photos', methods=['POST'])
def create_photo():
   data = request.get_json()
   photo = Photos(descr=data['descr'], image_url=data['image_url'])
   db.session.add(photo)
   db.session.commit()
   return jsonify(photo.to_dict()), 201

@app.route('/photos/<int:id>', methods=['PUT'])
def update_photo(id):
   photo = db.session.query(Photos).get(id)
   data = request.get_json()
   photo.descr = data.get('descr', photo.descr)
   photo.image_url = data.get('image_url', photo.image_url)
   db.session.commit()
   return jsonify(photo.to_dict())

@app.route('/photos/<int:id>', methods=['DELETE'])
def delete_photo(id):
   photo = Photos.query.get_or_404(id)
   db.session.delete(photo)
   db.session.commit()
   return '', 204

#Todos

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    user_id = data['user_id']
    task = data['task']
    completed = data.get('completed', False)

    todo = Todos(user_id=user_id, task=task, completed=completed)
    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_dict()), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todos.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# Get Todo by ID
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    todo = Todos.query.get_or_404(id)
    return jsonify(todo.to_dict())

# Update Todo by ID
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo_by_id(id):
    todo = Todos.query.get_or_404(id)
    data = request.json
    todo.task = data.get('task', todo.task)
    todo.completed = data.get('completed', todo.completed)
    db.session.commit()
    return jsonify(todo.to_dict())

# Delete Todo by ID
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo_by_id(id):
    todo = Todos.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)