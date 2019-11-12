# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 21:47
# @Author  : Yunjie Cao
# @FileName: LikeUnlikeBook.py
# @Software: PyCharm
# @Email   ：YunjieCao@hotmail.com

from sqlalchemy.orm.session import sessionmaker


class LikeUnlikeBooks():
    def __init__(self, engine, conn):
        self.engine = engine
        self.conn = conn

    def addLike(self, isbn, uid):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            self.conn.execute('INSERT INTO LikeBook (isbn, uid) VALUES (%s, %s);', (isbn, uid))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def unLike(self, isbn, uid):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            self.conn.execute('DELETE FROM LikeBook WHERE isbn=%s AND uid=%s;', (isbn, uid))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_likes(self, uid):
        books = self.conn.execute(
            'SELECT b.title, b.date, b.outline, b.isbn FROM Book b, LikeBook lb WHERE ' +
            'lb.uid=%s AND lb.isbn=b.isbn;', (uid,)
        ).fetchall()
        ret = []
        for b in books:
            title, date, outline, isbn = b
            ret.append({'title': title, 'date': date, 'outline': outline, 'isbn': isbn})
        return ret