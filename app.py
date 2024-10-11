from flask import Flask, request, jsonify 
import os
from dotenv import load_dotenv
import pymysql
from pymysql.err import MySQLError
import jwt
import datetime
import bcrypt
from functools import wraps


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except MySQLError as e:
        return None


def token_required(func):
    def wrapper(*args, **kwargs):

        try:
            token = None

            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            user_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = user_data["user_id"]
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return func(user_id, *args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper
    

@app.route("/posts/add", methods=['POST'])
@token_required
def add_post(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error" : "Database connection failed"}), 500
    
    content = request.json.get("content")
    if not content:
        return jsonify({"error" : "required Element is not Found"}), 400
    
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO posts(content, user_id) VALUES (\'{}\', {})".format(content, user_id)
            cursor.execute(query)
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({'error': "Oops! Something went wrong during post create"}), 400

        return jsonify({"message": "Post added"}), 201
    
    except MySQLError as e:
        return jsonify({"error": "general error: {}".format(e)}), 500
    finally:
        conn.close()


@app.route('/posts/<int:id>', methods =['GET'])
def get_post(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error" : "Database connection failed"}), 500
    
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM posts WHERE id={}".format(id)
            cursor.execute(query)
            post = cursor.fetchone()
            if post is None:
                return jsonify({'error': 'Post not found'}), 404
            
            return jsonify({"data" : post}), 200
        
    except MySQLError as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()


@app.route('/posts/<int:id>/update', methods=['PUT'])
@token_required
def update_post(user_id, id):
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error" : "Database connection failed"}), 500
    
    content = request.json.get("content")
    if not content:
        return jsonify({"error" : "required Element is not send"}), 400

    try:
        with conn.cursor() as cursor:

            cursor.execute("SELECT * FROM posts WHERE id={}".format(id))
            post = cursor.fetchone()
            if post is None:
                return jsonify({'error': 'Post not found'}), 404
            
            query = "UPDATE posts SET content=\'{}\' WHERE id={}".format(content, id)
            cursor.execute(query)
            conn.commit()
            
        return jsonify({"data" : "post is updated"}), 200

    except MySQLError as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()


@app.route('/posts/<int:id>/delete', methods=['DELETE'])
@token_required
def delete_post(user_id, id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error" : "Database connection failed"}), 500
    
    try:
        with conn.cursor() as cursor:

            cursor.execute("SELECT * FROM posts WHERE id={}".format(id))
            post = cursor.fetchone()
            if post is None:
                return jsonify({'error': 'Post not found'}), 404

            query = "DELETE FROM posts WHERE id={}".format(id)
            cursor.execute(query)
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({'error': "Oops! Something went wrong during post create"}), 400

        return jsonify({'message': 'Post deleted'}), 200

    except MySQLError as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()


@app.route("/register", methods=['POST'])
def register():

    conn = get_db_connection()
    if conn is None:
       return jsonify({"error" : "Database connection failed"}), 500

    data = request.json
    if not data:
        return jsonify({"error" : "required Element is not found"}), 400

    try:
        with conn.cursor() as cursor:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if not username or not email or not password:
                return jsonify({"error" : "required Element is not found"}), 400

            query = "INSERT INTO users(username, email, password) VALUES(\'{}\', \'{}\', \'{}\')".format(username, email, hashed_password)
            cursor.execute(query)
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({'error': "Oops! Something went wrong during registration"}), 404
            
            return jsonify({'message': 'Thank you for registering! Your account has been created successfully.'}), 201
        
    except MySQLError as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()


@app.route("/login", methods=['POST'])
def login():

    conn = get_db_connection()
    if conn is None:
       return jsonify({"error" : "Database connection failed"}), 500

    data = request.json
    if not data:
        return jsonify({"error" : "required Element is not send"}), 400

    try:
        with conn.cursor() as cursor:
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"error" : "required Element is not found"}), 400

            query = "SELECT * from users WHERE username=\'{}\'".format(username)
            cursor.execute(query)
            
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result["password"].encode('utf-8')):
                token = jwt.encode({'user_id': result["id"], 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)},
                           app.config['SECRET_KEY'], algorithm='HS256')
                
                return jsonify({'token': token}), 200
            
            else:
                return jsonify({'message': 'Invalid credentials!'}), 401
        
    except MySQLError as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)