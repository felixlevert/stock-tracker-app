from flask.cli import FlaskGroup

from src import db, app


cli = FlaskGroup(app)


# Create DB schema from scratch
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()