import time

from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start

        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        return response