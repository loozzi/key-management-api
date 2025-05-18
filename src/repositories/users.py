from src import db


class UserRepository:
    def __init__(self):
        self.cnx = db.get_connection()
        self.cursor = self.cnx.cursor()
        self.table_name = "users"

    def get_by_token(self, token: str):
        """
        Get user by token.
        """
        query = f"SELECT * FROM {self.table_name} WHERE token = %s"
        self.cursor.execute(query, (token,))
        result = self.cursor.fetchone()
        if result:
            return self.__serialize__(result)
        return None

    def get_by_username(self, username: str):
        """
        Get user by username.
        """
        query = f"SELECT * FROM {self.table_name} WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result:
            return self.__serialize__(result)
        return None

    def get_password(self, username: str):
        """
        Get user password by username.
        """
        query = f"SELECT password_hash FROM {self.table_name} WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def __repr__(self):
        return f"UserRepository(table_name={self.table_name})"

    def __serialize__(self, user):
        """
        Serialize user object to dictionary.
        """
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "token": user[3],
        }
