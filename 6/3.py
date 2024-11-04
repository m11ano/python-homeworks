import asyncio
import aiohttp
from typing import TypeVar, Type, Any
from pydantic import BaseModel, TypeAdapter, ValidationError

T = TypeVar("T")


class PostJsonByUrlError(Exception):
    def __init__(self, error_type: str, *args):
        super().__init__(error_type, *args)


async def post_json_by_url(url: str, data: Any, result_type: Type[T]) -> T:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                if response.status == 201:
                    try:
                        data = await response.json()
                    except Exception:
                        raise PostJsonByUrlError("BAD_RESPONSE", response)

                    adapter = TypeAdapter(result_type)
                    return adapter.validate_python(data)
                else:
                    raise PostJsonByUrlError("BAD_STATUS", response)
        except PostJsonByUrlError:
            raise
        except Exception:
            raise


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


async def main() -> None:
    post_title = input("Введите название поста: ")
    if len(post_title) == 0:
        return

    post_body = input("Введите текст поста: ")
    if len(post_body) == 0:
        return

    try:
        post = {
            "userId": 1,
            "title": post_title,
            "body": post_body,
        }

        data = await post_json_by_url(
            "https://jsonplaceholder.typicode.com/posts", post, Post
        )

        print(data.model_dump_json())

    except PostJsonByUrlError as e:
        match e.args[0]:
            case "BAD_STATUS":
                print(f"response error: {e.args[1].status}")
            case "BAD_RESPONSE":
                print("incorrect response, bad json")
    except ValidationError:
        print("incorrect response, unexpected data format")
    except Exception:
        print("unknown error in response")


asyncio.run(main())
