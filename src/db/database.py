from mysql.connector import pooling


class Database:
    __instance = None

    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

        self.__pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host=self.db_host,
            user=db_user,
            password=self.db_password,
            database=self.db_name,
        )

    def __new__(cls, db_host, db_port, db_name, db_user, db_password):
        if not cls.__instance:
            cls.__instance = super(Database, cls).__new__(cls)
            cls.__instance.__init__(db_host, db_port, db_name, db_user, db_password)
        return cls.__instance

    def get_connection(self):
        """
        Get a connection from the pool.
        """
        return self.__pool.get_connection()

    def close_connection(self, connection):
        """
        Close the connection.
        """
        connection.close()
