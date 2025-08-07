from json import loads
from random import randint

from scheme import Test, TestBase


class TestNotFound(Exception):
    pass


async def list_test() -> list[Test]:
    res = []
    try:
        with open("test.json") as f:
            test = loads(f.read())[randint(0, 1)]
            for question in test['questions']:
                res.append(Test.model_validate({'test_id': test["id"], **question}))
    except FileNotFoundError:
        pass
    return res


async def get_test(test_id: int) -> TestBase | None:
    try:
        with open("test.json") as f:
            for test in loads(f.read()):
                if test["id"] == test_id:
                    return TestBase(test_id=test["id"])
            else:
                raise TestNotFound(f'Test with id {test_id} not found')
    except FileNotFoundError:
        pass
    return


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(list_test()))
