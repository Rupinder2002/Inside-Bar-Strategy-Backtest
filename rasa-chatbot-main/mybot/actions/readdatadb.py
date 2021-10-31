from typing import Any, Text
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
#from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, VARCHAR,Text
from sqlalchemy import engine
from sqlalchemy.engine.interfaces import CreateEnginePlugin
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.sqltypes import DateTime, SmallInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Botapp_fundingprogramtbl(Base):
    __tablename__ = 'botapp_fundingprogramtbl'
    id = Column(Integer, primary_key= True)
    program_name = Column(String)
    about_program = Column(String(128))
    who_can_apply = Column(TEXT)
    deadline = Column(TEXT)
    how_to_apply = Column(TEXT)
    link = Column(TEXT) 
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    language = Column(VARCHAR(512))
    program_id = Column(VARCHAR(512))
    keywords = Column(VARCHAR(512))
    programTypeId = Column(VARCHAR(512))
    statusId = Column(VARCHAR(512))
    reserveId = Column(VARCHAR(512))
    eligibility = Column(TEXT) 

    def __repr__(self):
        return "<Botapp_fundingprogramtbl(id= '%d', program_name= '%s', about_program='%s', who_can_apply = '%s', deadline='%s', how_to_apply= '%s', link = '%s', created_at='%s', updated_at='%s', language = '%s', program_id='%s', keywords = '%s', programTypeId = '%s',statusId = '%s',reserveId = '%s',eligibility = '%s')>" % (
                                self.id, self.program_name, self.about_program, self.who_can_apply, self.deadline, self.how_to_apply, self.link, self.created_at, self.updated_at, self.language, self.program_id, self.keywords,self.programTypeId,self.statusId,self.reserveId,self.elgibility)

def fetch_about_program(program_name):
    #program_name = 'Education Partnerships Program'
    engine = create_engine("mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance")
    metadata = sqlalchemy.MetaData()
    #Botapp_fundingprogramtbl = Table('botapp_fundingprogramtbl', metadata, autoload=True, autoload_with=engine)
    #print(botapp_fundingprogramtbl.columns.keys())
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    bottab = session.query(Botapp_fundingprogramtbl).filter(Botapp_fundingprogramtbl.program_name == program_name).first()
    return bottab.about_program   

def fetch_who_can_apply(program_name):
    #program_name = 'Education Partnerships Program'
    engine = create_engine("mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance")
    metadata = sqlalchemy.MetaData()
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    bottab = session.query(Botapp_fundingprogramtbl).filter(Botapp_fundingprogramtbl.program_name == program_name).first()
    return bottab.who_can_apply   

def fetch_deadline(program_name):
    #program_name = 'Education Partnerships Program'
    engine = create_engine("mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance")
    metadata = sqlalchemy.MetaData()
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    bottab = session.query(Botapp_fundingprogramtbl).filter(Botapp_fundingprogramtbl.program_name == program_name).first()
    return bottab.deadline   

def fetch_how_to_apply(program_name):
    #program_name = 'Education Partnerships Program'
    engine = create_engine("mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance")
    metadata = sqlalchemy.MetaData()
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    bottab = session.query(Botapp_fundingprogramtbl).filter(Botapp_fundingprogramtbl.program_name == program_name).first()
    return bottab.how_to_apply 

def fetch_link(program_name):
    #program_name = 'Education Partnerships Program'
    engine = create_engine("mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance")
    metadata = sqlalchemy.MetaData()
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    bottab = session.query(Botapp_fundingprogramtbl).filter(Botapp_fundingprogramtbl.program_name == program_name).first()
    return bottab.link 
        
    
    #connection = engine.connect() 
    #query = sqlalchemy.select([botapp_fundingprogramtbl.columns.about_program]).where(botapp_fundingprogramtbl.columns.program_name == program_name)
    #result=  connection.execute(query)
    #res = result.fetchone()
    #return res


    #result = fetch_about_program(program_name)
    #print (result)