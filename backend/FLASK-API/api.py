# Import necessary libraries and modules
from flask import Flask  # Flask is used to create the web application
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy is used for database interactions
from datetime import datetime  # Used to handle date and time
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort  # Flask-RESTful for building REST APIs

# Initialize the Flask application, database, api, and configure the database URI
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

api = Api(app)

# Define the schema for User, Location, Box, and Item models
class User(db.Model):
    __tablename__ = 'users'  # Name of the table in the database
    user_id = db.Column(db.Integer, primary_key=True)  
    first_name = db.Column(db.String(50), nullable=False)  
    last_name = db.Column(db.String(50), nullable=False)  
    email = db.Column(db.String(50), unique=True, nullable=False)  
    password = db.Column(db.String(50), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    # For debugging
    def __repr__(self):
        return f"User(user_id={self.user_id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"


class Location(db.Model):
    __tablename__ = 'locations' 
    location_id = db.Column(db.Integer, primary_key=True)  
    location_creator = db.Column(db.Integer, nullable=False)  
    location_name = db.Column(db.String(50), nullable=False)
    location_category = db.Column(db.String(50), nullable=False) 
    location_address = db.Column(db.String(50), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"Location(location_id={self.location_id}, location_name='{self.location_name}', location_category='{self.location_category}', location_address='{self.location_address}')"


class Box(db.Model):
    __tablename__ = 'box'  
    box_id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False) 
    box_type = db.Column(db.String(50), nullable=False)   
    box_name = db.Column(db.String(50), nullable=False)  
    box_description = db.Column(db.String(50), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    
    def __repr__(self):
        return f"Box(box_id={self.box_id}, box_name='{self.box_name}', box_type='{self.box_type}')"


class Item(db.Model):
    __tablename__ = 'item' 
    item_id = db.Column(db.Integer, primary_key=True)  
    box_id = db.Column(db.Integer, db.ForeignKey('box.box_id'), nullable=False)  
    item_creator = db.Column(db.Integer, nullable=False)  
    item_name = db.Column(db.String(50), nullable=False)  
    item_image_ref = db.Column(db.String(50), nullable=False)  
    item_category = db.Column(db.String(50), nullable=False)  
    item_description = db.Column(db.String(50), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"Item(item_id={self.item_id}, item_name='{self.item_name}', item_category='{self.item_category}', item_description='{self.item_description}')"

class Box_Access(db.Model):
    __tablename__ = 'box_access'    
    user_id = db.Column(db.Integer, nullable=False)
    box_id = db.Column(db.Integer, nullable=False)
    access_level = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the composite primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'box_id'),  # Composite primary key
    )

    def __repr__(self):
        return f"Box_Access(user_id={self.user_id}, box_id={self.box_id}, access_level='{self.access_level}')"

class RequestParsers:
    @staticmethod
    def user_parser():
        
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, help='First name is required', required=True)
        parser.add_argument('last_name', type=str, help='Last name is required', required=True)
        parser.add_argument('email', type=str, help='Email is required', required=True)
        parser.add_argument('password', type=str, help='Password is required', required=True)
        return parser

    @staticmethod
    def location_parser():
        
        parser = reqparse.RequestParser()
        parser.add_argument('location_creator', type=int, help='Location creator is required', required=True)
        parser.add_argument('location_name', type=str, help='Location name is required', required=True)
        parser.add_argument('location_category', type=str, help='Location category is required', required=True)
        parser.add_argument('location_address', type=str, help='Location address is required', required=True)
        return parser

    @staticmethod
    def box_parser():
        
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, help='User ID is required', required=True)
        parser.add_argument('location_id', type=int, help='Location ID is required', required=True)
        parser.add_argument('box_creator', type=int, help='Box creator is required', required=True)
        parser.add_argument('box_type', type=str, help='Box type is required', required=True)
        parser.add_argument('box_name', type=str, help='Box name is required', required=True)
        parser.add_argument('box_description', type=str, help='Box description is required', required=True)
        return parser

    @staticmethod
    def item_parser():
        
        parser = reqparse.RequestParser()
        parser.add_argument('box_id', type=int, help='Box ID is required', required=True)
        parser.add_argument('item_creator', type=int, help='Item creator is required', required=True)
        parser.add_argument('item_name', type=str, help='Item name is required', required=True)
        parser.add_argument('item_image_ref', type=str, help='Item image reference is required', required=True)
        parser.add_argument('item_category', type=str, help='Item category is required', required=True)
        parser.add_argument('item_description', type=str, help='Item description is required', required=True)
        return parser

    @staticmethod
    def box_access_parser():
        
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, help='User ID is required', required=True)
        parser.add_argument('box_id', type=int, help='Box ID is required', required=True)
        parser.add_argument('access_level', type=str, help='Access level is required', required=True)
        return parser

