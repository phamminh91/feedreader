from sqlalchemy import Column, Integer, ForeignKey
from database import DeclarativeBase


class FeedSubscription(DeclarativeBase):

    __tablename__ = 'feedsubscription'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    source_id = Column(Integer, ForeignKey('feedsource.id'))


    def __repr__(self):
        return '<Subscription user_id =%d, source_id=%d>' % (self.user_id, self.source_id)