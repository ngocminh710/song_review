from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request,session
from config import Config
from sqlalchemy import func
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from app import db
from app.Model.models import Album, Artist, User,Song,Review
from app.Controller.forms import MusicsearchForm,ChangeUserForm,CommentForm
from app.Controller.user import login_required

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index/', methods=['GET','POST'])
def index():
    form = MusicsearchForm()
    if request.method == 'GET':
        return render_template('index.html',form=form)
    elif request.method == 'POST':
        if form.validate_on_submit(): 
            try:
                field = form.data['field']
                matching = form.data['matching']
                filters = {field:matching}
                if field == 'songname':
                    resultlist = Song.query.filter_by(**filters)
                    return render_template('searchsongresult.html',resultlist=resultlist,form=form,field=matching)
                elif field == 'artist':
                    resultlist = Artist.query.filter_by(name=matching)
                    return render_template('searchatristresult.html',resultlist=resultlist,form=form,field = matching)
                else:
                    resultlist = Album.query.filter_by(name=matching)
                    return render_template('searchalbumresult.html',resultlist=resultlist,form=form,field="Album")
            except:
                return redirect('/')      
        return redirect('/')   


@bp_routes.route('/home/', methods=['GET','POST'])
@login_required
def home():
    u = User.query.filter_by(username=session['user_name']).first()
    revlist = Review.query.filter_by(username=session['user_name'])
    form = ChangeUserForm(email=u.email)
    if request.method == 'GET':
        return render_template('home.html',form=form,reviewlist=revlist)
    elif request.method == 'POST':
        if form.validate_on_submit(): 
            try:
                u = User.query.filter_by(username=session['user_name']).first()
                u.password = form.password.data
                u.email = form.email.data
                db.session.commit()
                session.clear()
                return redirect(url_for('authentication.login'))
            except:
                return redirect('/home/')      
        return redirect('/home/')   

@bp_routes.route('/searchartist', methods=['GET','POST'])
def searchartist():
    try:
        resultlist = Song.query.filter_by(artistid= request.args.get("artistid"))
        field = Artist.query.filter_by(artistid = (request.args.get("artistid")))[0]
        return render_template('searchsongbyartist.html',resultlist=resultlist,field = field)
    except:
        return redirect('/index/') 
  

@bp_routes.route('/searchalbum', methods=['GET','POST'])
def searchalbum():
    try:
        songList = Song.query.filter_by(albumid=(request.args.get("albumid")))
        field = Album.query.filter_by(albumid = (request.args.get("albumid")))[0]
        return render_template('searchsongbyalbum.html',songlist=songList,field = field)
        
        
    except:
        return redirect('/index/')   



@bp_routes.route('/getreview', methods=['GET','POST'])
def getreview():
    form = CommentForm()
    try:
        thesong = Song.query.filter_by(songid=(request.args.get("songid")))[0]
        reviewlist = Review.query.filter_by(songid=(request.args.get("songid")))
        return render_template('review.html',reviewlist=reviewlist,thesong=thesong,form=form)
    except:
        return redirect('/index/')   


@bp_routes.route('/createreview', methods=['GET','POST'])
def createreview():
    if request.method == 'POST':
        try:
            songid = request.args.get("songid")
            rev = Review(username=session['user_name'], 
                        songid=songid,
                        content = request.form.get('comment'), 
                        rating=request.form.get('rating'),
                        )
            db.session.add(rev)
            db.session.commit()
            return redirect("/getreview?songid={}".format(songid))   
        except:
            return redirect('/index/') 