import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        duration = round(time.time() - start, 4)

        logger.info(
            "%s %s %s %.4fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response