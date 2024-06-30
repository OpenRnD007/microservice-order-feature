from fastapi import FastAPI
from features.auth.routers import auth_routers

# Initialize the FastAPI application
app = FastAPI()

# Include the auth router in the application
app.include_router(auth_routers)