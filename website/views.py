"""
purpose:   to store the URL endpoints for the front end of our website
        -- we store the routes (main pages of our website, like login, sign-up, main page, etc)
        -- import Blueprint means we define this file as a blueprint (it has a bunch of URLs/roots in it)
"""
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Recommended, IMDB_top_10
from . import db 
from google_links_and_posters_BS4 import get_google_1st_link, get_google_page, get_image, compute_three, compute_array
from movieREC_use_model import rec_10, titles_only
from imdb_get_top_ten import get_top_10_imdb
import json

views = Blueprint('views', __name__)       # set up a views blueprint for our flask application


@views.route('/journal', methods=['GET', 'POST']) # define 1st view (this is a decorator)
@login_required                            # 2nd decorator, cannot get to home pg without loggin in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            #flash('Journal entry added!', category='success')

    return render_template("journal.html", user=current_user)

@views.route('/recommend', methods=['GET', 'POST']) # define 1st view (this is a decorator)
@login_required                            # 2nd decorator, cannot get to home pg without loggin in
def recommend():
    for j in range(15):
        old_rec = Recommended.query.first()
        if old_rec:
            if old_rec.user_id == current_user.id:
                db.session.delete(old_rec)
                db.session.commit()
        else:
            break

    if request.method == 'POST':
        user_movie = request.form.get('movie')

        if len(user_movie) < 1:
            flash('Movie title is too short!', category='error')
        else:
            user_movie = user_movie.lower()               # make everything lowercase, then capitalize each word
            user_movie = user_movie.title()
            try:
                ten_rec, found_movie = rec_10(user_movie)
            except:
                flash('Movie not found:(', category='error')
                return render_template("recommend.html", user=current_user)
            recommendations = titles_only(str(ten_rec))
            results = compute_array(recommendations[:12])
            x = 1
            for i, three_links in enumerate(results):
                link1 = three_links[0]
                link2 = three_links[1]
                img_link = three_links[2]
                if img_link == None:         # avoid displaying a bad link (no img, void link)
                    continue                 # simply skip to next recommended movie
                title = str(x) + ') ' + str(recommendations[i])
                new_rec = Recommended(data=title, link1=link1, link2=link2, img_link=img_link, user_id=current_user.id)
                db.session.add(new_rec)
                db.session.commit()
                x += 1
            flash('Movie found!', category='success')

            found_movie = "Our recommendations for you for: " + str(found_movie)
            found_title = Recommended(found_title=found_movie, user_id=current_user.id)
            db.session.add(found_title)
            db.session.commit()

    return render_template("recommend.html", user=current_user)

@views.route('/imdb_top_10', methods=['GET', 'POST']) # define 1st view (this is a decorator)
@login_required                                       # 2nd decorator, cannot get to home pg without loggin in
def imdb_top_10():
    top_10 = get_top_10_imdb()      # we get an array of 10 movie names back
    results = compute_array(top_10) # imported function, uses threads to run web-scraping concurrently (50 sec --> 4 sec wait time)
    x = 1
    for i, three_links in enumerate(results):
        link1 = three_links[0]
        link2 = three_links[1]
        img_link = three_links[2]
        if img_link == None:         # avoid displaying a bad link (no img, void link)
            continue                 # simply skip to next recommended movie
        movie = str(x) + ') ' + str(top_10[i])
        top_ten_movies = IMDB_top_10(data=str(movie), link1=link1, link2=link2, img_link=img_link, user_id=current_user.id)
        db.session.add(top_ten_movies)
        db.session.commit()
        x += 1
    return render_template("imdb_top_10.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)      # turn our data into a python dictionary object
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})       # turn the dictionary into a json object (we don't need the dict, but a return is a must)
