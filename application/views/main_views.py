from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime
from application.services.forms import UserForm
from application.services.profile_handling import ProfileHandling
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
def user_registration():
    form = UserForm()

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        pf = ProfileHandling()
        whatsapp_number = form.whatsapp_number.data
        user_name = form.user_name.data
        current_date = datetime.now()
        date_created = str(current_date)
        data = {
            user_name : user_name,
            date_created: date_created
        }
        pf.append_storage(data, whatsapp_number)

        # Print the collected form data to the console (for testing)
        print(f"User name: {user_name}")
        print(f"WhatsApp Number: {whatsapp_number}")
        print(f"Date Created: {date_created}")

        # TODO: Add the collected user data to the database here

        return redirect(url_for(
            'main.success_page'))

    return render_template("registration.html", form=form), 200


@main.route("/success")
def success_page():
    return render_template("success.html"), 200


