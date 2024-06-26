import random
import typing
import uuid
from datetime import datetime
from enum import Enum
from string import ascii_letters
from typing import Any, Dict, Type, Union, get_args, get_origin

from pydantic import BaseModel, ConstrainedInt, NonNegativeInt, PositiveInt


class ModelObjectGenerator:
    simple_types = ("str", "float", "int", "bool", "list", "dict", "UUID", "date")
    pre_defined: Dict = None

    # TODO Add data generation that considers pydantic validators
    def generate(self, model: Type[BaseModel], **pre_defined) -> BaseModel:
        data = {}

        if self.pre_defined is None:
            self.pre_defined = pre_defined

        for name, type_ in typing.get_type_hints(model).items():
            if self.pre_defined.get(name, "pre_defined_is_absent") == "pre_defined_is_absent":
                data[name] = self.generate_field_value(type_)
            else:
                data[name] = self.pre_defined.pop(name)

        return model(**data)

    def generate_field_value(self, type_: Type, child: Type = None, **pre_defined) -> Any:
        if isinstance(type_, typing._GenericAlias):
            # List[str] -> list + str, Optional[int] -> Union[int, None] -> Union + int or None
            return self.generate_field_value(get_origin(type_), random.choice(get_args(type_)))
        elif isinstance(type_, typing._SpecialForm):
            # Union + int or None -> int or None
            return self.generate_field_value(child)
        elif type_.__name__ in self.simple_types:
            return self.generate_simple_value(type_.__name__, child)
        elif issubclass(type_, BaseModel):
            return self.generate(type_, **pre_defined)
        elif issubclass(type_, Enum):
            return random.choice(list(type_))
        elif issubclass(type_, ConstrainedInt):
            return self.generate_pydantic_int(type_)
        elif type_ == type(None):  # noqa E721
            return None
        else:
            raise Exception(type_)

    def generate_simple_value(self, type_name: str, child: Type = None) -> Union[str, float, int, bool, list, dict]:
        if type_name == "str":
            return random.choice(ascii_letters)
        elif type_name == "float":
            return random.uniform(1, 100)
        elif type_name == "int":
            return random.randint(-100, 100)
        elif type_name == "bool":
            return random.random()
        elif type_name == "list":
            return [self.generate_field_value(child or random.choice(self.simple_types)) for _ in range(10)]
        elif type_name == "dict":
            return {
                self.generate_simple_value("str"): self.generate_field_value(child or random.choice(self.simple_types))
                for _ in range(10)
            }
        elif type_name == "UUID":
            return uuid.uuid4()
        elif type_name == "date":
            return datetime.now().date()
        else:
            raise Exception(type_name)

    def generate_pydantic_int(self, type_: Type) -> int:
        if type_ == PositiveInt:
            return random.randint(1, 100)
        elif type_ == NonNegativeInt:
            return random.randint(0, 100)
