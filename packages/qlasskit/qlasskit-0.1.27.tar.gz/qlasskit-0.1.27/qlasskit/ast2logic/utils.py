# Copyright 2023-2024 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# isort:skip_file

from typing import List, Any, Iterable, Union


# def flatten(m: List[List[Any]]) -> List[Any]:
#     return [item for row in m for item in row]


def flatten(m: List[Union[Any, List[Any]]]) -> List[Any]:
    return [
        item
        for row in m
        for item in (
            row if isinstance(row, Iterable) and not isinstance(row, str) else [row]
        )
    ]
