from datetime import datetime
from enum import unique
from app import db
from sqlalchemy import func


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))

class Song(db.Model):
    __tablename__ = 'song'
    songid = db.Column(db.String(100), primary_key=True)
    songname = db.Column(db.String(100))
    artistid = db.Column(db.String(100), db.ForeignKey('artist.artistid'))
    songart = db.relationship('Artist')
    length = db.Column(db.String(100))
    albumid = db.Column(db.String(100), db.ForeignKey('album.albumid')) 
    songalbum = db.relationship('Album')

class Artist(db.Model):
    __tablename__ = 'artist'
    artistid = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    nationality = db.Column(db.String(100))

class Review(db.Model):
    __tablename__ = 'review'
    reviewid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    songid = db.Column(db.String(100),db.ForeignKey('song.songid') )
    reviewsong = db.relationship('Song')
    timeposted = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now())
    content = db.Column(db.String(500))
    rating = db.Column(db.Integer)

class Album(db.Model):
    __tablename__ = 'album'
    albumid = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    nos = db.Column(db.Integer)
    rd = db.Column(db.DateTime)
    artistid = db.Column(db.String(100), db.ForeignKey('artist.artistid'))
    albumart = db.relationship('Artist')
    songalbum = db.relationship('Song')