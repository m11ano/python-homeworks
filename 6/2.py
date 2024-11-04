import asyncio
import aiohttp
from typing import TypeVar, Type

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

                    # print(data)
                    adapter = TypeAdapter(result_type)
                    return adapter.validate_python(data)
                else:
                    raise GetJsonByUrlError("BAD_STATUS", response)
        except GetJsonByUrlError:
            raise
        except Exception:
            raise


class ResponseDataLocation(BaseModel):
    name: str
    country: str


class ResponseDataCurrent(BaseModel):
    temp_c: float
    wind_kph: float
    cloud: int
    pressure_mb: float
    precip_mm: float


class ResponseData(BaseModel):
    location: ResponseDataLocation
    current: ResponseDataCurrent


async def main() -> None:
    q = input("Введите название города:")
    if len(q) == 0:
        return

    try:
        data = await get_json_by_url(
            f"http://api.weatherapi.com/v1/current.json?key=ee8616928f4c4b8481394936240311&q={q.strip()}&aqi=no",
            ResponseData,
        )

        print(f"Город: {data.location.country}, {data.location.name}")
        print("Погода:")
        print(f"\tТемпература: {data.current.temp_c}")
        print(f"\tСкорость ветра: {data.current.wind_kph} км/ч")
        print(f"\tОблачность: {data.current.cloud}%")
        print(f"\tДавление: {data.current.pressure_mb} милибар")
        print(f"\tОсадки: {data.current.precip_mm} мм")

    except GetJsonByUrlError as e:
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
