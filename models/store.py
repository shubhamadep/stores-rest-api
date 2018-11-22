import sqlite3
from db import db


class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy ='dynamic')   #lazy does not create an item object for each item for a store.

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name" : self.name, "items" :  [item.json() for item in self.items.all()]} #Now that we use lazy = 'dynamic', we won't be getting objects to loop through. So self.items will be acting as a query builder.

    @classmethod
    def find_by_name(cls, name):
        
        return cls.query.filter_by(name=name).first()     #select * from items where name = name LIMIT 1

    def save_to_db(self):
        
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()