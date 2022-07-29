from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Cat:
    db_name = 'solo'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.age = db_data['age']
        self.descr = db_data['descr']
        self.color = db_data['color']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cats (name, age, descr, color, user_id) VALUES (%(name)s,%(age)s,%(descr)s,%(color)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cats;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_cats = []
        for row in results:
            all_cats.append( cls(row) )
        return all_cats
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cats WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE cats SET name=%(name)s, age=%(age)s, descr=%(descr)s, color=%(color)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM cats WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_cat(cat):
        is_valid = True
        if len(cat['name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters")
        if cat['age'] == "":
            is_valid = False
            flash("Please enter an age")
        if len(cat['descr']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters")
        if len(cat['color']) < 2:
            is_valid = False
            flash("Color must be at least 2 characters")
        return is_valid