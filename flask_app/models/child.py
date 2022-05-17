from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import chore
from flask_app.models import parent
import re

USERNAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class Child:
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['f_name']
        self.last_name = data['l_name']
        self.username = data['username']
        self.password = data['password']
        self.parent_id = data['parent_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.parent = parent.Parent.get_one({"id": data['parent_id']})
        self.chores = []

    @staticmethod
    def validate_child(data):
        is_valid = True
        if not USERNAME_REGEX.match(data['username']):
            flash("Please enter a valid username!")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be more than 8 characters!")
            is_valid = False
        return is_valid 

    @classmethod
    def save(cls, data):
        query = "INSERT INTO child (f_name, l_name, username, password, parent_id, created_at, updated_at) VALUES (%(f_name)s, %(l_name)s, %(username)s, %(password)s, %(parent_id)s, NOW(), NOW());"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM child;"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_child_by_username(cls, data):
        query = "SELECT * FROM child WHERE username = %(username)s;"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def edit(cls, data):
        query = "UPDATE child SET f_name = %(f_name)s, l_name = %(l_name)s, username = %(username)s, password = %(password)s, parent_id = %(parent_id)s WHERE id = %(id)s"
        results =  connectToMySQL("chore_tasker").query_db(query, data)
        print(results)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM child WHERE id = %(id)s;"
        results =  connectToMySQL("chore_tasker").query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_child_with_chores(cls, data):
        query = "SELECT * FROM child LEFT JOIN chore ON chore.child_id = child.id WHERE child.username = %(username)s;"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        this_child = cls(results[0])
        print(results)
        for row in results: 
            c_info = {
                "id" : row["chore.id"],
                "name" : row["name"],
                "description" : row["description"],
                "point" : row["point"],
                "day" : row["day"],
                "child_id" : row["child_id"],
                "parent_id": row["chore.parent_id"],
                "created_at" : row["chore.created_at"],
                "updated_at" : row["chore.updated_at"]
            }
            this_child.chores.append(chore.Chore(c_info))
        return this_child