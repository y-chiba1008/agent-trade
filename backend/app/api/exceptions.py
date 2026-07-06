from fastapi import Request
from fastapi.responses import JSONResponse

from app.features.common.errors import (
    DomainError,
    InsufficientBalanceError,
    NotFoundError,
    PriceUnavailableError,
    ValidationError,
)


async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={'detail': str(exc)})


async def validation_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={'detail': str(exc)})


async def insufficient_balance_handler(
    _request: Request,
    exc: InsufficientBalanceError,
) -> JSONResponse:
    return JSONResponse(status_code=422, content={'detail': str(exc)})


async def price_unavailable_handler(
    _request: Request,
    exc: PriceUnavailableError,
) -> JSONResponse:
    return JSONResponse(status_code=503, content={'detail': str(exc)})


async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=400, content={'detail': str(exc)})


def register_exception_handlers(app) -> None:
    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(ValidationError, validation_handler)
    app.add_exception_handler(InsufficientBalanceError, insufficient_balance_handler)
    app.add_exception_handler(PriceUnavailableError, price_unavailable_handler)
    app.add_exception_handler(DomainError, domain_error_handler)
