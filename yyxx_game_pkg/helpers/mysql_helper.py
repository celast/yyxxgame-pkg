# -*- coding: utf-8 -*-
"""
@File: mysql_helper.py
@Author: ltw
@Time: 2023/3/22
"""
import pymysql
from dbutils.pooled_db import PooledDB
from yyxx_game_pkg.utils.decorator import (
    except_monitor,
    log_execute_time_monitor,
    singleton_unique_obj_args,
)
from yyxx_game_pkg.logger.log import root_log


# ####################################################
class MysqlConfig:
    HOST = None
    PORT = None
    USER = None
    PASSWD = None
    DB = None
    USE_UNICODE = None
    CHARSET = None
    MAX_CACHED = None
    MAX_CONNECTIONS = None

    def __str__(self):
        return "host:{},port:{},db:{},use_unicode:{},charset:{},max_cache:{},max_connections:{}".format(
            self.HOST,
            self.PORT,
            self.DB,
            self.USE_UNICODE,
            self.CHARSET,
            self.MAX_CACHED,
            self.MAX_CONNECTIONS,
        )


@singleton_unique_obj_args
class MysqlDbPool(object):
    def __init__(self, config: MysqlConfig):
        self.DB_POOL = PooledDB(
            creator=pymysql,
            maxcached=config.MAX_CACHED,
            maxconnections=config.MAX_CONNECTIONS,
            host=config.HOST,
            port=config.PORT,
            user=config.USER,
            passwd=config.PASSWD,
            db=config.DB,
            use_unicode=config.USE_UNICODE,
            charset=config.CHARSET,
        )
        root_log(f"<MysqlDbPool> init, info:{config}")

    @except_monitor
    @log_execute_time_monitor()
    def get_connection(self):
        return self.DB_POOL.connection()

    def close_connection(self):
        """
        关闭线程池,线程池最少占用1连接,100个进程跑1000个相同IP库的服时,最多会生成10W连接，所以需要关闭线程池，释放全部连接。
        优化点：以后可以相同IP的服务器共用1个线程池（现阶段sql查game库没有指定库名,改动地方多,搁置）
        :return:
        """
        self.DB_POOL.close()


# #################### 模块对外接口 ####################
def get_dbpool(config: dict) -> MysqlDbPool:
    class Config(MysqlConfig):
        HOST = config["host"]
        PORT = config["port"]
        USER = config["user"]
        PASSWD = config["password"]
        DB = config["db"]
        USE_UNICODE = config.get("use_unicode", True)
        CHARSET = config.get("charset", "utf8")
        MAX_CACHED = config.get("maxcached", 0)
        MAX_CONNECTIONS = config.get("maxconnections", 0)

    return MysqlDbPool(Config())
