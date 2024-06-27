# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/26 18:17
@Auth ： yuslience
@File ：clickhouseApi.py
@IDE ：PyCharm
@Motto:Emmo...
"""
import pandas as pd
from typing import Tuple
from clickhouse_driver import Client


class ClickhouseClient:
    """ Clickhouse Database Api """

    def __init__(self, host: str = "localhost", port: int = 9000, user: str = "", password: str = "", database: str = ""):
        # 初始化数据库连接
        self.ck_conn = Client(host=host, port=port, user=user, password=password, database=database,
                              settings={'use_numpy': True})

    def execute_many(self, header_sql: str, df: pd.DataFrame) -> Tuple:
        """
        批量写入Df格式的数据
        :param header_sql: 表头信息,一般格式为: "INSERT INTO `{table_name}`(*) VALUES"
        :param df:
        :return:
        """
        flag = False
        err_res = None
        execute_res = None
        try:
            execute_res = self.ck_conn.insert_dataframe(header_sql, df)
            flag = True
        except Exception as err:
            err_res = err
        return flag, err_res, execute_res

    def execute_single(self, single_sql: str):
        """
        Execute a single SQL query.
        @param single_sql: SQL query to execute
        @return: Tuple containing a success flag, error message (if any), and query results
        """
        flag = False
        err_res = None
        execute_res = []
        try:
            # 执行SQL查询并获取数据
            execute_result = self.ck_conn.execute(single_sql, with_column_types=True)
            # 获取字段名称
            columns = [col[0] for col in execute_result[1]]
            # 将字段名称和数据组合成字典列表
            execute_res = [dict(zip(columns, row)) for row in execute_result[0]]
            flag = True
        except Exception as err:
            err_res = err
        return flag, err_res, execute_res

    def get_tables(self):
        """ Get All Tables """
        query_sql = "SHOW TABLES;"
        flag, err, res = self.execute_single(query_sql)
        # 返回表名列表
        return [table_dict["name"] for table_dict in res] if flag else []

    def get_databases(self):
        """ Get All Databases """
        query_sql = "SHOW DATABASES;"
        flag, err, res = self.execute_single(query_sql)
        # 返回数据库名列表
        return [db_dict["name"] for db_dict in res] if flag else []

