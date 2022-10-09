import os

from flask import Flask, request

from users_model import UsersModel
from users_responses import UsersResponses

app = Flask(__name__)
model = UsersModel(
    db_host=os.getenv("POSTGRES_HOST", "localhost"),
    db_port=int(os.getenv("POSTGRES_PORT", 5432)),
    db_user=os.getenv("POSTGRES_USER", "postgres"),
    db_password=os.getenv("POSTGRES_PASSWORD", ""),
    db_name=os.getenv("POSTGRES_DB", "postgres"),
)


@app.post("/add_user")
def add_user():
    if request.is_json:
        user_data = request.get_json()
        if UsersModel.is_user_data_valid(user_data):
            user_id = model.set_user_data(user_data)
            return UsersResponses.ok(user_id=user_id)
        return UsersResponses.invalid_json_format()
    return UsersResponses.invalid_request_body_data_type()


@app.get("/get_user/<user_id>")
def get_user(user_id):
    user_data = model.get_user_data(user_id)
    if user_data:
        return UsersResponses.ok(user_data=user_data)
    return UsersResponses.user_not_found()


@app.put("/update_user/<user_id>")
def update_user(user_id):
    if request.is_json:
        new_user_data = request.get_json()
        if UsersModel.is_user_data_valid(new_user_data):
            user_changed = model.set_user_data(new_user_data, user_id)
            if user_changed:
                return UsersResponses.ok(message="Successfully changed")
            return UsersResponses.user_not_found()
        return UsersResponses.invalid_json_format()
    return UsersResponses.invalid_request_body_data_type()


@app.delete("/delete_user/<user_id>")
def delete_user(user_id):
    deleted = model.delete_user_data(user_id)
    if deleted:
        return UsersResponses.ok(message="Successfully deleted")
    return UsersResponses.user_not_found()
