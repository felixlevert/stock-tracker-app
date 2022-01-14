from flask.cli import FlaskGroup

from src import db, app


cli = FlaskGroup(app)

# Create DB schema from scratch
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Create a user to speed up testing.
@cli.command("seed_db")
def create_user():
    db.session.add(User(name="test", password="test", email="test@test.org"))
    db.session.commit()


if __name__ == "__main__":
    cli()