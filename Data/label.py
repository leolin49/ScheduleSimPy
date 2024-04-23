# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/4 14:56
# Author  : linyf49@qq.com
# File    : label.py
from typing import List, Set


class Label(object):
    def __init__(self, tags_list: Set[str]):
        self._tags = set(tags_list)

    # def __str__(self):
    #     return self.tags

    def __len__(self) -> int:
        return len(self.tags)

    def __eq__(self, other: 'Label') -> bool:
        return self.tags == other.tags

    def __and__(self, other: 'Label') -> 'Label':
        return Label(self.tags & other.tags)

    def __or__(self, other: 'Label') -> 'Label':
        return Label(self.tags | other.tags)

    def issubset(self, other: 'Label') -> bool:
        return self.tags.issubset(other.tags)

    def match_num(self, other: 'Label') -> int:
        return len(self.tags & other.tags)

    @property
    def tags(self):
        return self._tags
