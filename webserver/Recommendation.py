# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 19:33
# @Author  : Yunjie Cao
# @FileName: Recommendation.py
# @Software: PyCharm
# @Email   ：YunjieCao@hotmail.com
from sqlalchemy.orm.session import sessionmaker
from datetime import datetime


class Recommend():
    def __init__(self, conn, session):
        self.conn = conn
        self.session = session


    def generateRecommendation(self):
        """
        get recommendations for user
        :return:
        """
        recommend_by_liked_types = self.recommendByType()
        recommend_by_rating = self.recommendByRating()
        filtered = set()
        ret = []
        for rc in recommend_by_liked_types:
            if rc['isbn'] in filtered:
                continue
            else:
                ret.append(rc)
                filtered.add(rc['isbn'])
        for rc in recommend_by_rating:
            if rc['isbn'] in filtered:
                continue
            else:
                ret.append(rc)
                filtered.add(rc['isbn'])
        return ret


    def recommendByType(self):
        """
        recommend books according to types this user like
        :return:
        """
        books = self.conn.execute(
            'SELECT b.title, b.date, b.outline, b.isbn FROM Book b, BookType bt, likeType lt '
            'WHERE lt.uid=%s AND lt.tid=bt.tid AND bt.isbn=b.isbn;', (self.session['uid'])
        ).fetchall()
        ret = []
        for b in books:
            title, date, outline, isbn = b
            ret.append({'title': title, 'date': date, 'outline': outline, 'isbn': isbn})
        return ret


    def recommendByRating(self):
        """
        recommend books according to their ratings
        :return:
        """
        books = self.conn.execute(
            'SELECT b.title, b.date, b.outline, b.isbn FROM Book b WHERE b.isbn in (SELECT temp.isbn FROM (SELECT r.isbn, AVG(r.val) FROM' +
            ' Rating r GROUP BY r.isbn ORDER BY AVG(r.val) DESC LIMIT 20) AS temp);'
        ).fetchall()
        ret = []
        for b in books:
            title, date, outline, isbn = b
            ret.append({'title': title, 'date': date, 'outline': outline, 'isbn': isbn})
        return ret
