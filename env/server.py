from form import userForm
from flask import Flask, Response, request, jsonify
from bson import json_util, ObjectId
import bcrypt
import pymongo
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'


# CONNECTING THE DATABASE MONGO DB
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.test
    mongo.server_info()  # trigger exception if cannot connect to database
except:
    print("ERROR: Cannot connect to the database")


@app.route("/register", methods=["GET", "POST"])
def create_user():
    user_collection = db.users
    form = userForm.UserRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']
        password = request.form['password']
        state = request.form['state']
        district = request.form['district']
        municipality = request.form['municipality']
        wardNo = request.form['wardNo']
        address = request.form['address']
        user_existing = user_collection.find_one({'mobileNumber': mobileNumber})
        if user_existing is None:
            hashPassword = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            user = user_collection.insert_one({
                'name': name,
                'email': email,
                'mobileNumber': mobileNumber,
                'password': hashPassword,
                'state': state,
                'district': district,
                'municipality': municipality,
                'wardNo': wardNo,
                'address': address
        })
            return Response(
                response=json.dumps(
                    {"message": "User Created Successfully", "id": f"{user.inserted_id}"}),
                    status=200,
                    mimetype="application/json"
        )
        return Response(
            response=json.dumps(
                {"message": "User already exist"}),
                status=400,
                mimetype="application/json"
        )
    return Response(
        response=json.dumps(
            {"message": "Validation failed"}),
            status=200,
            mimetype="application/json"
)


@app.route("/login", methods=["POST"])
def login():
    user = db.users
    login_user = user.find_one({'email': request.form['email']})
    if login_user:
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
            return Response(
                response=json.dumps(
                    {"message": "User successfully logged in", 'id': f"{login_user}"}),
                status=400,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "Password incorrect"}),
            status=400,
            mimetype="application/json"
        )
    return Response(
        response=json.dumps({"message": "User not found"}),
        status=400,
        mimetype="application/json"
    )


@app.route("/", methods=["GET"])
def get_all():
    user_collections = db.users
    data = list(user_collections.find())
    for user in data:
        user["_id"] = str(user["_id"])
    datas = json.loads(json_util.dumps(data))
    return Response(
        response=json.dumps(
            {'message': "User get successfully", 'user': datas}),
        status=200,
        mimetype="application/json"
    )


@app.route("/update/<id>", methods=["PATCH"])
def update_user(id):

    user_collections = db.users
    user = user_collections.update_one(
        {"_id": ObjectId(id)},
        {"$set": {'district': request.form['district'],
                  'state': request.form['state'],
                  'municipality': request.form['municipality'],
                  'wardNo': request.form['wardNo'],
                  'address': request.form['address']
                  }}
    )
    if user.modified_count == 1:
        return Response(
            response=json.dumps({'message': "User updated successfully"}),
            status=200,
            mimetype="application/json"
        )
    return Response(
        response=json.dumps({'message': "Nothing to update"}),
        status=200,
        mimetype="application/json"
    )


@app.route('/delete/<id>', methods=["DELETE"])
def delete_user(id):
    user_collections = db.users
    user = user_collections.delete_one({"_id": ObjectId(id)})
    if user.deleted_count == 1:
        return Response(
            response=json.dumps({'message': "User deleted successfully"}),
            status=200,
            mimetype="application/json"
        )
    return Response(
        response=json.dumps({'message': "Nothing to delete"}),
        status=200,
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(port=3500, debug=True)
