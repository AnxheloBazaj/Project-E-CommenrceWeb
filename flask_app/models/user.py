from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = "e-commerce.shcema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.lasr_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if result:
            for user in result:
                users.append(user)
            return users

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    @staticmethod
    def validate_user(data):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(data['first_name']) < 3:
            flash("Username should be at least 3 characters!", 'first_nameRegister')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Username should be at least 3 characters!", 'last_nameRegister')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password should be at least 8 characters!", 'passwordRegister')
            is_valid = False
        if data['password'] != data['confirmpassword']:
            flash("Password should match!", 'confirmPasswordRegister')
            is_valid = False
        return is_valid