# -*- coding: utf-8 -*-
# @Time    : 2019/11/9 9:31
# @Author  : Yunjie Cao
# @FileName: RatingComment.py
# @Software: PyCharm
# @Email   ：YunjieCao@hotmail.com
from sqlalchemy.orm.session import sessionmaker
from datetime import datetime


class UpdateRatingComment():
    def __init__(self, engine, conn):
        self.engine = engine
        self.conn = conn


    def addRate(self, rate, isbn, uid):
        """
        react to POST request of rating from user
        :param rate: rate from user
        :param isbn: isbn of the book
        :param uid: uid of the user
        :return: None. But conduct insert operation on database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            self.conn.execute('INSERT INTO Rating (uid, isbn, val) VALUES (%s, %s, %s);', (uid, isbn, rate))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def deleteComment(self, uid, time, isbn):
        """
        react to GET request of comment from user -> delete (html does not support DELETE in form)
        :param uid: uid of user
        :param time: time of the comment
        :param uid: uid of the user
        :return: None. But conduct delete operation on database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            datetime_object = time.strptime(time, '%Y-%m-%d-%H:%M:%S.%f') # convert string to datetime object
            self.conn.execute('DELETE FROM Comment WHERE uid=%s AND time=%s AND isbn=%s;', (uid, time, isbn))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def addComment(self, comment, isbn, uid):
        """
        react to POST request of comment from user
        :param comment: comments from user
        :param isbn: isbn of the book
        :param uid: uid of the user
        :return: None. But conduct insert operation on database
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            self.conn.execute('INSERT INTO Comment (uid, isbn, content) VALUES (%s, %s, %s);',
                              (uid, isbn, comment))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
