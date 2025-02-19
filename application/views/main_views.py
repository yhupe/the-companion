from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime
from application.services.forms import UserForm
main = Blueprint("main", __name__)


@main.route("/")
def index():
    return {"message": "I am a Teapot"}, 418


@main.route("/status")
def status():
    return {"API":"🟢",
            "Database": "🟢",
            "Conn_Twilio": "🟢",
            "FOTH_MagicSauce": "🟢"}, 200


@main.route("/registration", methods=["GET", "POST"])
def registration():
    form = UserForm()

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        username = form.username.data
        whatsapp_number = form.whatsapp_number.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        date_created = str(datetime.datetime.now())

        # Print the collected form data to the console (for testing)
        print(f"Username: {username}")
        print(f"WhatsApp Number: {whatsapp_number}")
        print(f"Email: {email}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Date Created: {date_created}")

        # TODO: Add the collected user data to the database here

        return redirect(url_for(
            'main.success_page'))

    return render_template("registration.html", form=form), 200


@main.route("/success")
def success_page():
    return render_template("success.html"), 200


