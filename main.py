from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


# create a database
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(125), nullable=False)
    country = db.Column(db.String(125), nullable=False )
    rating = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "country": self.country,
            "rating": self.rating
        }



# create routes 
@app.route("/")
def home():
    return jsonify( {"message":"Welcome Travel Rest API"})

@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()

    return jsonify ( [dest.to_dict()] for dest in destinations)

@app.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify ( destination.to_dict())
    else:
        return jsonify ( {"error": "destination not found"} ), 404

# POST
@app.route("/destinations", methods=["POST"])
def add_destination():
    data = request.get_json()

    new_destination = Destination(destination=data["destination"],
                                  country= data["country"],
                                  rating = data["rating"])
    db.session.add(new_destination)
    db.session.commit()

    return jsonify(  new_destination.to_dict() ), 201

# PUT
@app.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()

    desti = Destination.query.get(destination_id)
    if desti:
       desti.destination = data.get("destination", desti.destination)
       desti.country = data.get("country", desti.country)
       desti.rating = data.get("rating", desti.rating)

       db.session.commit()
       return jsonify(  desti.to_dict() )
    
    else:
        return jsonify({"error":"destinaton not found"}), 404


# DELETE
@app.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    data = request.get_json()

    desti = Destination.query.get(destination_id)
    if desti:
       db.session.delete(desti)
       db.session.commit()

       return jsonify(  "destination deleted!!" )
    
    else:
        return jsonify({"error":"delete not doable, destinaton not found"}), 404
    





if __name__ in "__main__":
    app.run(debug=True)

