from flask import request, jsonify
from config import app , db
from models import Contact

@app.route("/contact", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contact = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contact})

@app.route("/create_contact", methods=["POST"])
def cereate_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    # retriving data from database and checking if values exsist
    if not first_name or not last_name or not email:
        return(
                jsonify({"message":"you must include first name, last name and email"}),
                400,
            )
    # creating new collumn in database and adding it in to it
    new_contact  = Contact(first_name = first_name, last_name = last_name, email = email)
    try:
        db.session.add(new_contact)
        db.session.commit()

    # carching exeptions
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message":"user created"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "user not found"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message":"user updated"}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "user not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "user has been deleted"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)