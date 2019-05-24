from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

from sql import Base
from models import User


class OAuth(OAuthConsumerMixin, Base):
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

def storage(session, auth, google):
    store = SQLAlchemyStorage(OAuth, session, user=auth.current_user, user_required=False)
    google.setstorage(store)
