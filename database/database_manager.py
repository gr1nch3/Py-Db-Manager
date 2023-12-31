from sqlalchemy import create_engine, inspect, Table, Column, MetaData
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    """_summary_: A class to manage database connections and operations
    """
    def __init__(self):
        self.engine = None
        self.session = None
        self.metadata = MetaData()

# ---------------------------------------------------------------------------- #
#                                  Connections                                 #
# ---------------------------------------------------------------------------- #
    def connect(self, db_url: str) -> bool:
        """_summary_

            Args:
                db_url (_type_): _description_ (e.g. "sqlite:///database.db")

            Returns:
                _type_: _description_
        """
        # inject a driver into the db_url
        # check if the db_url contains a + sign
        if not "+" in db_url:
            if db_url.startswith("mysql"):
                db_url = db_url.replace("mysql", "mysql+pymysql")
            elif db_url.startswith("postgresql"):
                db_url = db_url.replace("postgresql", "postgresql+psycopg2")
            elif db_url.startswith("mssql"):
                db_url = db_url.replace("mssql", "mssql+pyodbc")
            elif db_url.startswith("oracle"):
                db_url = db_url.replace("oracle", "oracle+cx_oracle")
            print(f"db_url (no driver specified): {db_url}")

        try:
            self.engine = create_engine(db_url)
            _session = sessionmaker(bind=self.engine)
            self.session = _session()
            print("Connection sucessful")
            return True
        except Exception as e:
            print(f"Failed to connect: {str(e)}")
            return False

    def disconnect(self):
        """_summary_ : Disconnects from the database
        """
        if self.session:
            self.session.close()
        self.engine = None
        self.session = None

