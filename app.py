import uuid
from flask import Flask, request
from db import stores

app = Flask(__name__)


@app.get("/store") #http://127.0.01:5000/store
def get_stores():
    return{"stores": list(stores.values())}

@app.get("/store/<string:id>")
def get_store(id):
    try:
            return stores["store_id"]
    except KeyError:
        return{"message" : "store not found"}, 404

@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"]==name:
            return {"items": store["items"]}
    return {"message":"store not found"}, 404

@app.post("/store") 
def create_stores():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id":store_id}
    stores.append(store)
    return store, 201

@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get.json()
    for store in stores:
        if store["name"]==name:
            new_item={"name":request_data["name"], "price":request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message":"store not found"}, 404