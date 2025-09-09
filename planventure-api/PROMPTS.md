# Building the Planventure API with GitHub Copilot

This guide will walk you through creating a Flask-based REST API with SQLAlchemy and JWT authentication using GitHub Copilot to accelerate development.

## Prerequisites

- Python 3.8 or higher
- VS Code with GitHub Copilot extension
- Bruno API Client (for testing API endpoints)
- Git installed

## Project Structure

We'll be working in the `api-start` branch and creating a structured API with:
- Authentication system
- Database models
- CRUD operations for trips
- JWT token protection

## Step 1: Project Setup
### Prompts to Configure Flask with SQLAlchemy

Open Copilot Chat and type:
```
@workspace Update the Flask app with SQLAlchemy and basic configurations
```

When the code is generated, click "Apply in editor" to update your `app.py` file.

### Update Dependencies

In Copilot Chat, type:
```
update requirements.txt with necessary packages for Flask API with SQLAlchemy and JWT
```

Install the updated dependencies:
```bash
pip install -r requirements.txt
```

### Create .env File

Create a `.env` file for environment variables and add it to `.gitignore`.

## Step 2: Database Models

### User Model

In Copilot Edits, type:
```
Create SQLAlchemy User model with email, password_hash, and timestamps. add code in new files
```

Review and accept the generated code.

### Initialize Database Tables

Ask Copilot to create a database initialization script:
```
update code to be able to create the db tables with a python shell script
```

Run the initialization script:
```bash
python init_db.py
```

### Install SQLite Viewer Extension

1. Go to VS Code extensions
2. Search for "SQLite viewer"
3. Install the extension
4. Click on `init_db.py` to view the created tables

### Trip Model

In Copilot Edits, type:
```
Create SQLAlchemy Trip model with user relationship, destination, start date, end date, coordinates and itinerary
```

Accept changes and run the initialization script again:
```bash
python3 init_db.py
```

### Commit Your Changes

Use Source Control in VS Code:
1. Stage all changes
2. Click the sparkle icon to generate a commit message with Copilot
3. Click commit

## Step 3: Authentication System

### Password Hashing Utilities

In Copilot Edits, type:
```
Create password hashing and salt utility functions for the User model
```

Review, accept changes, and install required packages:
```bash
pip install bcrypt
```

### JWT Token Functions

In Copilot Edits, type:
```
Setup JWT token generation and validation functions
```

Review, accept changes, and install the JWT package:
```bash
pip install flask-jwt-extended
```

### Registration Route

In Copilot Edits, type:
```
Create auth routes for user registration with email validation
```

Review and accept the changes.

### Test Registration Route

Use Bruno API Client:
1. Create a new POST request
2. Set URL to `http://localhost:5000/auth/register`
3. Add header: `Content-Type: application/json`
4. Add JSON body:
```json
{
  "email": "user@example.com",
  "password": "test1234"
}
```
5. Send the request and verify the response

### Login Route

In Copilot Edits, type:
```
Create login route with JWT token generation
```

Review, accept changes, and restart the Flask server.

### Enable Development Mode

To have Flask automatically reload on code changes:

```bash
export FLASK_DEBUG=1
flask run
```

### Authentication Middleware

In Copilot Edits, type:
```
Create auth middleware to protect routes
```

Review and accept the changes.

### Commit Your Changes

Use Source Control and Copilot to create a commit message.

## Step 4: Trip Routes

### Create Trip Routes Blueprint

In Copilot Edits, type:
```
Create Trip routes blueprint with CRUD operations
```

Review and accept the changes.

> **Note**: Ensure that `verify_jwt_in_request` is set to `verify_jwt_in_request(optional=True)` if needed

### Test Trip Routes

Use Bruno API Client to test:
1. CREATE a new trip
2. GET a trip by ID

### Add Itinerary Template Generator

In Copilot Edits, type:
```
Create function to generate default itinerary template
```

Review, accept changes, and test the updated route.

## Step 5: Finalize API

### Configure CORS for Frontend Access

In Copilot Edits, type:
```
Setup CORS configuration for React frontend
```

Review and accept the changes.

### Add Health Check Endpoint

In Copilot Edits, type:
```
Create basic health check endpoint
```

Review and accept the changes.

### Commit Final Changes

Use Source Control with Copilot to create your final commit.

### Create README

Ask Copilot to write a comprehensive README for your API project.

## API Endpoints Reference

### Trip Endpoints

| Method | URL                              | Description         | Request Body | Auth Required |
|--------|----------------------------------|-------------------|--------------|---------------|
| POST   | http://localhost:5000/api/trips  | Create new trip   | Yes         | Yes           |
| GET    | http://localhost:5000/api/trips  | Get all trips     | No          | Yes           |
| GET    | http://localhost:5000/api/trips/1| Get trip by ID    | No          | Yes           |
| PUT    | http://localhost:5000/api/trips/1| Update trip       | Yes         | Yes           |
| DELETE | http://localhost:5000/api/trips/1| Delete trip       | No          | Yes           |

Example trip creation body:
```json
{
  "destination": "Paris, France",
  "start_date": "2024-06-15",
  "end_date": "2024-06-22",
  "coordinates": {
    "lat": 48.8566,
    "lng": 2.3522
  },
  "itinerary": {
    "day1": {
      "activities": [
        {
          "time": "09:00",
          "activity": "Visit Eiffel Tower",
          "location": "Champ de Mars"
        }
      ]
    }
  }
}
```

**Note**: All trip endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Curl Examples

1. Create a new trip:
```bash
curl -X POST http://localhost:5000/api/trips \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "destination": "Paris, France",
    "start_date": "2024-06-15",
    "end_date": "2024-06-22",
    "coordinates": {
      "lat": 48.8566,
      "lng": 2.3522
    },
    "itinerary": {
      "day1": {
        "activities": [
          {
            "time": "09:00",
            "activity": "Visit Eiffel Tower",
            "location": "Champ de Mars"
          }
        ]
      }
    }
  }'
```

1. Get all trips:
```bash
curl -X GET http://localhost:5000/api/trips \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

2. Get single trip:
```bash
curl -X GET http://localhost:5000/api/trips/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

4. Update trip:
```bash
curl -X PUT http://localhost:5000/api/trips/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "destination": "Updated Paris Trip",
    "start_date": "2024-06-16"
  }'
```

5. Delete trip:
```bash
curl -X DELETE http://localhost:5000/api/trips/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Note**: Replace `YOUR_JWT_TOKEN` with the actual token received from the login endpoint.

## Common Issues and Solutions

### GOTCHAS:

- Ensure there are no trailing slashes in any of the routes - especially the base `/trip` route
- Make sure all required packages are installed
- Check that JWT token validation is configured correctly
- Verify database tables are created properly using the SQLite viewer

## Next Steps

Consider these enhancements for your API:
- Add more comprehensive input validation
- Create custom error handlers for HTTP exceptions
- Setup logging configuration
- Add validation error handlers for form data
- Configure database migrations

## Conclusion

You now have a fully functional API with authentication, database models, and protected routes. This can serve as the backend for your Planventure application!