# ---------------------------------------------------------------------------- #
#                                    Metadat                                   #
# ---------------------------------------------------------------------------- #
    def get_table_names(self) -> list:
        """_summary_ : Retrieves the names of all tables in the database

        Returns:
            _type_: _description_
        """
        try:
            inspector = inspect(self.engine)
            print(f"db names: {inspector.get_table_names()}")
            tables = inspector.get_table_names()
            return tables
        except Exception as e:
            print(f"Failed to retrieve table names: {str(e)}")
            return []

    def get_columns(self, table_name) -> list:
        """_summary_ : Retrieves the names of all columns in a table

            Args:
                table_name (_type_): _description_

            Returns:
                _type_: _description_
        """
        try:
            inspector = inspect(self.engine)
            # print(f"col names: {inspector.get_columns(table_name)}")
            print(f"tbl name: {table_name}")
            return inspector.get_columns(table_name)
        except Exception as e:
            print(f"Failed to retrieve column names: {str(e)}")
            return []

    def get_table_details(self, table_name) -> list:
        """_summary_ : Retrieves the details of a table in the database

        Args:
            table_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            inspector = inspect(self.engine)
            return inspector.get_columns(table_name)
        except Exception as e:
            print(f"Failed to retrieve table details: {str(e)}")
            return []

    def get_db_and_table_names(self) -> dict:
        """_summary_

            Returns:
                dict: _description_
        """
        try:
            inspector = inspect(self.engine)
            # tbl_names = inspector.get_table_names()
            return {
                self.engine.url.database: inspector.get_table_names()
            }
        except Exception as e:
            print(f"Failed to retrieve database and table names: {str(e)}")
            return {}

# ---------------------------------------------------------------------------- #
#                                    Tables                                    #
# ---------------------------------------------------------------------------- #
    def create_table(self, table_name, column_details) -> bool:
        """_summary_

            Args:
                table_name (_type_): _description_ (e.g. "users")
                column_details (_type_): _description_ (e.g. [("id", "Integer", "NOT NULL"), ("name", "String", "NULL")])

            Returns:
                _type_: _description_ (e.g. True)
        """
        try:
            columns = [
                Column(name, eval(data_type), nullable=constraint.lower() == 'nullable')
                for name, data_type, constraint in column_details
            ]

            table = Table(
                table_name,
                self.metadata,
                *columns
            )
            table.create(self.engine)
            return True
        except Exception as e:
            print(f"Table creation failed: {str(e)}")
            return False

    def drop_table(self, table_name) -> bool:
        """_summary_

        Args:
            table_name (_type_): _description_ (e.g. "users")

        Returns:
            bool: _description_
        """
        try:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
            table.drop(self.engine)
            return True
        except Exception as e:
            print(f"Table dropping failed: {str(e)}")
            return False

    def reflect_table(self, table_name) -> bool:
        """_summary_

        Args:
            table_name (_type_): _description_ (e.g. "users")

        Returns:
            bool: _description_
        """
        try:
            self.metadata.reflect(only=[table_name], views=True)
            return True
        except Exception as e:
            print(f"Reflecting table failed: {str(e)}")
            return False

    def refresh_metadata(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        try:
            self.metadata.reflect(views=True)
            return True
        except Exception as e:
            print(f"Refreshing metadata failed: {str(e)}")
            return False

# ---------------------------------------------------------------------------- #
#                                    Columns                                   #
# ---------------------------------------------------------------------------- #
    def add_column(self, table_name, column_name, column_type, nullable=True) -> bool:
        """_summary_

        Args:
            table_name (_type_): _description_ (e.g. "users")
            column_name (_type_): _description_ (e.g. "name")
            column_type (_type_): _description_ (e.g. "String")
            nullable (bool, optional): _description_. Defaults to True. (e.g. True)

        Returns:
            bool: _description_
        """
        try:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)

            # Check if the column already exists
            if column_name not in table.columns:
                new_column = Column(column_name, eval(column_type), nullable=nullable)
                new_column.create(table)
                self.metadata.create_all(self.engine)
                return True
            else:
                print(f"Column '{column_name}' already exists in table '{table_name}'.")
                return False
        except Exception as e:
            print(f"Adding column failed: {str(e)}")
            return False

    def remove_column(self, table_name, column_name) -> bool:
        """_summary_

        Args:
            table_name (_type_): _description_ (e.g. "users")
            column_name (_type_): _description_ (e.g. "name")       

        Returns:
            bool: _description_
        """
        try:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)

            # Check if the column exists
            if column_name in table.columns:
                table.c[column_name].drop()
                self.metadata.create_all(self.engine)
                return True
            else:
                print(f"Column '{column_name}' does not exist in table '{table_name}'.")
                return False
        except Exception as e:
            print(f"Removing column failed: {str(e)}")
            return False

# ---------------------------------------------------------------------------- #
#                                     CRUD                                     #
# ---------------------------------------------------------------------------- #
    def execute_query(self, query) -> list:
        """_summary_

            Args:
                query (_type_): _description_ (e.g. "SELECT * FROM users")

            Returns:
                list: _description_
        """
        try:
            result = self.session.execute(query)
            if result.returns_rows:
                return result.fetchall()
            else:
                return None
        except Exception as e:
            print(f"Query execution failed: {str(e)}")
            return None

    def insert_record(self, table_name, data) -> bool:
        """_summary_

        Args:
            table_name (_type_): _description_ (e.g. "users")
            data (_type_): _description_ (e.g. {"name": "John Doe", "age": 25})

        Returns:
            bool: _description_
        """
        try:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
            self.session.execute(table.insert().values(data))
            self.session.commit()
            return True
        except Exception as e:
            print(f"Record insertion failed: {str(e)}")
            return False

    def update_record(self, table_name, primary_key, data) -> bool:
        """_summary_

        Args:
            table_name (_type_): _description_ (e.g. "users")
            primary_key (_type_): _description_ (e.g. 1)
            data (_type_): _description_ (e.g. {"name": "John Doe", "age": 25})

        Returns:
            bool: _description_
        """
        try:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
            self.session.execute(table.update().where(table.c.id == primary_key).values(data))
            self.session.commit()
            return True
        except Exception as e:
            print(f"Record update failed: {str(e)}")
            return False

    def delete_record(self, table_name, primary_key) -> bool:
        """_summary_

        Args:
            table_name (_type_): _description_ (e.g. "users")
            primary_key (_type_): _description_ (e.g. 1)

        Returns:
            bool: _description_
        """
        try:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
            self.session.execute(table.delete().where(table.c.id == primary_key))
            self.session.commit()
            return True
        except Exception as e:
            print(f"Record deletion failed: {str(e)}")
            return False
