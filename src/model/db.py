'''
Created on 3 Feb 2020

@author: nish
'''
from env.constant import SQL
from sqlalchemy import engine
from sqlalchemy import create_engine,           \
                       Table,                   \
                       MetaData,                \
                       Column,                  \
                       Integer,                 \
                       String,                  \
                       DateTime,                \
                       Boolean,                 \
                       Float,                   \
                       and_,                    \
                       asc,                    \
                       desc,                    \
                       between,                 \
                       UniqueConstraint
from sqlalchemy.exc import OperationalError, InterfaceError
from sqlalchemy.sql import select
import logging
import pandas as pd

class DBConnStringFactory:
    
    @staticmethod
    def build_connection_string(db_config):
        if db_config["dbms"] == "postgresql":
            conn_string = "{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(db_config["dbms"],
                                                                 db_config["connector"],
                                                                 db_config["su_user"],
                                                                 db_config["su_password"],
                                                                 db_config["host"],
                                                                 db_config["port"],
                                                                 db_config["db_name"])
        elif db_config["dbms"] == "mssql":
            conn_string = "{0}+{1}://{2}:{3}@{4}/{5}".format(db_config["dbms"],
                                                             db_config["connector"],
                                                             db_config["su_user"],
                                                             db_config["su_password"],
                                                             db_config["host"],
                                                             db_config["db_name"])
        return conn_string
    
class DatabaseManager:
    
    def __init__(self, db_config):
        self._logger = logging.getLogger("risk_matrix_log")
        self._db_config = db_config
        self._init_engine()
        self._create_connection()
        self.qry = self._read_sql_file(path=SQL)
        #execute the query here
        self.data = self.get_trade_query()
        
    def _init_engine(self):
        conn_string = DBConnStringFactory.build_connection_string(self._db_config)
        self._logger.debug("{} connection string created".format(conn_string))
        self._db_engine = create_engine(conn_string)
        try:
            self._db_engine.connect()
            self.db_exists = True
            self._logger.debug("Connection to the database {} successful".format(self._db_config["db_name"]))
        except (OperationalError, InterfaceError):
            self.db_exists = False
            self._logger.error("Connection to the database {} has failed".format(self._db_config["db_name"]))
    
    def _create_connection(self):
        self._logger.debug("establishing connection to the database")
        self.conn = self._db_engine.connect()
        self._logger.debug("connection to the database complete")
    
    def _read_sql_file(self, path=None):
        with open(path, "r") as sql_file:
            qry = sql_file.read()
        return qry
             
    def get_trade_query(self):
        s = self._read_sql_file(path=SQL)
        return pd.read_sql(s, con=self._db_engine)



        