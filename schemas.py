#Marshmallow schema is a class that defines the fields of the data structure and how they should be 
# converted to and from Python types.
from marshmallow import Schema, fields

#defining different Marshmallow schemas for serializing and deserializing data structures in Python.

#The PlainReviewSchema class is defined by subclassing 
#"Schema" and declaring several fields using the "fields" module.
class PlainReviewSchema(Schema):
    id = fields.Str(dump_only=True) 
    #"dump_only" means it will only be included in the serialized data 
    #(i.e., when using the dump method), and will not be used when 
    #deserializing data (i.e., when using the load method).
    body = fields.Str(required=True)
    sentiment = fields.Str(required=False)
    product_id = fields.Str(required=True)

class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    overall_satisfaction = fields.Float(required=False)
    
class ReviewUpdateSchema(Schema):
    body = fields.Str()
    product_id = fields.Int()
    
class ReviewSchema(PlainReviewSchema): #a subclass of PlainReviewSchema
    product_id = fields.Int(required=True, load_only=True) 
    #modifies the product_id field to be of type Int and is marked as load_only, 
    #which means it will only be used when deserializing data (i.e., when using the load method), 
    #and will not be included in the serialized data (i.e., when using the dump method).
    product = fields.Nested(PlainProductSchema(), dump_only=True) 
    #adds an additional field "product" of type Nested and associated with the PlainProductSchema, 
    #which means that it will contain the serialized representation of a PlainProduct data structure.

class ProductSchema(PlainProductSchema): #a subclass of PlainProductSchema
    reviews = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)
    #adds an additional field "reviews" of type List and contains nested fields that are associated 
    #with the PlainReviewSchema, which means that it will contain a list of the serialized representations 
    #of PlainReview data structures.

