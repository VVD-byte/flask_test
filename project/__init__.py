from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
import sys
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData


app = Flask(__name__)
api = Api(app, prefix='/api/v1')
auth = HTTPBasicAuth()

Base = declarative_base()
engine = create_engine('sqlite:////home/vova/PycharmProjects/flask_test/test.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

from project import models, urls, views

Base.metadata.create_all(engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



