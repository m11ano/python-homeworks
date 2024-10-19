from typing import Type, Any, Dict


class Singleton(type):
    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls: Type[Any], *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            instance = cls._instances[cls]
        return instance
