from starlette.responses import JSONResponse


class BaseError(Exception):
    status_code = 400
    error_code = 'error'


class NifRequired(BaseError):
    status_code = 400
    error_code = 'nif_required'


class InvalidNif(BaseError):
    status_code = 400
    error_code = 'invalid_nif'



async def handle_base_error(request, exception):
    payload = dict(error_code=exception.error_code)
    error_desc = str(exception)

    if error_desc:
        payload.update({'error_desc': error_desc})

    return JSONResponse(payload, status_code=exception.status_code)


exception_handlers = {
    BaseError: handle_base_error
}