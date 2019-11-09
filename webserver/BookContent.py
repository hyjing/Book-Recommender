# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 21:18
# @Author  : Yunjie Cao
# @FileName: BookContent.py
# @Software: PyCharm
# @Email   ：YunjieCao@hotmail.com
import logging
class BookDetail():
    def __init__(self, conn, session):
        self.conn = conn
        self.session = session

    def queryBookInformation(self):
        user = self.conn.execute(
            'SELECT * FROM Book WHERE isbn = \'{}\';'.format(self.session["isbn"])
        ).fetchone()
        isbn, title, date, outline = user
        book_info = {'isbn': isbn, 'title': title, 'date': date, 'outline': outline}
        author_info = self.queryAuthor(isbn)
        # TODO: query rating and comments information
        return {'book_info': book_info, 'author_info': author_info}

    def queryAuthor(self, isbn):
        author = self.conn.execute(
            'SELECT author.first_name, author.last_name, author.birthday, author.nationality, author.introduction ' +
            'FROM author, bookauthor ' +
            'WHERE bookauthor.isbn = \'{}\' AND bookauthor.wid = author.wid;'.format(isbn)
        ).fetchone()
        first_name, last_name, BOA, nationality, introduction = author
        return {'First Name': first_name, 'Last Name': last_name, 'BirthDay': BOA, 'Nationality': nationality, 'Introduction': introduction}


    def queryRating(self, isbn, uid):
        #TODO: query rating
        pass

    def queryComment(self, isbn, uid):
        # TODO: query comments: other uesrs/ myself
        pass