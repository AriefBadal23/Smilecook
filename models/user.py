from extensions import db
class User(db.Model):
    """ The database model to create a new user account for the application """
    # create a table user
    __tablename__='user'

    # Define the colums we need for our table user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    avatar_image = db.Column(db.String(100), default=None)
    
    recipes = db.relationship('Recipe', backref='user')
   
    # The methods we can use to retrieve data of the table    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # Method to save the entry in the database
    def save(self):
        db.session.add(self)
        db.session.commit()