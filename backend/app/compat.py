from __future__ import annotations

from copy import deepcopy
from dataclasses import MISSING
from enum import Enum
from typing import Any

try:
    from fastapi import FastAPI, HTTPException, Query
except ModuleNotFoundError:
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str) -> None:
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    class FastAPI:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.args = args
            self.kwargs = kwargs
            self.routes: list[tuple[str, str, Any, Any]] = []

        def get(self, path: str, response_model: Any = None) -> Any:
            def decorator(func: Any) -> Any:
                self.routes.append(("GET", path, func, response_model))
                return func

            return decorator

    def Query(default: Any = None, **_: Any) -> Any:
        return default

try:
    from pydantic import BaseModel, Field
except ModuleNotFoundError:
    class _FieldInfo:
        def __init__(self, default: Any = MISSING, default_factory: Any = None) -> None:
            self.default = default
            self.default_factory = default_factory

    def Field(default: Any = MISSING, **kwargs: Any) -> _FieldInfo:
        return _FieldInfo(default=default, default_factory=kwargs.get("default_factory"))

    class BaseModel:
        def __init__(self, **values: Any) -> None:
            annotations = self._collect_annotations()
            for field_name in annotations:
                if field_name in values:
                    value = values[field_name]
                else:
                    field_default = getattr(self.__class__, field_name, MISSING)
                    if isinstance(field_default, _FieldInfo):
                        if field_default.default_factory is not None:
                            value = field_default.default_factory()
                        elif field_default.default is not MISSING and field_default.default is not ...:
                            value = deepcopy(field_default.default)
                        else:
                            raise TypeError(f"Missing required field '{field_name}'")
                    elif field_default is not MISSING and field_default is not ...:
                        value = deepcopy(field_default)
                    else:
                        raise TypeError(f"Missing required field '{field_name}'")
                setattr(self, field_name, value)

        @classmethod
        def _collect_annotations(cls) -> dict[str, Any]:
            annotations: dict[str, Any] = {}
            for model_class in reversed(cls.__mro__):
                annotations.update(getattr(model_class, "__annotations__", {}))
            return annotations

        def model_dump(self, mode: str | None = None) -> dict[str, Any]:
            del mode
            return {
                field_name: self._serialize(getattr(self, field_name))
                for field_name in self._collect_annotations()
            }

        @classmethod
        def _serialize(cls, value: Any) -> Any:
            if isinstance(value, BaseModel):
                return value.model_dump()
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, list):
                return [cls._serialize(item) for item in value]
            if isinstance(value, dict):
                return {key: cls._serialize(item) for key, item in value.items()}
            return value

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.model_dump()!r})"

        def __eq__(self, other: Any) -> bool:
            if not isinstance(other, BaseModel):
                return NotImplemented
            return self.model_dump() == other.model_dump()
