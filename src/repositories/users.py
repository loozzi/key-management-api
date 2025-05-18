from src import db


class UserRepository:
    def __init__(self):
        self.cnx = db.get_connection()
        self.cursor = self.cnx.cursor()
        self.table_name = "users"

    def get_by_id(self, user_id: int):
        """
        Get user by ID.
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        if result:
            return self.__serialize__(result)
        return None

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

    def get_by_email(self, email: str):
        """
        Get user by email.
        """
        query = f"SELECT * FROM {self.table_name} WHERE email = %s"
        self.cursor.execute(query, (email,))
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

    def create_user(self, username: str, password_hash: str, email: str) -> bool:
        """
        Create a new user.
        """
        try:
            query = f"INSERT INTO {self.table_name} (username, password_hash, email) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, password_hash, email))
            self.cnx.commit()
            return True
        except Exception as e:
            self.cnx.rollback()
            print(f"Error creating user: {e}")
            return False

    def update_token(self, user_id: int, token: str) -> bool:
        """
        Update user token.
        """
        try:
            query = f"UPDATE {self.table_name} SET token = %s WHERE id = %s"
            self.cursor.execute(query, (token, user_id))
            self.cnx.commit()
            return True
        except Exception as e:
            self.cnx.rollback()
            print(f"Error updating token: {e}")
            return False

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
