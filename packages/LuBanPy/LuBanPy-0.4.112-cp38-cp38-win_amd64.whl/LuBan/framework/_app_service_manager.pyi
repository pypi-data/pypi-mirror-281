#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_app_service_manager.py
@Author     ：Alex
@Date       ：2024/6/12 19:24 
@Function   ：应用服务管理器
"""
from typing import Optional


class __AppServiceManager:

    @property
    def __IS_TOP_PROCESS__(self) -> bool:
        """
        检查当前进程是否主进程

        :return bool:   当前是主进程返回True，否则返回False
        """
        pass

    @property
    def __CURRENT_PROCESS_NO__(self) -> int:
        """
        返回当前应用服务进程序号
        :return:
        """
        pass

    @property
    def __IS_DEBUG__(self) -> bool:
        """
        是否开启调试模式
        :return bool:
        """
        pass

    @property
    def __IS_RUNNING__(self) -> bool:
        """
        应用服进程是否运行中
        :return bool:       True运行中，False未运行
        """
        pass

    @property
    def __IS_EXIT__(self) -> bool:
        """
        当前是否已标记退出
        :return:
        """
        pass

    def send(self, msg, receiver=None):
        """
        发送消息

        :param msg:
        :param receiver:
        :return:
        """
        pass

    def command(self, directive: str, params=None):
        """
        发送命令

        :param directive:       操作指令
        :param params:          参数
        :return:
        """
        pass

    def start(self, cls: str, params: Optional[dict] = None, name: Optional[str] = None, daemon: bool = False, worker: int = 1, sync: bool = False):
        """
        启动新的服务进程发送指令

        向系统总线发送请求启动服务服务进程指令：`command:service-start`
        :param str cls:                     应用服务类名，需要实现`AppServiceInterface`接口
        :param Optional[dict] params:       可以给应用服务类传递参数
        :param Optional[str] name:          指定应用服务的名称，未指定时使用类名
        :param bool daemon:                 是否守护进程
        :param int worker:                  指定服务启动的子进程数量，最少必须为1
        :param bool sync:                   是否使用同步(True)或异步(False)模式启动进程（异步无需等待进程启动完成，即可调用下一进程启动）
        :return:
        """
        pass

    def run(self):
        """
        应用服务管理器运行正在启动入口
        :return:
        """
        pass

    def exit(self):
        """
        退出应用操作(推送请求)
        :return:
        """
        pass


App = __AppServiceManager()

__all__ = ['App']

