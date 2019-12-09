import json
from db import Apartments, User, Reviews, land_lord, db
from flask import Flask, request

app = Flask(__name__)
db_filename = 'apartmentfinder.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/api/apartments/')
def get_apartments():
    apartments = Apartments.query.all()
    res = {'success': True, 'data': [c.serialize() for c in apartments]}
    return json.dumps(res), 200


@app.route('/api/apartments/', methods=["POST"])
def create_apartment():
    post_body = json.loads(request.data)
    address = post_body.get('address', '')
    description = post_body.get('description', '')
    landlord = post_body.get('land_lord_username', '')
    id = land_lord.query.filter_by(user_name = landlord).first()
    apartment = Apartments(
        address=address,
        description=description,
        land_lord=id
    )
    db.session.add(apartment)
    db.session.commit()
    return json.dumps({'success': True, 'data': apartment.serialize()}), 201


@app.route('/api/apartment/<int:apartment_id>', methods=['POST'])
def update_apartment(apartment_id):
    post_body = json.loads(request.data)
    apartment = Apartments.query.filter_by(id=apartment_id).first()
    address = post_body.get('address', apartment.address)
    description = post_body.get('description', apartment.description)
    apartment.address = address
    apartment.description = description
    db.session.commit()
    if not apartment:
        return json.dumps({'success': False, 'data': "Apartment not found!"}), 404
    return json.dumps({'success': True, 'data': apartment}), 200


@app.route('/api/apartment/<int:apartment_id>')
def get_apartment(apartment_id):
    apartment = Apartments.query.filter_by(id=apartment_id).first()
    if not apartment:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    return json.dumps({'success': True, 'data': apartment.serialize()}), 200


@app.route('/api/apartment/<int:apartment_id>', methods=["DELETE"])
def delete_apartment(apartment_id):
    apartment = Apartments.query.filter_by(id=apartment_id).first()
    if not apartment:
        return json.dumps({'success': False, 'error': 'Apartment not found!'}), 404
    db.session.delete(apartment)
    db.session.commit()
    return json.dumps({'success': True, 'data': apartment.serialize()}), 200


@app.route('/api/apartment/<int:apartment_id>/reviews/', methods=["POST"])
def create_review(apartment_id):
    apartment = Apartments.query.filter_by(id=apartment_id).first()
    if not apartment:
        return json.dumps({'success': False, 'error': 'Apartment not found!'}), 404
    post_body = json.loads(request.data)
    review = Reviews(
        user_id=post_body.get('user_id'),
        rating=post_body.get('rating', 5),
        review=post_body.get('review', ''),
        apartment_id=apartment_id
    )
    apartment.reviews.append(review)
    db.session.add(review)
    db.session.commit()
    return json.dumps({'success': True, 'data': review.serialize()}), 200


@app.route('/api/users/')
def get_users():
    users = User.query.all()
    res = {'success': True, 'data': [c.serialize() for c in users]}
    return json.dumps(res), 200


@app.route('/api/users/', methods=["POST"])
def create_user():
    post_body = json.loads(request.data)
    username = post_body.get('username')
    if username is None:
        return json.dumps({'success': False, 'error': 'Invalid username!'})
    user = User(
        username=username
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201


@app.route('/api/landlords/', methods=["POST"])
def create_landlord():
    post_body = json.loads(request.data)
    name = post_body.get['name']
    username = post_body.get['username']
    if name is None:
        return json.dumps({'success': False, 'error': 'Invalid username!'})
    landlord = land_lord(name=name, username = username)
    db.session.add(landlord)
    db.session.commit()
    return json.dumps({'success': True, 'data': landlord.serialize()}), 201


@app.route('/api/landlord/<int:landlord_id>')
def get_landlord(landlord_id):
    landlord = land_lord.query.filter_by(id=landlord_id).first()
    if not landlord:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    return json.dumps({'success': True, 'data': landlord.serialize()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
