import sqlalchemy
from sqlalchemy import Column, String, MetaData, Table
from passlib.hash import pbkdf2_sha256
import pandas as pd
import migrate


class UsernameDatabase:
    """
    A class to manage the users database.
    """
    def __init__(self, username, password, host, port, database):
        """Constructor"""
        self.engine = sqlalchemy.create_engine(
                                                sqlalchemy.engine.url.URL(
                                                drivername='postgresql',
                                                username=username,
                                                password=password,
                                                host=host,
                                                port=port,
                                                database=database,
                                                 ),
                                                echo_pool=True,
                                                )
        self.meta = MetaData(self.engine)
        self.users_table = self.init_table()

    def init_table(self) -> sqlalchemy.Table:
        """
        Initiate the users_app table.

        Returns
        -------
        table   sqlalchemy Table
            Table containing three columns (username, hashed password and which apps it can access)
        """
        table = Table("users_app", self.meta,
                      Column('username', String, primary_key=True, unique=True),
                      Column('password', String),
                      Column('app_access', String)
                      )
        return table

    def create_table(self) -> None:
        """
        Create the table.

        Returns
        -------
        None
        """
        self.users_table.create()

    def insert_user(self, username: str, password: str, app_access: str = '') -> None:
        """
        Insert a row in the users-app table.

        Parameters
        ----------
        username: str
            Username chosen by the user
        password: str
            Password chosen by the user
        app_access: str
            Space separated list of apps the user can access
        Returns
        -------
        None
        """
        with self.engine.connect() as conn:
            insert_statement = self.users_table.insert().values(username=username,
                                                                password=pbkdf2_sha256.hash(password),
                                                                app_access=app_access
                                                                 )
            conn.execute(insert_statement)

    def update_user(self, username: str, password: str, app_access: str = '') -> None:
        """
        Update the password and the access for a specific user.
        Parameters
        ----------
        username: str
            Username for which the password/app access must be updated.
        password: str
            Updated password.
        app_access: str
            Updated space separated list of apps the user can access
        Returns
        -------
        None
        """
        with self.engine.connect() as conn:
            # Update password and access to apps
            update_statement = self.users_table.update().where(self.users_table.c.username == username).values(
                password=pbkdf2_sha256.hash(password), app_access=app_access)
            conn.execute(update_statement)

    def delete_user(self, username: str) -> None:
        """
        Delete the row (for the specified username) in the table of the database.

        Parameters
        ----------
        username: str
            Username for the row that has to be deleted
        Returns
        -------
        None
        """
        with self.engine.connect() as conn:
            # Delete
            delete_statement = self.users_table.delete().where(self.users_table.c.username == username)
            conn.execute(delete_statement)

    def connect_to_db(self) -> None:
        """
        Check the connection to the database.

        Returns
        -------
        None
        """
        print("Connecting with engine " + str(self.engine))
        connection = self.engine.connect()
        print(connection)

    def return_table_as_df(self) -> pd.DataFrame:
        """
        Load the users-app table in a panda dataframe.
        Returns
        -------
        df: pd.Dataframe
        """
        df = pd.read_sql_query('select * from "users_app"', con=self.engine)
        return df

    def add_column_to_db(self, col_name, col_type, default_val):
        table = migrate.versioning.schema.Table("users_app", self.meta)
        col = Column(col_name, col_type, default=default_val)
        col.create(table, populate_default=True)
        # Column is added to table based on its name
        assert col is table.c[col_name]
