import os

import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

con = mysql.connector.connect(host="localhost", port=3306, user="user", password="my-secret-pw", database='paintings_schema')
cur = con.cursor()
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/results', methods=['get', 'post'])
def searching():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('upload'))
        if file and file.filename.endswith('.sql'):
            filename = secure_filename(file.filename)
            file.save(os.path.join('queries/', filename))
            with open((os.path.join('queries/', filename)), 'r') as f:
                query = f.read()
    else:
        query = request.args.get('query')
    if len(query) == 0:
        return redirect(url_for('search'))
    sql_queries = query.split(';')
    for query in sql_queries:
        cur.execute(query)
    result = cur.fetchall()
    return render_template('results.html', result=result)


@app.route('/paintings')
def paintings():
    cur.execute("SELECT paintings_schema.painting.title, creation_date, paintings_schema.artist.name, "
                "paintings_schema.museum.name, paintings_schema.medium.title, paintings_schema.art_movement.title "
                "FROM paintings_schema.painting, paintings_schema.artist, paintings_schema.museum, "
                "paintings_schema.medium, paintings_schema.art_movement WHERE "
                "paintings_schema.painting.id_artist=paintings_schema.artist.id_artist AND "
                "paintings_schema.painting.id_museum=paintings_schema.museum.id_museum AND "
                "paintings_schema.painting.id_medium=paintings_schema.medium.id_medium AND "
                "paintings_schema.painting.id_art_movement=paintings_schema.art_movement.id_art_movement ORDER BY "
                "paintings_schema.painting.title")
    result = cur.fetchall()
    return render_template('paintings.html', result=result)


@app.route('/artists')
def artists():
    cur.execute("SELECT name, born, died, origin FROM paintings_schema.artist ORDER BY name")
    result = cur.fetchall()
    return render_template('artists.html', result=result)


@app.route('/museums')
def museums():
    cur.execute("SELECT name, locality, country FROM paintings_schema.museum, paintings_schema.location WHERE "
                "paintings_schema.museum.id_location=paintings_schema.location.id_location ORDER BY name")
    result = cur.fetchall()
    return render_template('museums.html', result=result)


@app.route('/mediums')
def mediums():
    cur.execute("SELECT title FROM paintings_schema.medium ORDER BY title")
    result = cur.fetchall()
    return render_template('mediums.html', result=result)


@app.route('/art_movements')
def art_movements():
    cur.execute("SELECT title, dates FROM paintings_schema.art_movement ORDER BY title")
    result = cur.fetchall()
    return render_template('art_movements.html', result=result)


@app.route('/exhibitions')
def exhibitions():
    cur.execute("SELECT paintings_schema.painting.title, paintings_schema.exhibition.title, dates, name FROM "
                "paintings_schema.exhibition, paintings_schema.painting, paintings_schema.museum WHERE "
                "paintings_schema.exhibition.id_painting=paintings_schema.painting.id_painting AND "
                "paintings_schema.exhibition.id_museum=paintings_schema.museum.id_museum ORDER BY "
                "paintings_schema.painting.title")
    result = cur.fetchall()
    return render_template('exhibitions.html', result=result)


@app.route('/locations')
def locations():
    cur.execute("SELECT locality, country FROM paintings_schema.location ORDER BY country")
    result = cur.fetchall()
    return render_template('locations.html', result=result)


@app.errorhandler(500)
def error_500(e):
    response = e.get_response()
    return render_template('500.html', response=response)


if __name__ == '__main__':
    app.run()
