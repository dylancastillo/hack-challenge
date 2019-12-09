from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartments.id'))
)


class Apartments(db.Model):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    reviews = db.relationship('Reviews', cascade = 'delete')
    land_lord = db.Column(db.Integer, db.ForeignKey('land_lord.id'), nullable = False)

    def __init__(self, **kwargs):
        self.address = kwargs.get('address')
        self.description = kwargs.get('description')
        self.land_lord = kwargs.get('land_lord_id')
        self.reviews = []

    def serialize(self):
        r = []
        for review in self.reviews:
            r.append({'rating': review.rating, 'review': review.review})
        return {
            'id': self.id,
            'address': self.address,
            'description': self.description,
            'Landlord' : land_lord.query.filter_by(id = self.landlord).first().name,
            'reviews': r
        }

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable = False)
    review = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable = False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user id')
        self.rating = kwargs.get('rating')
        self.review = kwargs.get('review')
        self.apartment_id = kwargs.get('apartment id')

    def serialize(self):
        return{
            'id': self.id,
            'user id': self.user_id,
            'rating': self.rating,
            'review': self.review
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    favorites_id = db.relationship('Apartments', secondary = association_table)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.favorites_id = []

    def serialize(self):
        fav = []
        for i in self.favorites_id:
            fav.append(i.serialize())
        return {
            'id' : self.id,
            'username': self.username,
            'favorites' : fav
        }


class land_lord(db.Model):
    __tablename__ = 'land_lord'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    properties = db.relationship('Apartments', cascade = 'delete')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.username = kwargs.get('username')
        self.properties = []

    def serialize(self):
        h = []
        for i in self.properties():
            h.append(i.serialize())
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'properties': h
        }
