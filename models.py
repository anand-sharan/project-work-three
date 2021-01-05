def create_classes(db):
    class Pet(db.Model):
        __tablename__ = 'pets'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64))
        lat = db.Column(db.Float)
        lon = db.Column(db.Float)

        def __repr__(self):
            return '<Pet %r>' % (self.name)

    # Creates Classes which will serve as the anchor points for our Tables
#    class Dog(Base):
#        __tablename__ = 'dog'
#        id = Column(Integer, primary_key=True)
#        name = Column(String(255))
#        color = Column(String(255))
#        age = Column(Integer)

#        def __repr__(self):
#            return '<Dog %r>' % (self.name)

#    class Cat(Base):
#        __tablename__ = 'cat'
#        id = Column(Integer, primary_key=True)
#        name = Column(String(255))
#        color = Column(String(255))
#        age = Column(Integer)
#        
#        def __repr__(self):
#            return '<Cat %r>' % (self.name)
    
    return Pet