from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import child
from flask_app.models import chore
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Parent:
    def __init__( self, data ):
        self.id = data['id']
        self.f_name = data['f_name']
        self.l_name = data['l_name']
        self.email = data['email']
        self.password = data['password']
        self.award = data['award']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.children = []
        self.chores = []

    @staticmethod
    def validate_parent(data):
        is_valid = True
        if len(data['f_name']) < 2:
            flash("Please enter a valid first name!")
            is_valid = False
        if len(data['l_name']) < 2:
            flash("Please enter a valid last name!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please enter a valid email address!")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be more than 8 characters!")
            is_valid = False
        if data['password'] != data['c_password']:
            flash("Passwords do not match!")
            is_valid = False
        return is_valid    

    @classmethod
    def save(cls, data):
        query = "INSERT INTO parent (f_name, l_name, email, password, created_at, updated_at) VALUES (%(f_name)s, %(l_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM parent;"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_parent_by_email(cls, data):
        query = "SELECT * FROM parent WHERE email = %(email)s;"
        results = connectToMySQL('chore_tasker').query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def get_all_children_with_parent( cls , data ):
        query = "SELECT * FROM parent LEFT JOIN child ON child.parent_id = parent.id WHERE parent.id = %(id)s;"
        results = connectToMySQL('chore_tasker').query_db( query , data )
        this_parent = cls(results[0])
        for row in results: 
            c_info = {
                "id" : row["child.id"],
                "f_name" : row["child.f_name"],
                "l_name" : row["child.l_name"],
                "username" : row["username"],
                "password" : row["child.password"],
                "parent_id" : row["parent_id"],
                "created_at" : row["child.created_at"],
                "updated_at" : row["child.updated_at"]
            }
            this_parent.children.append(child.Child(c_info))
        return this_parent
        
    @classmethod
    def get_all_chores_with_parent( cls , data ):
        query = "SELECT * FROM parent LEFT JOIN chore ON chore.parent_id = parent.id WHERE parent.id = %(id)s;"
        results = connectToMySQL('chore_tasker').query_db( query , data )
        cur_parent = cls(results[0])
        for row in results: 
            chore_info = {
                "id" : row["chore.id"],
                "name" : row["name"],
                "description" : row["description"],
                "point" : row["point"],
                "day" : row["day"],
                "child_id" : row["child_id"],
                "parent_id": row["parent_id"],
                "created_at" : row["chore.created_at"],
                "updated_at" : row["chore.updated_at"]
            }
            cur_parent.chores.append(chore.Chore(chore_info))
        return cur_parent