from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    auditions = relationship("Audition", backref=backref("role"))

    def actors(self):
        return [a.actor for a in self.auditions]

    def locations(self):
        return [a.location for a in self.auditions]

    def lead(self):
        hired = [a for a in self.auditions if a.hired]
        return hired[0] if hired else "no actor has been hired for this role"

    def understudy(self):
        hired = [a for a in self.auditions if a.hired]
        return hired[1] if len(hired) > 1 else "no actor has been hired for understudy for this role"

class Audition(Base):
    __tablename__ = "auditions"

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    def call_back(self):
        self.hired = True
