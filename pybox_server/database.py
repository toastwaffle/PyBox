from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, desc, Enum
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref, sessionmaker

from libpybox.sqlbase import PyBoxSQL

import os.path
import random
random.seed()

Base = declarative_base()

class Client(PyBoxSQL,Base):

    name = Column(String, nullable=False)
    authkey = Column(Integer, nullable=False)
    authorised = Column(Boolean, nullable=False)

    def __init__(self, name, authorised=False):
        self.name = name
        self.authorised = authorised
        self.authkey = random.randint(100000, 999999)

    def __repr__(self):
        return "<Client '%s', %s authorised>" % (self.name, ('is' if self.authorised else 'isn\'t'))

    def authorise(self, authkey):
        if authkey == self.authkey:
            self.authorised = True
            return True
        else:
            return False


class Folder(PyBoxSQL,Base):

    name = Column(String)
    parent_id = Column(Integer, ForeignKey('folder.id'), nullable=True)

    parent = relationship('Folder', backref=backref('children', order_by=name))

    def __init__(self,name,parent_id=None):
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        return "<Folder('%s', parent %s)>" % (self.name, self.parent_id)


class File(PyBoxSQL,Base):

    folder_id = Column(Integer, ForeignKey('folder.id'), nullable=False)
    name = Column(String, nullable=False)
    last_updated_client = Column(Integer, ForeignKey('client.id'), nullable=False)
    deleted = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey('file.id'), nullable=True)

    folder = relationship('Folder', backref=backref('files', order_by=name))

    def __init__(self, folder_id, name, last_updated_client):
        self.folder_id = folder_id
        self.name = name
        self.last_updated_client = last_updated_client

    def __repr__(self):
        return "<File(%s, in %s, updated by client %s)>" % (self.name, self.folder_id, self.last_updated_client)


class Object(PyBoxSQL,Base):

    file_id = Column(Integer, ForeignKey('file.id'))
    sha512 = Column(String(128), nullable=False)

    file = relationship('File', backref=backref('objects', order_by=updated_at.desc()))

    def __init__(self, file_id, sha512):
        self.file_id = file_id
        self.sha512 = sha512

    def __repr__(self):
        return "<Object(%s, file %s, version %s)>" % (self.sha512[0:10], self.file.name, self.updated_at)

class Log(Base):
    __tablename__ = log

    id = Column(Integer, primary_key=True)
    type = Column(Enum('add', 'delete', 'revert', 'client', 'move', 'undelete', 'cleanup', 'folder'), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    def __init__(self,type,message):
        self.type = type
        self.message = message

    def __repr__(self):
        return "%s : %s - %s" % (self.timestamp, self.type.capitalize(), self.message)

class DBHandler(object):

    def __init__(self,db_location=None):
        if db_location == None:
            self.database = os.path.join(os.path.expanduser('~'), '.PyBoxServer/database.sqlite')
        else
            self.database = db_location

        self.engine = create_engine('sqlite://' + database, echo=True)
        self.session = sessionmaker(bind=self.engine)

    def get_file_object(self,file):
        return self.session.query(Object).order_by(Object.updated_at.desc()).filter_by(Object.file_id == File.id)[0]