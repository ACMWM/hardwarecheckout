from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

from models import Base, User
import auth


class OAuth(OAuthConsumerMixin, Base):
    user_id = Column(String, ForeignKey(User.id))
    user = relationship(User)

def storage(session, googlebp):
    store = SQLAlchemyStorage(OAuth, session, user=auth.current_user, user_required=False)
    googlebp.setstorage(store)
