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


from beartype.typing import Mapping

from superlinked.framework.common.dag.categorical_similarity_node import (
    CategoricalSimilarityNode,
)
from superlinked.framework.common.dag.node import Node
from superlinked.framework.common.dag.schema_field_node import SchemaFieldNode
from superlinked.framework.common.data_types import Vector
from superlinked.framework.common.embedding.categorical_similarity_embedding import (
    CategoricalSimilarityParams,
)
from superlinked.framework.common.schema.schema_object import (
    SchemaObject,
    String,
    StringList,
)
from superlinked.framework.dsl.space.exception import InvalidSpaceParamException
from superlinked.framework.dsl.space.space import Space
from superlinked.framework.dsl.space.space_field_set import SpaceFieldSet


class CategoricalSimilaritySpace(Space):
    """
    Represents a space for encoding categorical similarity.

    A CategoricalSimilaritySpace is designed to measure the similarity between items that
    are grouped into a finite number of textual categories. The categories are represented
    in an n-hot encoded vector, with the option to apply a negative filter for unmatched
    categories, enhancing the distinction between matching and non-matching category items.
    Negative_filter allows for filtering out unmatched categories, by setting
    it to a large negative value, effectively resulting in large negative similarity between
    non-matching category items. A category input not present in categories will be encoded
    as `other` category. These categories will be similar to each other by default. Set
    uncategorized_as_category parameter to False in order to suppress this behavior - this
    way other categories are not similar to each other in any case - not even to the same
    `other` category. To make that specific category value similar to only the same category
    items, consider adding it to `categories`.

    Attributes:
        category_input (StringList | List[StringList] | String | List[String]):
            The schema field containing input categories to be considered in the similarity space.
            Input contains one or more categories in a list if `StringList` is provided.
            If `String` is provided, then the input must be a single value.
        categories (List[str]): A list of categories that defines the dimensionality of the
            one-hot encoded vector. Any category not listed is considered as 'other'.
        negative_filter (float): A value to represent unmatched categories in the one-hot vector.
            Instead of using 0, which typically represents the absence of a category, this allows
            for a different representation - resulting in effectively filtering out items that has
            non-matching categories.
        uncategorized_as_category (bool): If set to False, the similarity between other categories will be
            set to 0, or negative_filter if set. By this we can control if a category_input not in
            categories will be similar to other category_inputs not in categories. Note that the same
            category_inputs not in categories will not be similar to each other either.
    Raises:
        InvalidSchemaException: If a schema object does not have a corresponding node in the
            similarity space.
    """

    def __init__(
        self,
        category_input: StringList | list[StringList] | String | list[String],
        categories: list[str],
        negative_filter: float = 0.0,
        uncategorized_as_category: bool = True,
    ) -> None:
        """
        Initializes a new instance of the CategoricalSimilaritySpace.

        This constructor sets up the space with the necessary configurations to encode and measure categorical
        similarity based on the provided parameters.

        Args:
            category_input (StringList | List[StringList] | String | List[String]):
            The schema field containing input categories to be considered in the similarity space.
            Input contains one or more categories in a list if `StringList` is provided.
            If `String` is provided, then the input must be a single value.
            categories (list[str]): A list of all the recognized categories. Categories not included in this list will
                be treated as 'other', unless `uncategorized_as_category` is False.
            negative_filter (float, optional): A value used to represent unmatched categories in the encoding process.
                This allows for a penalizing non-matching categories - in contrast to them contributing 0 to similarity,
                 it is possible to influence the similarity score negatively. Defaults to 0.0.
            uncategorized_as_category (bool, optional): Determines whether categories not listed in `categories` should
                be treated as a distinct 'other' category. Defaults to True.

        Raises:
            InvalidSchemaException: If a schema object does not have a corresponding node in the similarity space,
            indicating a configuration or implementation error.
        """
        super().__init__(
            # TODO FAI-1988 remove this type ignore
            category_input,  # type: ignore[misc]
            self.__get_input_type(category_input),
        )
        self.categorical_similarity_param: CategoricalSimilarityParams = (
            CategoricalSimilarityParams(
                categories=categories,
                uncategorized_as_category=uncategorized_as_category,
                negative_filter=negative_filter,
            )
        )
        self.__category = SpaceFieldSet(self, self._field_set)
        unchecked_category_node_map = {
            single_category: CategoricalSimilarityNode(
                parent=SchemaFieldNode(single_category),
                categorical_similarity_param=self.categorical_similarity_param,
            )
            for single_category in self._field_set
        }
        self.__schema_node_map: dict[SchemaObject, CategoricalSimilarityNode] = {
            schema_field.schema_obj: node
            for schema_field, node in unchecked_category_node_map.items()
        }

    def __get_input_type(
        self, category_input: StringList | list[StringList] | String | list[String]
    ) -> type[StringList] | type[String]:
        if isinstance(category_input, list):
            if not category_input:
                raise InvalidSpaceParamException("Category input must not be empty.")
            return type(category_input[0])
        return type(category_input)

    @property
    def _node_by_schema(self) -> Mapping[SchemaObject, Node[Vector]]:
        return self.__schema_node_map

    @property
    def uncategorized_as_category(self) -> bool:
        return self.categorical_similarity_param.uncategorized_as_category

    @property
    def category(self) -> SpaceFieldSet:
        return self.__category
