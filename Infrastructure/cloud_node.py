# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/2 12:38
# Author  : linyf49@qq.com
# File    : cloud_node.py.py
from Infrastructure.edge_node import EdgeNode, EdgeNodeConfig


# 边缘云
class CloudNode(EdgeNode):
    def __init__(self, node_id: int, cfg: EdgeNodeConfig):
        super().__init__(node_id, cfg)
