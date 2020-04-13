from starlette.responses import JSONResponse

from census.census import Palma
from census.errors import NifRequired


async def find(request):
    nif = request.query_params.get('nif', None)
    if nif is None:
        raise NifRequired()

    census = Palma()
    voter = await census.find_by_nif(nif)
    return JSONResponse(voter.to_dict())
