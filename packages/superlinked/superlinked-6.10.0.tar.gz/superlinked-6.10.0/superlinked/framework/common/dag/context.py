# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from collections import defaultdict
from enum import Enum, auto

from beartype.typing import Mapping, TypeVar, cast
from typing_extensions import Self, TypeAlias

from superlinked.framework.common.exception import (
    NotImplementedException,
    QueryException,
)
from superlinked.framework.common.util import time_util

ContextValue: TypeAlias = int | float | str | Mapping | list | bool | None
T = TypeVar("T", bound=ContextValue)
CONTEXT_COMMON = "common"
CONTEXT_COMMON_ENVIRONMENT = "environment"
CONTEXT_COMMON_NOW = "now"
LOAD_DEFAULT_NODE_INPUT = "load_default_node_input"
SPACE_WEIGHT_PARAM_NAME = "weight"


class ExecutionEnvironment(Enum):
    IN_MEMORY = 1
    QUERY = 2
    BATCH = 3


class NowStrategy(Enum):
    SYSTEM_TIME = auto()
    CONTEXT_TIME = auto()
    CONTEXT_OR_SYSTEM_TIME = auto()


class ExecutionContext:
    def __init__(
        self,
        environment: ExecutionEnvironment,
        now_strategy: NowStrategy = NowStrategy.CONTEXT_OR_SYSTEM_TIME,
        data: Mapping[str, Mapping[str, ContextValue]] | None = None,
    ) -> None:
        self.__environment = environment
        self.__now_strategy = now_strategy
        self.__data: dict[str, dict[str, ContextValue]] = defaultdict(dict)
        if data:
            self.update_data(data)

    def update_data(self, data: Mapping[str, Mapping[str, ContextValue]]) -> Self:
        for key, sub_map in data.items():
            self.__data[key].update(sub_map)
        return self

    def now(self) -> int:
        match self.__now_strategy:
            case NowStrategy.CONTEXT_OR_SYSTEM_TIME:
                return (
                    self.__data_now() or time_util.now()
                )  # ingestion uses system time for in_memory executor if it is not overridden
            case NowStrategy.CONTEXT_TIME:
                now = self.__data_now()
                if now is None:
                    raise QueryException(
                        (
                            f"Environment's '{CONTEXT_COMMON}.{CONTEXT_COMMON_NOW}' ",
                            "property should always be initialized for query contexts",
                        )
                    )
                return now
            case NowStrategy.SYSTEM_TIME:
                return time_util.now()
            case _:
                raise NotImplementedException(
                    f"Unknown now strategy: {self.__now_strategy}"
                )

    @property
    def environment(self) -> ExecutionEnvironment:
        return self.__environment

    @property
    def data(self) -> Mapping[str, Mapping[str, ContextValue]]:
        return self.__data

    def has_environment(self, environment: ExecutionEnvironment) -> bool:
        return self.__environment == environment

    def get_node_context_value(
        self, node_id: str, key: str, _type: type[T]
    ) -> T | None:
        value = self.__node_context(node_id).get(key)
        if value is None:
            return None

        return cast(T, value)

    def set_node_context_value(
        self, node_id: str, key: str, value: ContextValue | None
    ) -> None:
        self.__node_context(node_id)[key] = value

    def get_common_value(self, key: str, _: type[T]) -> T | None:
        value = self.__common_context().get(key)
        if value is None:
            return None
        return cast(T, value)

    def set_common_value(self, key: str, value: ContextValue | None) -> None:
        self.__common_context()[key] = value

    def __data_now(self) -> int | None:
        now_value = self.__common_context().get(CONTEXT_COMMON_NOW)
        return None if now_value is None else int(cast(int, now_value))

    def __common_context(self) -> dict[str, ContextValue]:
        return self.__data[CONTEXT_COMMON]

    def __node_context(self, node_id: str) -> dict[str, ContextValue]:
        return self.__data[node_id]

    @property
    def is_query_context(self) -> bool:
        return self.has_environment(ExecutionEnvironment.QUERY)

    @property
    def should_load_default_node_input(self) -> bool:
        return bool(self.__data[CONTEXT_COMMON].get(LOAD_DEFAULT_NODE_INPUT))

    def set_load_default_node_input(self, load_default_node_input: bool) -> None:
        self.update_data(
            {CONTEXT_COMMON: {LOAD_DEFAULT_NODE_INPUT: load_default_node_input}}
        )

    @classmethod
    def from_context_data(
        cls,
        context_data: Mapping[str, Mapping[str, ContextValue]] | None,
        environment: ExecutionEnvironment,
        now_strategy: NowStrategy = NowStrategy.CONTEXT_OR_SYSTEM_TIME,
    ) -> ExecutionContext:
        return (
            cls(environment, now_strategy)
            if context_data is None
            else cls(environment, now_strategy).update_data(context_data)
        )
