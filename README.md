# Poll System Backend

This is the backend for the **Poll System** API, Built in completion of the ALX ProDevs Program, it is developed using **Django** and **Django Rest Framework** (DRF) ans PostgreSQL, with JWT authentication for user login and vote functionality. The system allows users to create polls, vote on options, and retrieve poll results.

## Features

- **Poll Management**: Create, update, and delete polls.
- **Voting System**: Users can cast votes on poll options.
- **JWT Authentication**: Secure login and token-based authentication for API access.
- **Swagger Documentation**: Auto-generated API documentation using **drf-yasg**.
- **Real-Time Vote Updates**: Track votes in real-time and prevent duplicate voting by a user.

## Table of Contents

- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
  - [Login](#login)
  - [Create Poll](#create-poll)
  - [Vote on Poll](#vote-on-poll)
- [Swagger UI](#swagger-ui)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

Follow these steps to install and set up the backend for the Poll System.

### Prerequisites

- **Python 3.8+** (Ensure Python is installed on your machine)
- **PostgreSQL** (Database used for the project)
- **pip** (Python package manager)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/evarmedia/poll_system.git
   cd poll_system-backend
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # For Linux/macOS
   myenv\Scripts\activate     # For Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:

   - Update `DATABASES` settings in `poll_system/settings.py` to configure your PostgreSQL connection.
   - Run migrations:

     ```bash
     python manage.py migrate
     ```

5. **Create a superuser for the admin panel (optional)**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

## Usage

### Login

To log in and receive a JWT token:

1. Send a `POST` request to `/api/login/` with **email** and **password** in the body.
   
   **Request body**:

   ```json
   {
       "email": "your_email",
       "password": "your_password"
   }
   ```

   **Response**:

   ```json
   {
       "email": "your_email",
       "access_token": "your_jwt_token",
       "refresh_token": "your_refresh_token"
   }
   ```

   Use the `access_token` in the **Authorize** section of Swagger UI (as described below) to authenticate API requests.

### Create Poll

To create a new poll, send a `POST` request to `/api/polls/`.

**Request body**:

```json
{
    "title": "What is your favorite programming language?",
    "description": "Please choose the programming language you like the most from the options below.",
    "expires_at": "2025-12-31T23:59:59Z",
    "options": [
        {"text": "Python"},
        {"text": "JavaScript"},
        {"text": "Java"},
        {"text": "C++"}
    ]
}
```

### Vote on Poll

To cast a vote, send a `POST` request to `/api/polls/<poll_id>/vote/<option_id>/`.

**Request body**: No body required; the user is added based on authentication.

**Response**:

```json
{
    "detail": "Vote cast successfully!"
}
```

### Swagger UI

The project uses **drf-yasg** to generate **Swagger UI** documentation for easy testing and exploration of the API.

1. Access Swagger UI at `http://127.0.0.1:8000/api/docs/`.
2. Click the **Authorize** button and enter the `Bearer` token from the login response in the format:

   ```
   Bearer <your_jwt_token>
   ```

   After successful authorization, you can start testing API endpoints.

## API Endpoints

### Authentication

- **POST /api/login/**: Login and receive JWT token.

### Poll Management

- **GET /api/polls/**: List all polls.
- **POST /api/polls/**: Create a new poll.
- **GET /api/polls/{poll_id}/**: Retrieve a specific poll.
- **PUT /api/polls/{poll_id}/**: Update an existing poll.
- **DELETE /api/polls/{poll_id}/**: Delete a poll.

### Voting

- **POST /api/polls/{poll_id}/vote/{option_id}/**: Cast a vote for a poll option.

## Testing

- **Unit Tests**: The project uses Django’s built-in testing framework. You can run tests with:

   ```bash
   python manage.py test
   ```

- **Manual Testing**: Use the Swagger UI to manually test API endpoints by sending requests with the Bearer token for authorization.

## Contributing

We welcome contributions to this project! To contribute:

1. Fork this repository.
2. Clone your fork.
3. Create a new branch.
4. Make your changes and commit them.
5. Push your changes and create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

---
