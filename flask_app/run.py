"""Flask CLI/Application entry point."""
import os

import click

from backend_api import create_app, db
from backend_api.models.token_blacklist import BlacklistedToken
from backend_api.models.user import User
from backend_api.models.datatest import Datatest

CONFIG = os.getenv("FLASK_ENV", "production")
app = create_app(CONFIG)


@app.route("/")
def flask_landing():
    return f"""
        <b>Flask App Index Page</b>
        <br>
        Your app is set to config: {CONFIG}
        <br>
        There really is nothing to see here...
        <br>
        Header over to 
        <a href="https://api.the-ripple-effect.app/api/v1/ui"> The Swagger Page </a>
    """

@app.shell_context_processor
def shell():
    return {
        "db": db,
        "User": User,
        "BlacklistedToken": BlacklistedToken,
        "Datatest": Datatest
    }


@app.cli.command("add-user", short_help="Add a new user")
@click.argument("email")
@click.option(
    "--admin", is_flag=True, default=False, help="New user has administrator role"
)
@click.password_option(help="Do not set password on the command line!")
def add_user(email, admin, password):
    """Add a new user to the database with email address = EMAIL."""
    if User.find_by_email(email):
        error = f"Error: {email} is already registered"
        click.secho(f"{error}\n", fg="red", bold=True)
        return 1
    new_user = User(email=email, password=password, admin=admin)
    db.session.add(new_user)
    db.session.commit()
    user_type = "admin user" if admin else "user"
    message = f"Successfully added new {user_type}:\n {new_user}"
    click.secho(message, fg="blue", bold=True)
    return 0