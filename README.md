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
  
  POST /posts: Create a new post.
  PUT /posts/{id}/update: Update an existing post.
  DELETE /posts/{id}/delete: Delete a specific post.
  GET /posts/{id}: Retrieve a specific post.

Getting Started
 1- Clone the repository
 2- Set up the MySQL database
 3- Execute the SQL scripts found in the repo to create the necessary tables.
 4- Create virtual environment > virtualenv venv
 5- Activate your created virtual env > ven\scripts\activate
 6- Install the requirements > pip install -r requirements.txt
 7- Run the Flask application > python app.py
 8- Access the API at http://localhost:5000.


