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

from superlinked.framework.common.dag.context import ExecutionContext
from superlinked.framework.common.dag.dag import Dag
from superlinked.framework.common.dag.dag_effect import DagEffect
from superlinked.framework.common.data_types import Vector
from superlinked.framework.common.exception import (
    InvalidDagEffectException,
    InvalidSchemaException,
)
from superlinked.framework.common.parser.parsed_schema import ParsedSchema
from superlinked.framework.common.schema.id_schema_object import IdSchemaObject
from superlinked.framework.common.schema.schema_object import SchemaObject
from superlinked.framework.common.storage_manager.storage_manager import StorageManager
from superlinked.framework.compiler.online_schema_dag_compiler import (
    OnlineSchemaDagCompiler,
)
from superlinked.framework.evaluator.dag_evaluator import DagEvaluator
from superlinked.framework.online.dag.evaluation_result import EvaluationResult
from superlinked.framework.online.dag.online_schema_dag import OnlineSchemaDag


class OnlineDagEvaluator(DagEvaluator[EvaluationResult[Vector]]):
    def __init__(
        self,
        dag: Dag,
        schemas: set[SchemaObject],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__()
        self._dag = dag
        self._schemas = schemas
        self._schema_online_schema_dag_mapper = (
            self.__init_schema_online_schema_dag_mapper(
                self._schemas, self._dag, storage_manager
            )
        )
        self._dag_effect_online_schema_dag_mapper = (
            self.__init_dag_effect_online_schema_dag_mapper(self._dag, storage_manager)
        )

    def __get_single_schema(self, parsed_schemas: list[ParsedSchema]) -> IdSchemaObject:
        unique_schemas: set[IdSchemaObject] = {
            parsed_schema.schema for parsed_schema in parsed_schemas
        }
        if len(unique_schemas) != 1:
            raise InvalidSchemaException(
                f"Multiple schemas ({[s._schema_name for s in unique_schemas]}) present in the index."
            )
        return next(iter(unique_schemas))

    def evaluate(
        self,
        parsed_schemas: list[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector]]:
        index_schema = self.__get_single_schema(parsed_schemas)
        if (
            online_schema_dag := self._schema_online_schema_dag_mapper.get(index_schema)
        ) is not None:
            return online_schema_dag.evaluate(parsed_schemas, context)

        raise InvalidSchemaException(
            f"Schema ({index_schema._schema_name}) isn't present in the index."
        )

    def evaluate_by_dag_effect(
        self,
        parsed_schema: ParsedSchema,
        context: ExecutionContext,
        dag_effect: DagEffect,
    ) -> EvaluationResult[Vector]:
        if (
            online_schema_dag := self._dag_effect_online_schema_dag_mapper.get(
                dag_effect
            )
        ) is not None:
            return online_schema_dag.evaluate([parsed_schema], context)[0]
        raise InvalidDagEffectException(
            f"DagEffect ({dag_effect}) isn't present in the index."
        )

    def __init_schema_online_schema_dag_mapper(
        self,
        schemas: set[SchemaObject],
        dag: Dag,
        storage_manager: StorageManager,
    ) -> dict[SchemaObject, OnlineSchemaDag]:
        return {
            schema: OnlineSchemaDagCompiler(set(dag.nodes)).compile_schema_dag(
                dag.project_to_schema(schema),
                storage_manager,
            )
            for schema in schemas
        }

    def __init_dag_effect_online_schema_dag_mapper(
        self, dag: Dag, storage_manager: StorageManager
    ) -> dict[DagEffect, OnlineSchemaDag]:
        dag_effect_schema_dag_map = {
            dag_effect: dag.project_to_dag_effect(dag_effect)
            for dag_effect in dag.dag_effects
        }
        return {
            dag_effect: OnlineSchemaDagCompiler(
                set(schema_dag.nodes)
            ).compile_schema_dag(
                schema_dag,
                storage_manager,
            )
            for dag_effect, schema_dag in dag_effect_schema_dag_map.items()
        }
