# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 21:18
# @Author  : Yunjie Cao
# @FileName: BookContent.py
# @Software: PyCharm
# @Email   ：YunjieCao@hotmail.com
import logging
import collections
from datetime import datetime


class BookDetail():
    def __init__(self, conn, session):
        self.conn = conn
        self.session = session

    def queryBookInformation(self):
        user = self.conn.execute(
            'SELECT * FROM Book WHERE isbn = \'{}\';'.format(self.session["isbn"])
        ).fetchone()
        isbn, title, date, outline = user
        book_info = collections.OrderedDict({'isbn': isbn, 'title': title, 'date': date})

        author_info = self.queryAuthor(isbn)
        self.session['author_info'] = author_info

        # get rating
        book_info['rating'] = self.queryRating(isbn)

        # add author and outline
        book_info['author'] = author_info['First Name'] + ' ' + author_info['Last Name']
        book_info['outline'] = outline

        # get comment (two parts: this user/ other user)
        comments = self.queryComment(isbn, self.session['uid'])
        return {'book_info': book_info, 'my comment': comments[0], 'other comment': comments[1]}

    def queryAuthor(self, isbn):
        author = self.conn.execute(
            'SELECT author.first_name, author.last_name, author.birthday, author.nationality, author.introduction ' +
            'FROM author, bookauthor ' +
            'WHERE bookauthor.isbn = \'{}\' AND bookauthor.wid = author.wid;'.format(isbn)
        ).fetchone()
        first_name, last_name, BOA, nationality, introduction = author
        return {'First Name': first_name, 'Last Name': last_name, 'BirthDay': BOA, 'Nationality': nationality, 'Introduction': introduction}


    def queryRating(self, isbn):
        rating = self.conn.execute('SELECT AVG(val) FROM Rating WHERE isbn = \'{}\';'.format(isbn)).fetchone()
        return round(rating[0], 2)


    def queryComment(self, isbn, uid):
        """
        :param isbn: isbn
        :param uid: uid
        :return: my_comment: list(dict) other_comment: list(tuple)
        """
        myComment = self.conn.execute('SELECT yc3702.User.first_name, Comment.time, Comment.content, Comment.uid, Comment.isbn ' +
                                   'FROM yc3702.User, Comment WHERE Comment.isbn = %s AND Comment.uid = %s AND ' +
                                   'yc3702.User.uid = Comment.uid;', (isbn, uid)).fetchall()
        otherComment = self.conn.execute('SELECT yc3702.User.first_name, Comment.time, Comment.content, Comment.uid ' +
                                   'FROM yc3702.User, Comment WHERE Comment.isbn = %s '+
                                   'AND yc3702.User.uid = Comment.uid;', (isbn,)).fetchall()

        myComment = list(myComment)
        ret_my_comment = []
        # change datetime object to string
        for mc in myComment:
            m = dict(mc)
            time = m['time']
            m['time'] = str(time).replace(' ','-') # url do not allow space, so replace that with '-'
            ret_my_comment.append(m)
        ret_my_comment.sort(key = lambda x: x['time'], reverse=True) # shown from latest
        otherComment = list(otherComment)
        filter_comment = []
        for com in otherComment:
            if com[3] != uid:
                filter_comment.append(com)
        return [ret_my_comment, filter_comment]