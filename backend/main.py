import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyQuery as BaseAPIKeyQuery
from pydantic import ValidationError
from starlette.status import HTTP_403_FORBIDDEN

from scheme import Test, TestResponse
from utils import list_test, get_test, TestNotFound

app = FastAPI()
load_dotenv('.env')
API_KEY = os.getenv('API_KEY')


class APIKeyQuery(BaseAPIKeyQuery):

    @staticmethod
    def check_api_key(api_key: Optional[str], auto_error: bool) -> Optional[str]:
        if not api_key or api_key != API_KEY:
            if auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            return None
        return api_key


query_scheme = APIKeyQuery(name="api_key")


@app.get("/tests")
async def tests(api_key: str = Depends(query_scheme)):
    try:
        data: list[Test] = await list_test()
        return data
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/results")
async def results(test_result: TestResponse, api_key: str = Depends(query_scheme)):
    try:
        test = await get_test(test_result.test_id)
        return {
            'accepted': True,
            'test_id': test.test_id,
            'score': test_result.score,
        }
    except TestNotFound:
        raise HTTPException(status_code=404, detail=f"Test with id {test_result.test_id} not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
