from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ... other columns as needed

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

# get_current_user() is a function that returns the current logged in user
blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=get_current_user)
