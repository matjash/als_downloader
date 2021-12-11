# -*- coding: utf-8 -*-

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name

    from .lidar_slovenia import LidarSlovenia
    return LidarSlovenia(iface)
