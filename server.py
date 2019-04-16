#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
import pandas as pd
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, session, request, render_template, g, redirect, Response, url_for, escape

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# XXX: The Database URI should be in the format of:
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = "wg2329"
DB_PASSWORD = "GRL2NNLxqs"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


# Here we create a test table and insert some values in it
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  if 'username' in session:
      return render_template("index.html")
  return redirect('/login')


  # #
  # # example of a database query
  # #
  # # cursor = g.conn.execute("SELECT name FROM test")
  # # names = []
  # # for result in cursor:
  # #   names.append(result['name'])  # can also be accessed using result[0]
  # # cursor.close()
  #
  # cursor = g.conn.execute("select singer_name from singer")
  # names = []
  # for result in cursor:
  #   names.append(result['singer_name'])
  # cursor.close()
  #
  # #
  # # Flask uses Jinja templates, which is an extension to HTML where you can
  # # pass data to a template and dynamically generate HTML based on the data
  # # (you can think of it as simple PHP)
  # # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  # #
  # # You can see an example template in templates/index.html
  # #
  # # context are the variables that are passed to the template.
  # # for example, "data" key in the context variable defined below will be
  # # accessible as a variable in index.html:
  # #
  # #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  # #     <div>{{data}}</div>
  # #
  # #     # creates a <div> tag for each element in data
  # #     # will print:
  # #     #
  # #     #   <div>grace hopper</div>
  # #     #   <div>alan turing</div>
  # #     #   <div>ada lovelace</div>
  # #     #
  # #     {% for n in data %}
  # #     <div>{{n}}</div>
  # #     {% endfor %}
  # #
  # context = dict(data = names)
  #
  #
  # #
  # # render_template looks in the templates/ folder for files.
  # # for example, the below file reads template/index.html
  # #
  # return render_template("index.html", **context)
  # #return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

#
# This is an example of a different path.  You can see it at
#
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another')
def another():
  return render_template("anotherfile.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')

@app.route('/search_singer', methods=['POST'])
def search_singer():
  name = request.form['name']
  print name
  cmd = "select singer_name FROM singer where singer_name ILIKE '%" + name + "%'"
  cursor = g.conn.execute(text(cmd))

  search_result = []
  for result in cursor:
    search_result.append(result[0])
    print result
  cursor.close()

  if len(search_result) == 0:
      return render_template("no_result.html")

  return render_template("search_singer.html", search_result = search_result)

@app.route('/search_song', methods=['POST'])
def search_song():
  if 'album' in request.form:
      album = request.form['album']
      cmd = "select distinct(song_name) from album t1, song_album_r t2 where t1.album_name = t2.album_name and t1.album_name = '" + album + "'"
      cursor = g.conn.execute(text(cmd))

      search_result = []
      for result in cursor:
        search_result.append(result[0])
        print result
      cursor.close()

      return render_template("search_song.html", search_result = search_result)

  if 'playlist' in request.form:
      playlist = request.form['playlist']
      cmd = "select distinct(song_name) from song_playlist_r where list_name = '" + playlist + "'"
      cursor = g.conn.execute(text(cmd))

      search_result = []
      for result in cursor:
        search_result.append(result[0])
        print result
      cursor.close()

      return render_template("search_song.html", search_result = search_result)

  name = request.form['name']
  print name
  cmd = "select song_name FROM sing_song where song_name ILIKE '%" + name + "%'"
  cursor = g.conn.execute(text(cmd))

  search_result = []
  for result in cursor:
    search_result.append(result[0])
    print result
  cursor.close()

  if len(search_result) == 0:
    return render_template("no_result.html")

  return render_template("search_song.html", search_result = search_result)


@app.route('/similar_songs', methods=['POST'])
def similar_songs():
  name = request.form['name'].rstrip()
  print name
  cmd = "select * from (select distinct(t1.song_name) from sing_song t1, sing_song t2 where t1.genre = t2.genre and t2.song_name = '" + name + "' union select distinct(t3.song_name) from song_playlist_r t3 where t3.list_name in (select list_name from song_playlist_r where song_name = '" + name + "')) t4 order by random() limit 20"
  cursor = g.conn.execute(text(cmd))

  search_result = []
  for result in cursor:
    search_result.append(result[0])
    print result
  cursor.close()

  return render_template("search_song.html", search_result = search_result)


@app.route('/singer_song', methods=['POST'])
def singer_song():
    name = request.form['name'].rstrip()
    print name
    cmd = "select song_name from singer t1, sing_song t2 where t1.singer_name ilike '" + name + "' and t1.singer_name = t2.singer_name"
    print cmd
    cursor = g.conn.execute(text(cmd))

    search_result = []
    for result in cursor:
      search_result.append(result[0])
      print result
    cursor.close()

    return render_template("singer_song.html", name=name, search_result=search_result)


@app.route('/search_album', methods=['POST'])
def search_album():
  name = request.form['name']
  print name
  cmd = "select t1.album_name, t2.singer_name FROM album t1, singer_album_r t2 where t1.album_name = t2.album_name and t1.album_name ILIKE '%" + name + "%' order by t1.album_volume desc"
  cursor = g.conn.execute(text(cmd))

  search_result = []
  for result in cursor:
    search_result.append(result[0:2])
    print result
  cursor.close()

  if len(search_result) == 0:
      return render_template("no_result.html")

  return render_template('albuminfo.html', search_result = search_result)
  # data = pd.DataFrame(search_result)
  # data.columns = ['album_name', 'album_year','album_volume']
  # return render_template('albuminfo.html', tables = [data.to_html(index = False)], titles = ['Search Album Info Results'])


@app.route('/search_list', methods=['POST'])
def search_list():
  name = request.form['name']
  print name
  cmd = "select list_name from playlist where list_name ILIKE '%" + name + "%' order by list_volume desc"
  cursor = g.conn.execute(text(cmd))

  search_result = []
  for result in cursor:
    search_result.append(result[0])
    print result
  cursor.close()

  if len(search_result) == 0:
      return render_template('no_result.html')

  return render_template('search_list.html', search_result = search_result)


@app.route('/search_comment', methods=['POST'])
def search_comment():
  name = request.form['name']
  print name
  if 'comment' in request.form and request.form['comment'].strip() != '':
      comment = request.form['comment']
      print comment
      comment_cmd="insert into comment values (current_timestamp, '" + comment + "', '" + name + "')"
      g.conn.execute(text(comment_cmd))
  cmd="select comment_time,content from comment where song_name ILIKE '%" + name + "%' order by comment_time desc"
  cursor = g.conn.execute(text(cmd))

  search_result = []
  for result in cursor:
    search_result.append(result)
    print result
  cursor.close()

  if len(search_result) == 0:
      return render_template('no_comment.html', name = name)

  data = pd.DataFrame(search_result)
  data.columns = ['comment time', 'content']
  return render_template('comment.html', name = name, tables = [data.to_html(index = False)], titles = ['Search Your Song Comments'])


@app.route('/albums', methods=['POST'])
def albums():
    name = request.form['name'].rstrip()
    print name
    cmd = "select t1.album_name from singer_album_r t1, album t2 where t1.album_name = t2.album_name and singer_name = '" + name + "' order by album_year"
    print cmd
    cursor = g.conn.execute(text(cmd))

    search_result = []
    for result in cursor:
      search_result.append(result[0])
      print result
    cursor.close()

    # data = pd.DataFrame(search_result)
    # data.columns = ['Singer Name', 'Album Name']
    return render_template('album.html', name = name, search_result = search_result)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
