from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200


@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict()), 200


@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()

    new_plant = Plant(
        name=data.get("name"),
        image=data.get("image"),
        price=data.get("price")
    )
    db.session.add(new_plant)
    db.session.commit()

    return jsonify(new_plant.to_dict()), 201


