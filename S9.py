from flask import Flask, request, jsonify

app = Flask(__name__)

medications = {
    "user_1": [
        {
            "id": 1,
            "name": "Aspirin",
            "dosage": "100mg",
            "time": "08:00"
        },
        {
            "id": 2,
            "name": "Vitamin D",
            "dosage": "2000 IU",
            "time": "12:00"
        }
    ]
}

def is_carer(role):
    return role == "carer"

@app.route('/medications/<user_id>', methods=['GET'])
def get_medications(user_id):
    return jsonify({
        "user_id": user_id,
        "medications": medications.get(user_id, [])
    })

@app.route('/update_medication', methods=['POST'])
def update_medication():
    data = request.get_json()

    role = data.get("role")
    user_id = data.get("user_id")
    med_id = data.get("med_id")

    if not all([role, user_id, med_id]):
        return jsonify({"error": "Missing required fields"}), 400

    if not is_carer(role):
        return jsonify({"error": "Permission denied"}), 403

    user_meds = medications.get(user_id)

    if not user_meds:
        return jsonify({"error": "User not found"}), 404

    for med in user_meds:
        if med["id"] == med_id:
            med["name"] = data.get("name", med["name"])
            med["dosage"] = data.get("dosage", med["dosage"])
            med["time"] = data.get("time", med["time"])

            return jsonify({
                "message": "Medication updated successfully",
                "updated_medication": med
            })

    return jsonify({"error": "Medication not found"}), 404

@app.route('/add_medication', methods=['POST'])
def add_medication():
    data = request.get_json()

    user_id = data.get("user_id")
    name = data.get("name")
    dosage = data.get("dosage")
    time = data.get("time")

    if not all([user_id, name, dosage, time]):
        return jsonify({"error": "Missing fields"}), 400

    new_med = {
        "id": len(medications.get(user_id, [])) + 1,
        "name": name,
        "dosage": dosage,
        "time": time
    }

    medications.setdefault(user_id, []).append(new_med)

    return jsonify({
        "message": "Medication added successfully",
        "medication": new_med
    })

@app.route('/delete_medication', methods=['POST'])
def delete_medication():
    data = request.get_json()

    user_id = data.get("user_id")
    med_id = data.get("med_id")

    user_meds = medications.get(user_id, [])

    for med in user_meds:
        if med["id"] == med_id:
            user_meds.remove(med)
            return jsonify({"message": "Medication deleted successfully"})

    return jsonify({"error": "Medication not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
