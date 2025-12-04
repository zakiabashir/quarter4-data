from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserResponse

security = HTTPBearer()

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 24 hours

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if token is provided (optional authentication)"""
    if not credentials:
        return None

    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            return None

        user_id: str = payload.get("sub")
        if user_id is None:
            return None

    except JWTError:
        return None

    return db.query(User).filter(User.id == user_id).first()

def require_role(required_role: str):
    """Decorator to require specific user role"""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role}"
            )
        return current_user
    return role_checker

# Role dependency functions
require_admin = require_role("admin")
require_instructor = require_role("instructor")

def require_student_or_instructor(current_user: User = Depends(get_current_active_user)):
    """Require student or instructor role"""
    if current_user.role not in ["student", "instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user

class AuthMiddleware:
    """Custom authentication middleware for route protection"""

    def __init__(self, app, excluded_paths=None):
        self.app = app
        self.excluded_paths = excluded_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/api/v1/auth/login",
            "/api/v1/auth/register"
        ]

    async def __call__(self, scope, receive, send):
        # Get the request path
        path = scope.get("path", "")

        # Skip authentication for excluded paths
        if any(path.startswith(excluded) for excluded in self.excluded_paths):
            return await self.app(scope, receive, send)

        # Check for Authorization header
        headers = dict(scope.get("headers", []))
        authorization = headers.get(b"authorization", b"").decode()

        if not authorization or not authorization.startswith("Bearer "):
            # Return 401 Unauthorized
            from fastapi.responses import JSONResponse
            response = JSONResponse(
                status_code=401,
                content={"detail": "Not authenticated"}
            )
            return await response(scope, receive, send)

        # Extract token
        token = authorization.split(" ")[1]
        payload = verify_token(token)

        if not payload:
            from fastapi.responses import JSONResponse
            response = JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
            return await response(scope, receive, send)

        # Add user info to scope
        user_id = payload.get("sub")
        scope["user_id"] = user_id

        return await self.app(scope, receive, send)