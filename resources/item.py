from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required = True)
    parser.add_argument('store_id', type = int, required = True, help = "Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message" : "Item not found"}
    
    def post(self, name):

        if ItemModel.find_by_name(name):
            return  {"message" : "An item with same name exist"}, 400
            # 400 is bad request.
        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data)      #data['price'], data['store_id']
        
        try:
            item.save_to_db()
        except:
            return {"message" : "An error occurred while inserting the item."}, 500 #internal server error.

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message' : 'Item deleted'}

    def put(self, name):

        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)      #data['price'], data['store_id']
        else:
            item.price = request_data['price']
        
        item.save_to_db()
        return item.json()  


class ItemList(Resource):
    def get(self) :
        return {'items' : [item.json() for item in ItemModel.query.all()]}