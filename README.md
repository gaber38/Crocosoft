Welcome to the Simple Newsfeed App repository!

Features
The application includes the following core entities and functionalities:

- User: Users can register, log in, and manage their profiles.
- Post: Users can create, update, delete, and retrieve posts.
- Comment: Users can comment on posts.
- Like: Users can like posts.
- Share: Users can share posts with others.
- Follow/Friendships: Users can follow each other and manage friendships.

Database Design:
- There is an ERD diagram details the relationships between the entities and can be found in the repository as a screenshot.

API Endpoints
  The microservice includes the following RESTful endpoints:
  
  - POST /posts: Create a new post.
  - PUT /posts/{id}/update: Update an existing post.
  - DELETE /posts/{id}/delete: Delete a specific post.
  - GET /posts/{id}: Retrieve a specific post.

Getting Started
 - Clone the repository
 - Set up the MySQL database
 - Execute the SQL scripts found in the repo to create the necessary tables.
 - Create virtual environment > virtualenv venv
 - Activate your created virtual env > ven\scripts\activate
 - Install the requirements > pip install -r requirements.txt
 - Run the Flask application > python app.py
 - Access the API at http://localhost:5000.


