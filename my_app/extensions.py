import redis
from flask_sqlalchemy import SQLAlchemy

from my_app import settings

###############################################################################
# autocommit has been set to True so you don't have to call                   #
# db.session.commit() explicitly, a call to db.session.flush() will also      #
# commit the DB operation, unless you are inside a transaction, only then a   #
# call to db.session.flush() will not commit the DB operation and rather you  #
# need to call commit explicitly.                                             #
#                                                                             #
# We also assume that you will need transaction when there are more than one  #
# DB operations or some business logic followed after a DB operation and to   #
# commit only if all the operations pass or rollback if one of those fails.   #
# To get such behaviour you can use the transactional() decorator imported    #
# from sports_ops.decorators. You still won't have to call                    #
# db.session.commit() explicitly.                                             #
#                                                                             #
# Example usage of transactional() decorator:                                 #
# -------------------------------------------                                 #
#                                                                             #
# @transactional()                                                            #
# def some_method(self, arguments):                                           #
#                                                                             #
###############################################################################
db = SQLAlchemy(session_options={'autocommit': True, 'autoflush': False})

# Redis
redis_client = redis.Redis(
    db=settings.REDIS_DB_FOR_APPLICATION,
    host=settings.REDIS_HOSTNAME,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD)


def begin_transaction():
    db.session.begin(subtransactions=True)


def commit_transaction():
    db.session.commit()


def rollback_transaction():
    db.session.rollback()
