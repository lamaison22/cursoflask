import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import items
from db import stores

blp = Blueprint("item",__name__,description="Operations on items")
@blp.route("/store/<string:store_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:        
            abort(404,message="store not found")

    def delete(self,item_id):
        try:
            del(items[item_id])
            return {"message":"loja deletada"}
        except KeyError:
            abort(404,message="Loja nao encontrada") 
            
    def put(self,item_id):
        item_data=request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(404,"Bad request faltou preco ou nome")
        try:
            item=items[item_id]
            item |=item_data #novo comando q atualiza dictionarys direto
            return item
        except KeyError:
            abort(404,message="item nao encontrado")

@blp.route("/item")


class ItemList(MethodView):
    def get(self):
     return{"items":list(items.values())}

    def post(self):
        item_data=request.get_json()
        if(
            "price" not in item_data 
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(400,message="Bad request. Granta que todos os atributos estejam presentes")
        
        for item in items.values():
            if(item_data["name"]==item["name"] and item_data["store_id"]==item["store_id"]):
                abort(400,message="ja existe")
                
        if item_data["store_id"] not in stores:
            abort(404,message="nao encontrada")
            
        item_id=uuid.uuid4().hex    
        item = {**item_data,"id":item_id}
        items[item_id]=item
        
        return item,201
