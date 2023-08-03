"""_summary_: Abstract Database class for multiple database types
"""

# Import the necessary modules
import os
import json
import logging
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.databases import mysql, postgresql, mssql, sqlite

# database driver support import
import psycopg2
import pyodbc
import pymysql


class Database(object):
    """_summary_: Abstract Database class for multiple database types"""

    def __init__(
            self,
            db_type,
            db_name=None,
            db_user=None,
            db_pass=None,
            db_host=None,
            db_port: int = 0,
    ):
        """
            The __init__ function is called when the class is instantiated.
            It sets up the object with all of its attributes and methods.

            :param self: Represent the instance of the class
            :param db_type: Specify the type of database that is being used
            :param db_name: Specify the name of the database to connect to
            :param db_user: Specify the username of the database
            :param db_pass: Store the password for the database
            :param db_host: Specify the hostname of the database server
            :param db_port: int: Specify the port number
            :param : Specify the type of database
            :return: Nothing, it is a constructor
            """
        self.db_type = db_type
        self.db_name = db_name if db_name else "master"
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host if db_host else 'localhost'
        self.db_port = db_port
        self._db = None
        self.connection = None
        self._cursor = None

    def connect(self):
        """
            The connect function is used to connect to the database.
            It takes in a db_type, db_user, db_pass, db_host and a port number as arguments.
            The function then uses these arguments to create an engine object
            that can be used for querying the database.

            :param self: Represent the instance of the class
            :return: A connection object
            """
        # ----------------------------------- mssql ---------------------------------- #
        if self.db_type == "mssql":
            try:
                conn_string = \
                    f"mssql+pyodbc://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/" \
                    f"{self.db_name}?driver=ODBC+Driver+18+for+SQL+Server" \
                    f"&TrustServerCertificate=yes"

                self._db = create_engine(conn_string)
                self._connection_string()
            except SQLAlchemyError as _e:
                logging.error(f"Error connecting to database: {_e}")
                raise RuntimeError(f"Connection error: {str(_e)}")
        # ----------------------------------- mysql ---------------------------------- #
        elif self.db_type == "mysql":
            try:
                conn_string = \
                    f"mysql+pymysql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
                self._db = create_engine(conn_string)
                self._connection_string()
            except SQLAlchemyError as e:
                logging.error(f"Error connecting to database: {e}")
                raise RuntimeError(f"Connection error: {str(e)}")
        # -------------------------------- postgresql -------------------------------- #
        elif self.db_type == "postgresql":
            try:
                conn_string = f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
                self._db = create_engine(conn_string)
                self._connection_string()
            except SQLAlchemyError as e:
                logging.error(f"Error connecting to database: {e}")
                raise RuntimeError(f"Connection error: {str(e)}")
        else:
            logging.error("Database type not supported")
            raise Exception("Database type not supported")

    def create_database(self):
        """
            The create_database function creates a database on the server.
            Args:
                db_type (str): The type of database to create.
                                The database currently supports mssql, mysql, and postgresql.
                db_host (str): The hostname or IP address of the server where the database will be created.
                                Defaults to localhost if not specified in config file or passed as an argument
                                when calling this function directly from Python code.
                db_port (int): The port number used by the DBMS for communication with
                                clients running on other machines; defaults to 1433 for MSSQL and 3306

            :param self: Represent the instance of the class
            :return: Nothing
        """
        # ----------------------------------- mssql ---------------------------------- #
        if self.db_type == "mssql":
            self.connection = pyodbc.connect(
                "DRIVER={ODBC Driver 18 for SQL Server};"
                f'SERVER={self.db_host};'
                # f'PORT={self.db_port};'
                'DATABASE=master;'
                f'UID={self.db_user};'
                f'PWD={self.db_pass};'
                'TrustServerCertificate=yes;'
            )
            self._cursor = self.connection.cursor()
            try:
                self._cursor.execute(f"CREATE DATABASE {self.db_name}")

                self._cursor.close()
                self.connection.commit()
                self.connection.close()

            except Exception as _e:
                self.connection.rollback()
                logging.error(f"Database creation failed: {_e}")
                raise RuntimeError(f"Connection error: {str(_e)}")

        # ----------------------------------- mysql ---------------------------------- #
        elif self.db_type == "mysql":
            self.connection = pymysql.connect(
                host=self.db_host, user=self.db_user, password=self.db_pass
            )
            self._cursor = self.connection.cursor()
            try:
                self._cursor.execute(f"CREATE DATABASE {self.db_name}")
            except Exception as _e:
                logging.error(f"Database creation failed: {_e}")
                raise RuntimeError(f"Connection error: {str(_e)}")

            self._cursor.close()

            self.connection.close()
        # -------------------------------- postgresql -------------------------------- #
        elif self.db_type == "postgresql":
            print(f"db details: {self.db_host}, {self.db_user}, {self.db_pass}")
            self.connection = psycopg2.connect(
                host=self.db_host, user=self.db_user, password=self.db_pass, port=self.db_port, database="postgres"
            )
            print(f"db name form create db 1: {self.db_name}")
            self.connection.autocommit = True
            self._cursor = self.connection.cursor()
            print(f"db name form create db 2: {self.db_name}")
            try:
                print(f"db name form create db: {self.db_name}")
                self._cursor.execute(f"CREATE DATABASE {self.db_name}")
            except Exception as _e:
                logging.error(f"Database creation failed: {_e}")
                raise RuntimeError(f"Connection error: {str(_e)}")

            self._cursor.close();

            self.connection.close()
        else:
            # log an exception
            logging.error("Database type not supported")
            raise Exception("Database type not supported")

    def disconnect(self):
        """
            The disconnect function closes the connection to the database.


            :param self: Represent the instance of the class
            :return: A null value and does not return anything
            """
        try:
            self._db.dispose()  # ignore
        except Exception as e:
            logging.error(f"Error disconnecting from database: {e}")
            raise RuntimeError(f"Connection error: {str(e)}")

    def query(self, sql: str, as_transaction: bool = False):
        """
            The query function takes in a SQL query as a parameter, then uses that query to select data from
            the database.
            The function returns the result of the query.

            :param self: Represent the instance of the class
            :param sql: str: Pass in the sql query that we want to execute
            :param as_transaction: bool: Pass in a boolean value to determine if the query should be executed as a
                                                transaction or not
            :return: The result of the query as a result-proxy object
        """
        try:
            # commit the transaction if as_transaction is True
            if as_transaction is True:
                print("transaction")
                with self._db.connect() as connection:
                    result = connection.execute(sql)
                    self._db.commit()
                return result
            else:
                print("not transaction")
                return self._db.execute(sql)
        except Exception as _e:
            logging.error(f"Query error: {str(_e)}")
            # connection.rollback()
            raise RuntimeError(f"Connection error: {str(_e)}")

    # transaction
    def transaction(self, sql: list):
        """
            The transaction function is used to execute multiple SQL statements within a single transaction.
            This function takes in a list of SQL statements and executes them one by one, rolling back the entire
            transaction if any error occurs. This ensures that all database operations are atomic.

            :param self: Represent the instance of the class
            :param sql: list: Pass in a list of sql statements that will be executed within the transaction
            :return: A boolean value
        """
        _session = sessionmaker(bind=self._db)
        session = _session()

        try:
            # Start a transaction
            session.begin()

            # Perform multiple database operations within the transaction with a loop
            for _sql in sql:
                session.execute(_sql)

            # Commit the transaction
            session.commit()

        except SQLAlchemyError as e:
            # Rollback the transaction if an error occurs
            session.rollback()
            logging.error(f"Transaction error: {str(e)}")
            raise RuntimeError(f"Connection error: {str(e)}")

        finally:
            # Close the session
            session.close()

    def get_tables(self):
        """
            The get_table_names function returns a list of table names in the database.

            :param self: Represent the instance of the class
            :return: A list of table names
        """
        try:
            _inspector = inspect(self._db)
            tables = _inspector.get_table_names()
            return tables
        except Exception as e:
            logging.error(f"Get table names error: {str(e)}")
            raise RuntimeError(f"Connection error: {str(e)}")

    def get_table_data(self, table_name):
        """
            The get_table_data function takes in a table name as an argument and returns the data from that table.

            :param self: Reference the instance of the class
            :param table_name: Specify the table to query
            :return: A list of tuples
        """
        try:
            return self.query(f'SELECT * FROM {table_name} LIMIT 10')
        except Exception as e:
            logging.error(f"Get table data error: {str(e)}")
            raise RuntimeError(f"Connection error: {str(e)}")

    def get_db_metadata(self):
        """
            The get_db_metadata function returns a dictionary containing the following metadata:
                - Engine
                - Collation (MySQL only)
                - Tables Length

            :param self: Represent the instance of the class
            :return: A dictionary with the database type as a key and
        """
        _inspector = inspect(self._db)
        metadata = MetaData()
        metadata.reflect(bind=self._db)

        response = {}

        # get the following metadata based on the database type:
        # Engine,	Collation,	Tables Length
        if self.db_type == "mysql":
            try:
                response[self.db_type] = {
                    "name": _inspector.default_schema_name,
                    "tables_length": len(_inspector.get_table_names()),
                }
            except Exception as e:
                logging.error(f"Get db metadata error: {str(e)}")
                raise RuntimeError(f"Connection error: {str(e)}")
        elif self.db_type == "mssql":
            try:
                response[self.db_type] = {
                    "name": _inspector.default_schema_name,
                    "tables_length": len(_inspector.get_table_names()),
                }
            except Exception as e:
                logging.error(f"Get db metadata error: {str(e)}")
                raise RuntimeError(f"Connection error: {str(e)}")
        elif self.db_type == "postgresql":
            sc = _inspector.get_schema_names()
            print("ps name",_inspector.default_schema_name)
            print("ps sc", sc)
            try:
                response[self.db_type] = {
                    "name": _inspector.default_schema_name if _inspector.default_schema_name != "public" else self._db.url.database,
                    "tables_length": len(_inspector.get_table_names()),
                }
            except Exception as e:
                logging.error(f"Get db metadata error: {str(e)}")
                raise RuntimeError(f"Connection error: {str(e)}")
        return response

    def get_table_metadata(self):
        """
            The get_table_metadata function returns a dictionary of dictionaries containing
            the following metadata for each table in the database:
                - engine
                - charset
                - collation
                - row_count

            :param self: Represent the instance of the class
            :return: A dictionary with the following keys:
        """
        _inspector = inspect(self._db)
        _table_names = _inspector.get_table_names()

        response = {}

        # get the following metadata based on the database type:
        # Table Name,	Engine,	Auto Increment,	Charset,	Data Length,	Collation,	Description,	Row Count,	Index length

        # ----------------------------------- mysql ---------------------------------- #
        if self.db_type == "mysql":
            try:
                for table_name in _table_names:
                    # get the engine and autoincrement values
                    table_engine = _inspector.get_table_options(table_name)['mysql_engine']
                    # auto_increment = _inspector.get_columns(table_name)[0]['autoincrement']

                    # get the charset and collation
                    table_charset = _inspector.get_table_options(table_name)['mysql_default charset']
                    table_collation = _inspector.get_table_options(table_name)['mysql_collate']

                    # get the data length and index length
                    # data_length = _inspector.get_indexes(table_name)[0]['total_length']
                    # index_length = _inspector.get_indexes(table_name)[0]['index_length']

                    # get the row count
                    row_count = self.query(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]

                    # add the table metadata to the response
                    response[table_name] = {
                        "engine": table_engine,
                        "charset": table_charset,
                        "collation": table_collation,
                        "row_count": row_count
                    }

            except Exception as e:
                logging.error(f"Get table metadata error: {str(e)}")
                raise RuntimeError(f"Connection error: {str(e)}")

        # ----------------------------------- mssql ---------------------------------- #
        if self.db_type == "mssql":
            try:
                for table_name in _table_names:
                    # get the engine and autoincrement values
                    table_engine = _inspector.get_table_options(table_name)['mssql_table_options']['engine']
                    # auto_increment = _inspector.get_columns(table_name)[0]['autoincrement']

                    # get the charset and collation
                    table_charset = _inspector.get_table_options(table_name)['mssql_table_options']['charset']
                    table_collation = _inspector.get_table_options(table_name)['mssql_table_options']['collation']

                    # get the data length and index length
                    # data_length = _inspector.get_indexes(table_name)[0]['total_length']
                    # index_length = _inspector.get_indexes(table_name)[0]['index_length']

                    # get the row count
                    row_count = self.query(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]

                    # add the table metadata to the response
                    response[table_name] = {
                        "engine": table_engine,
                        "charset": table_charset,
                        "collation": table_collation,
                        "row_count": row_count
                    }

            except Exception as e:
                logging.error(f"Get table metadata error: {str(e)}")
                raise RuntimeError(f"Connection error: {str(e)}")

        # -------------------------------- postgresql -------------------------------- #
        if self.db_type == "postgresql":
            try:
                for table_name in _table_names:
                    print("t names: ", table_name)
                    # get the engine and autoincrement values
                    table_engine = _inspector.get_table_options(table_name)['postgresql_table_options']['engine']
                    # auto_increment = _inspector.get_columns(table_name)[0]['autoincrement']

                    # get the charset and collation
                    table_charset = _inspector.get_table_options(table_name)['postgresql_table_options']['charset']
                    table_collation = _inspector.get_table_options(table_name)['postgresql_table_options']['collation']

                    # get the data length and index length
                    # data_length = _inspector.get_indexes(table_name)[0]['total_length']
                    # index_length = _inspector.get_indexes(table_name)[0]['index_length']

                    # get the row count
                    row_count = self.query(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]

                    # add the table metadata to the response
                    response[table_name] = {
                        "engine": table_engine,
                        "charset": table_charset,
                        "collation": table_collation,
                        "row_count": row_count
                    }
            except Exception as e:
                logging.error(f"Get table metadata error: {str(e)}")
                raise RuntimeError(f"Connection error: {str(e)}")

        return response

    # TODO: use this for altering table columns
    def get_table_columns(self, table):
        """
            The get_table_columns function takes in a table name and returns the columns of that table.

            :param self: Allow an object to refer to itself inside of a method
            :param table: Get the columns of a specified table
            :return: The columns in the table

        """
        # Create a metadata object and reflect the existing database schema
        metadata = MetaData(bind=self._db)
        metadata.reflect()

        inspector = inspect(self._db)

        try:
            # get the columns in the table
            _columns = inspector.get_columns(table)
            # get the foreign keys in the table
            fk = inspector.get_foreign_keys(table)
            # get the primary keys in the table
            pk = inspector.get_pk_constraint(table)
            # get unique constraints in the table
            uc = inspector.get_unique_constraints(table)

            for i in range(len(_columns)):
                if len(fk) != 0:
                    # foreign key
                    for j in range(len(fk)):
                        if _columns[i]['name'] in fk[j]['constrained_columns']:
                            _columns[i]['foreign_key'] = f"{fk[j]['referred_table']} {fk[j]['referred_columns']}"\
                                .replace("[", "").replace("]", "").replace("'", "")
                            _columns[i]['ondelete'] = fk[j]['options']['ondelete'] if 'ondelete' in fk[j][
                                'options'] else "NO ACTION"
                            _columns[i]['onupdate'] = fk[j]['options']['onupdate'] if 'onupdate' in fk[j][
                                'options'] else "NO ACTION"
                # primary key
                if str(_columns[i]['name']) in str(pk['constrained_columns']):
                    _columns[i]['primary_key'] = True
                else:
                    _columns[i]['primary_key'] = False
                # unique constraint
                if len(uc) != 0:
                    for k in range(len(uc)):
                        if _columns[i]['name'] == uc[k]['name']:
                            _columns[i]['unique'] = True
                        else:
                            _columns[i]['unique'] = False

            return _columns
        except Exception as e:
            logging.error(f"Get table columns error: {str(e)}")
            raise RuntimeError(f"Connection error: {str(e)}")

    # save database to a json file in the database folder
    def _connection_string(self):
        """
            The _connection_string function is used to create a connection string for the database.

            :param self: Represent the instance of the class
            :return: A string that is used to connect to the database

        """
        file_path = f"program/databases/{self.db_type}.json"
        try:
            with self._db.connect() as conn:
                result = conn.execute("SELECT 1")
                if result.fetchone():
                    if os.path.exists(file_path):
                        with open(file_path, "r+") as _file:  # noqa: W1514
                            data = json.load(_file)

                            new_data = {
                                self.db_name: [
                                    self.db_type,
                                    self.db_name,
                                    self.db_user,
                                    self.db_pass,
                                    self.db_host,
                                    self.db_port,
                                ]
                            }
                            data.update(new_data)

                            _file.seek(0)
                            json.dump(data, _file, indent=4)
                            _file.truncate()

                    else:
                        with open(file_path, "w") as _file:
                            data = {
                                self.db_name: [
                                    self.db_type,
                                    self.db_name,
                                    self.db_user,
                                    self.db_pass,
                                    self.db_host,
                                    self.db_port,
                                ]
                            }
                            json.dump(data, _file)
                else:
                    logging.error("Could not connect to the database")
        except Exception as e:
            logging.error(f"Connection error: {str(e)}")
            raise RuntimeError(f"Connection error: {str(e)}")

    # remove from connection string
    def remove_connection_string(self):
        """
            The _remove_connection_string function is used to remove a database from the connection string.

            :param self: Represent the instance of the class
            :return: A string that is used to connect to the database

        """
        file_path = f"program/databases/{self.db_type}.json"

        if os.path.exists(file_path):
            with open(file_path, "r+") as _file:
                data = json.load(_file)

                data.pop(self.db_name)

                _file.seek(0)
                json.dump(data, _file, indent=4)
                _file.truncate()

    @staticmethod
    def get_databases():
        """
            The get_databases function is used to get the databases from the database files.
            The function returns a dict with the databases connection string in it.

            :return: A dictionary with the databases
        """
        db_dict = {
            "MySQL": {
                "Databases": {}
            },
            "MSSQL": {
                "Databases": {}
            },
            "PostgreSQL": {
                "Databases": {}
            },
        }
        file_path = "program/databases/"

        # possible database files
        mysql_file = f"{file_path}mysql.json"
        mssql_file = f"{file_path}mssql.json"
        postgresql_file = f"{file_path}postgresql.json"

        # check if files exist and get the databases in the files as a dict
        if os.path.exists(mysql_file):
            with open(mysql_file, "r") as _file:
                data = json.load(_file)
                db_dict["MySQL"]["Databases"].update(data)
        if os.path.exists(mssql_file):
            with open(mssql_file, "r") as _file:
                data = json.load(_file)
                db_dict["MSSQL"]["Databases"].update(data)
        if os.path.exists(postgresql_file):
            with open(postgresql_file, "r") as _file:
                data = json.load(_file)
                db_dict["PostgreSQL"]["Databases"].update(data)

        return db_dict
