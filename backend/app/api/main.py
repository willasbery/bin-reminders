from fastapi import APIRouter

from api.routes import login, users, collections

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(collections.router, prefix="/collections", tags=["collections"])

