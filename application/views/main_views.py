from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return {"message": "I am a Teapot"}, 418


@main.route("/status")
def status():
    return {"message":"Up and running"}, 200
