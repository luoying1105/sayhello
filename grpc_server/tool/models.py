from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP

from grpc_server.tool._tools import Base


class Message(Base):
    __tablename__ = 'hello'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    body = Column(String(200))
    timestamp = Column(TIMESTAMP, default=datetime.now)

    # def __repr__(self):
    #     return "<Message(name='%s', body='%s', nickname='%s')>" % (
    #         self.name, self.body)
