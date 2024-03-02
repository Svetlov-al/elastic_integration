import uvicorn
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import FastAPI
from starlette.requests import Request

from mapping import MAPPING_FOR_INDEX
from models import CreateUserRequest

elastic_client = AsyncElasticsearch(hosts='http://localhost:9200')
app = FastAPI(
    title='Elastic Search Integration'
)
app.state.elastic_client = elastic_client


@app.get('/ping')
async def ping() -> dict[str, bool]:
    return {'success': True}


@app.get('/create_index')
async def create_index(request: Request) -> dict:
    elastic: AsyncElasticsearch = request.app.state.elastic_client
    await elastic.indices.create(index='users', mappings=MAPPING_FOR_INDEX)
    return {"success": True}


@app.get('/delete_index')
async def delete_index(request: Request) -> dict:
    elastic: AsyncElasticsearch = request.app.state.elastic_client
    try:
        await elastic.indices.delete(index='users')
    except NotFoundError as e:
        print(f'Error-{e}')
        return {"failed": e.status_code}
    return {"success": True}


@app.post('/create_user')
async def create_user(request: Request, body: CreateUserRequest) -> dict:
    elastic: AsyncElasticsearch = request.app.state.elastic_client
    res = await elastic.index(index='users', document=body.model_dump())
    res_dict = {"index": res["_index"], "id": res["_id"], "result": res["result"]}
    return {"success": True, "result": res_dict}


@app.get('/all_users')
async def get_all_users(request: Request):
    elastic: AsyncElasticsearch = request.app.state.elastic_client
    res = await elastic.search(index='users', query={"match_all": {}})
    return {"success": True, "result": res}


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
