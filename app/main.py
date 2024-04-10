from fastapi import FastAPI, Depends
from app.utils.exceptions import (
    AppExceptionCase,
    app_exception_handler,
    http_exception_handler,
    request_validation_exception_handler
)
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User
from app.config.user import (
    SECRET_KEY,
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)
from app.config.faststream import app
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import App Routers
from app.routers.task_workflow import router as task_workflow_router


# Added custom Exception handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


# Include fastapi-users Routers to app here
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET_KEY),
    prefix="/auth/google",
    tags=["auth"],
)


# Include API Routers to app here
app.include_router(task_workflow_router)


# Root route
@app.get("/", tags=["Base Url"])
async def welcome_msg() -> dict:
    return {"message": "Welcome to Task Workflow!"}

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}