# Flask Overview

## Flask is a web framework that lets you build HTTP servers in Python

1. The imported Flask class is used to create the application itself. 
2. jsonify is a helper that converts dicts and lists into proper JSON HTTP responses (e.g. setting the correct Content-Type: application/json header automatically).
3. request is a global object Flask provides that gives access to the incoming HTTP requests data (body, headers, query params, etc)
4. SQLAlchemy is an ORM (Object Relational Mapper). Lets you interact with the database using python objects instead of writing raw SQL.
5. SQLALCHEMY_DATABASE_URI tells SQLAlchemy where database is.
6. SQLite is a file based database. It creates a file called tasks.db in project folder. No separate database server needed. In production you'd just swap this for postgres or mysql (e.g. 'postgresql://username:password@localhost/dbname')
7. db = SQLAlchemy(app) creates a database connection tied to your Flask app.
8. REST means Representational State Transfer and its a convention for designing APIs where HTTP methods map to database operations.

## Flask Testing Using Pytest
1. @pytest.fixture decorator for the functions *client* and *sample_task* are reusable test functions. Instead of repeating database setup for every test, we define it once and use it on each test.
2. Every test gets a fresh database via the fixture so tests never affect each other. 
3. Tests are grouped into classes to keep things organized. 
4. We are making different assertions about what the response should contain. Success and failure modes are tested to catch subtle bugs normal status codes would not reveal.