# Define a class for db models into API responses
class SerializationFields:

    user_fields = {
        'user_id': fields.Integer,
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }


    location_fields = {
        'location_id': fields.Integer,
        'location_creator': fields.Integer,
        'location_name': fields.String,
        'location_category': fields.String,
        'location_address': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }


    box_fields = {
        'box_id': fields.Integer,
        'user_id': fields.Integer,
        'location_id': fields.Integer,
        'box_creator': fields.Integer,
        'box_type': fields.String,
        'box_name': fields.String,
        'box_description': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }


    item_fields = {
        'item_id': fields.Integer,
        'box_id': fields.Integer,
        'item_creator': fields.Integer,
        'item_name': fields.String,
        'item_image_ref': fields.String,
        'item_category': fields.String,
        'item_description': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    box_access_fields = {
        'user_id': fields.Integer,
        'box_id': fields.Integer,
        'access_level': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

# For handling User-related API requests
class UserResource(Resource):
    @marshal_with(SerializationFields.user_fields)  
    def get(self):
       
        users = User.query.all()
        return users

    @marshal_with(SerializationFields.user_fields)
    def post(self):
        # Parse the incoming request data
        parser = RequestParsers.user_parser()
        args = parser.parse_args()
        # Create a new User object
        new_user = User(
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            password=args['password']
        )
        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

class LocationResource(Resource):
    @marshal_with(SerializationFields.location_fields)
    def get(self):

        locations = Location.query.all()
        return locations

    @marshal_with(SerializationFields.location_fields)
    def post(self):

        parser = RequestParsers.location_parser()
        args = parser.parse_args()

        new_location = Location(
            location_creator=args['location_creator'],
            location_name=args['location_name'],
            location_category=args['location_category'],
            location_address=args['location_address']
        )

        db.session.add(new_location)
        db.session.commit()
        return new_location, 201

# Define a resource for handling Box-related API requests
class BoxResource(Resource):
    @marshal_with(SerializationFields.box_fields)
    def get(self):
        boxes = Box.query.all()
        return boxes

    @marshal_with(SerializationFields.box_fields)
    def post(self):
        parser = RequestParsers.box_parser()
        args = parser.parse_args()
        new_box = Box(
            user_id=args['user_id'],
            location_id=args['location_id'],
            box_creator=args['box_creator'],
            box_type=args['box_type'],
            box_name=args['box_name'],
            box_description=args['box_description']
        )

        db.session.add(new_box)
        db.session.commit()
        return new_box, 201


class ItemResource(Resource):
    @marshal_with(SerializationFields.item_fields)
    def get(self):

        items = Item.query.all()
        return items

    @marshal_with(SerializationFields.item_fields)
    def post(self):

        parser = RequestParsers.item_parser()
        args = parser.parse_args()

        new_item = Item(
            box_id=args['box_id'],
            item_creator=args['item_creator'],
            item_name=args['item_name'],
            item_image_ref=args['item_image_ref'],
            item_category=args['item_category'],
            item_description=args['item_description']
        )

        db.session.add(new_item)
        db.session.commit()
        return new_item, 201
    

class BoxAccessResource(Resource):
    @marshal_with(SerializationFields.box_access_fields)
    def get(self):
        # Fetch all box access records
        box_access_records = Box_Access.query.all()
        return box_access_records

    @marshal_with(SerializationFields.box_access_fields)
    def post(self):
        # Parse the incoming request data
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, help='User ID is required', required=True)
        parser.add_argument('box_id', type=int, help='Box ID is required', required=True)
        parser.add_argument('access_level', type=str, help='Access level is required', required=True)
        args = parser.parse_args()

        # Create a new Box_Access record
        new_access = Box_Access(
            user_id=args['user_id'],
            box_id=args['box_id'],
            access_level=args['access_level']
        )

        db.session.add(new_access)
        db.session.commit()
        return new_access, 201


# Define a class for validating if records already exist in the database
class Validators:
    @staticmethod
    def check_user_exists(user_id):
        # Check if a user with the given ID exists
        user = User.query.get(user_id)
        if user:
            abort(400, message=f"User with ID {user_id} already exists.")

    @staticmethod
    def check_location_exists(location_id):
        location = Location.query.get(location_id)
        if location:
            abort(400, message=f"Location with ID {location_id} already exists.")

    @staticmethod
    def check_box_exists(box_id):
        box = Box.query.get(box_id)
        if box:
            abort(400, message=f"Box with ID {box_id} already exists.")

    @staticmethod
    def check_item_exists(item_id):
        item = Item.query.get(item_id)
        if item:
            abort(400, message=f"Item with ID {item_id} already exists.")

    @staticmethod
    def check_box_access_exists(user_id, box_id):
        box_access = Box_Access.query.filter_by(user_id=user_id, box_id=box_id).first()
        if box_access:
            abort(400, message=f"Box access for user {user_id} and box {box_id} already exists.")

# For registering API resources
class APIResources:
    @staticmethod
    def register_resources(api):
        # Generic registry
        api.add_resource(UserResource, '/api/users')
        api.add_resource(LocationResource, '/api/locations')
        api.add_resource(BoxResource, '/api/boxes')
        api.add_resource(ItemResource, '/api/items')
        api.add_resource(BoxAccessResource, '/api/box_access')

class APIResourcesWithID:
    @staticmethod
    def register_resources(api):
        # For verifying specific users
        api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
        api.add_resource(LocationResource, '/api/locations', '/api/locations/<int:location_id>')
        api.add_resource(BoxResource, '/api/boxes', '/api/boxes/<int:box_id>')
        api.add_resource(ItemResource, '/api/items', '/api/items/<int:item_id>')
        api.add_resource(BoxAccessResource, '/api/box_access', '/api/box_access/<int:user_id>/<int:box_id>')

# Register all resources
APIResources.register_resources(api)

# Define a route for the home page
@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)