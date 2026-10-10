from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):

        errors = []

        for error in exc.errors():
            errors.append(
                {
                    "loc": error.get("loc"),
                    "msg": str(error.get("msg")),
                    "type": str(error.get("type")),
                }
            )

        return JSONResponse(
            status_code=422,
            content={
                "detail": errors
            },
        )