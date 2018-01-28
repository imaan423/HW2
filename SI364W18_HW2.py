## SI 364
## Winter 2018
## HW 2 - Part 1
## Imaan Munir


## This homework has 3 parts, all of which should be completed inside this file.

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json


#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class Artistform(FlaskForm):
	artist = StringField("Enter Artist", validators=[Required()])
	submit = SubmitField('Submit')

class AlbumEntryForm(FlaskForm):
	album = StringField("Enter the name of an album:", validators=[Required()])
	radio = RadioField("How much do you like this album?", choices=[(1,1),(2,2),(3,3)], validators=[Required()])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


@app.route('/artistform', methods = ['POST', 'GET'])
def artistform():
	simpleForm = Artistform()
	return render_template('artistform.html', form=simpleForm)


@app.route('/artistinfo', methods = ['GET', 'POST'])
def artistinfo():
	form = Artistform(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		itunes = "https://itunes.apple.com/search?term=" 
		s = form.artist.data
		url = itunes + s
		whole = requests.get(url)
		data = json.loads(whole.text)
		return render_template('artist_info.html', objects = data["results"])
	flash('All fields are required!')
	return redirect(url_for('artistform'))


@app.route('/artistlinks')
def artistlinks():
    return render_template('artist_links.html')


@app.route('/specific/song/<artist_name>')
def artistname(artist_name):
	itunes = "https://itunes.apple.com/search?term=" + artist_name 
	whole = requests.get(itunes)
	data = json.loads(whole.text)
	return render_template('specific_artist.html', results = data['results'])


@app.route('/specific/song/<album_entry>')
def artistentry():
    return render_template('album_entry.html')


@app.route('/album_data.html')
def artistdata():
    return render_template('album_data.html')


@app.route('/album_entry')
def album_entry():
		simpleForm = AlbumEntryForm()
		return render_template('album_entry.html', form=simpleForm)
	

@app.route('/album_result', methods = ['POST', 'GET'])
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST': 
		s = request.form['album']
		r = request.form['radio']
		results = {}
		results['s'] = s
		results['r'] = r
		return render_template("album_data.html", results=results, form=form)
	flash('All fields are required!')
	return redirect(url_for('album_entry'))



if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
