import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
#from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import engine
from sqlalchemy.engine.interfaces import CreateEnginePlugin
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.sqltypes import SmallInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key= True)
    realm = Column(String(512))
    username = Column(String(512))
    password = Column(String(512))
    email = Column(String(512))
    emailVerified = Column(SmallInteger)
    verificationToken = Column(String(512)) 
    userLanguage = Column(String(512))
    

    def __repr__(self):
        return "<testuserbot(id= '%d', realm= '%s', username='%s', password = '%s', email='%s', emailVerified= '%d', verificationToken = '%s', userLanguage='%s')>" % (
                                self.id, self.realm, self.username, self.password, self.email, self.emailVerified, self.verificationToken, self.userLanguage)

def UpdateUserDetails( username,email, userLanguage, password):
    #engine = create_engine("mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance")
    engine = create_engine("mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance")
    metadata = MetaData()
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    update_user = user ( username =username,  email = email, userLanguage = userLanguage, password = password )
    session.add(update_user)
    session.commit()






#class testuserbot(Base):
 #   __tablename__ = 'testuserbot'
  #  name = Column(String(255), primary_key= True)
   # email = Column(String(255))
    #language = Column(String(250))












#testuserbot = Table ('testuserbot', metadata,
 #               Column ('name', String(255) ), 
  #              Column ('email', String(255)),
   #             Column ('language', String(255)))
#metadata.create_all(engine)
#Base.metadata.create_all(engine)
    


    


   
