from .exception import exception_middleware
from .auth import auth_middleware

MIDDLEWARES = [
    exception_middleware,
    auth_middleware
]

__all__ = [
    'MIDDLEWARES'
]
