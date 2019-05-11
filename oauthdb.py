from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sql import Base
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

class OAuth(OAuthConsumerMixin, Base):
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)
