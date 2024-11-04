import asyncio
import aiohttp
from typing import TypeVar, Type, List
from pydantic import BaseModel, TypeAdapter, ValidationError

T = TypeVar("T")


class GetJsonByUrlError(Exception):
    def __init__(self, error_type: str, *args):
        super().__init__(error_type, *args)


async def get_json_by_url(url: str, result_type: Type[T]) -> T:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                    except Exception:
                        raise GetJsonByUrlError("BAD_RESPONSE", response)

                    adapter = TypeAdapter(result_type)
                    return adapter.validate_python(data)
                else:
                    raise GetJsonByUrlError("BAD_STATUS", response)
        except GetJsonByUrlError:
            raise
        except Exception:
            raise


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


async def main() -> None:
    try:
        data = await get_json_by_url(
            "https://jsonplaceholder.typicode.com/posts", List[Post]
        )
        for item in data[0:5]:
            print(item.model_dump_json())

    except GetJsonByUrlError as e:
        match e.args[0]:
            case "BAD_STATUS":
                print(f"response error: {e.args[1].status}")
            case "BAD_RESPONSE":
                print("incorrect response, bad json")
    except ValidationError:
        print("incorrect response, unexpected data format")
    except Exception as e:
        print("unknown error in response")


asyncio.run(main())
