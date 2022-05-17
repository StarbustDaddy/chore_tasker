from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import child
from flask_app.models import parent

class Chore:
    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.point = data['point']
        self.day = data['day']
        self.parent_id = data['parent_id']
        self.child_id = data['child_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO chore(name, description, point, day, child_id, parent_id, created_at, updated_at) VALUES(%(name)s, %(description)s, %(point)s, %(day)s, %(child_id)s, %(parent_id)s, NOW(), NOW());"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM chore WHERE id = %(id)s;"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_all_chores_for_parent(cls, data):
        query = "SELECT * FROM chore WHERE parent_id = %(parent_id)s;"
        results = connectToMySQL("chore_tasker").query_db(query, data)
        print(results)
        chores = []
        for c in results:
            chores.append(cls[c])
        return chores

    @classmethod
    def edit(cls, data):
        query = "UPDATE chore SET name = %(name)s, description = %(description)s, point = %(point)s, day = %(day)s WHERE id = %(id)s"
        results =  connectToMySQL("chore_tasker").query_db(query, data)
        print(results)
        return results

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM chore WHERE id = %(id)s;"
        return connectToMySQL('chore_tasker').query_db(query,data)
