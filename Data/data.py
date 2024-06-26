# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/2 11:51
# Author  : linyf49@qq.com
# File    : data.py


class Data(object):
    def __init__(self, data_id: int, size: float, location: int):
        """
        :param data_id: 数据编号
        :param size: 数据大小
        :param location: 数据位置
        """
        self.id = data_id
        self.size = size
        self.location = location
