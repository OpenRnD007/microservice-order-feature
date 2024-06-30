# MicroService Series - Order Feature
## [Part of Microsevices Architecture](https://github.com/OpenRnD007/microservices/)

This FastAPI application streamlines the process of user authentication through the creation of tokens, verification of user credentials, and execution of CRUD operations. Following successful authentication, it grants users the capability to place new orders and access order details specific to their account within the system.

## Features

- OAuth2 token generation and authentication.
- Password hashing and verification.
- CRUD operations for user management.
- Place Order (TODO)
- Display all Orders by userinfo (TODO)


## Endpoints

### POST /token

OAuth2 compatible token login to get an access token for future requests.

### GET /users/me/

Read the current logged-in user's information.

### POST /users/

Create a new user in the database.

## Dependencies
- `Fastapi` for Framework
- `SQLAlchemy` for ORM support.
- `Pydantic` for data validation and schema definition.
- `Passlib` for password hashing.
- `python-jose` for JWT token creation and verification.


## Installation

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Set up your `.env` file with the necessary environment variables.

## Env Configuration
- `POSTGRES_HOST`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `SECRET_KEY`
- `ALGORITHM`

## Usage

Run the FastAPI server with the command:

```bash
uvicorn main:app --reload
```

### Navigate to /docs or /redoc for interactive API documentation.


## Contributing
Contributions to this project are welcome. To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License
This project is licensed under the [MIT License](LICENSE).

## TODO
- Orders API