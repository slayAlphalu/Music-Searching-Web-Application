# Music-Searching-Web-Application
Using google cloud as engine. Combine the power of flask and python to build a music virtual searching engine.

# Overview of Project 1

We build a substantial real-world database application of music.  This project is split into three parts:

* [Part 1](./part1.md): come up with a web application and design the database on paper using ER-modeling.
* [Part 2](./part2.md): implement your database by translating your model into a database schema and example data.
* [Part 3](./part3.md): implement an application that accesses and modifies your database.


# References


The following documentation may be helpful for both learning Python and Flask:

* [Java to Python Cheatsheet](https://github.com/w4111/w4111.github.io/blob/master/java2python.md)
* [Python 2 tutorial](https://docs.python.org/2/tutorial/)
* [Python 3 tutorial](https://docs.python.org/3.7/tutorial/)
* [Learn Python The Hard Way](http://learnpythonthehardway.org/book/)
* [Flask documentation](http://flask.pocoo.org)
* [Flask Tutorial](http://flask.pocoo.org/docs/latest/tutorial/)
* [Jinja Template documentation](http://jinja.pocoo.org/)
* [Jinja Tutorial](https://realpython.com/blog/python/primer-on-jinja-templating/)

If your application has users, and you'd like to implement login/logout pages with password authentication, check:
* [Flask Quickstart: Sessions](http://flask.pocoo.org/docs/1.0/quickstart/#sessions)
* [Creating a login page](https://pythonspot.com/login-authentication-with-flask/)
    * Note: do not follow the "Connecting to your database" section of this tutorial, as it uses ORM. Remember that you are **not** allowed to use ORM, and your code must issue SQL queries instead.



# Getting Started

Your job is to implement your proposed web application.  To help you out,
we have provided a bare-bones Flask web application in [./webserver/](./webserver/) which implemented in Python 2.7. **You can build upon this starter code using Python 2.7 or change to Python 3 by referring to the official [Flask tutorial](http://flask.pocoo.org/docs/latest/tutorial/) and [Python 3 tutorial](https://docs.python.org/3.7/tutorial/).**
It provides code that connects to a database url, and a default index page.
Take a look at the comments in `server.py` to see how to use modify the server.
You will need to connect to the class database (used for part 2).

Please read all these directions, and get the example server we provide running. Once you get it
running you should edit it to talk to your own database and start working on your custom logic.


### A Short Introduction to SQLAlchemy

We use a python package called `SQLAlchemy` to simplify our work for connecting to the database.
For example, `server.py` contains the following code to load useful functions from
the package:

        # import useful functions from the package
        from sqlalchemy import *

`SQLAlchemy` is able to connect to many different types of DBMSes such as 
SQLite, PostgreSQL, MySQL, Oracle and other databases.  Each such DBMS
is called an "engine".  The `create_engine()` function sets up the configuration
to specify which type of DBMS we want to connect to, and what their parameters are.

        engine = create_engine(DATABASEURI)


Given an engine, we can then connect to it (this is similar to how `psql` connects
to the staff database).

        conn = engine.connect()

At this point, the `conn` connection object can be used to
execute queries to the database.  This is basically what `psql`
is doing under the covers!  

        cursor = conn.execute("select 1")

The `execute` function takes a SQL query string as input, and
returns a `cursor` object.  You can think of this as an iterator 
over the result relation.  This means you can run `select *` 
on a million row table, and not run out of memory. Instead of
sending the entire result at once. Instead, this
object lets you treat the result as an iterator and call `.next()`
on it, or loop through it.  [See the documentation for a detailed description](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy).

        # this fetches the first row if called right after
        # the execute function above.  It also moves the
        # iterator to the next result row.
        record = cursor.fetchone()

        # this will fetch the next record, or None if
        # there are no more results.
        second_record = cursor.fetchone()

        # this loops through the results of the cursor one by one
        for row in cursor:
          print list(row)


The above description is a way to directly write and run SQL
queries as strings, and directly manipulate the result relations.
SQLAlchemy is also an [Object Relational Mapper](https://en.m.wikipedia.org/wiki/Object-relational_mapping)
that provides an interface that hides SQL query strings and 
result sets from you.  Instead you access and manipulate
tables in the database as if they were normal Python objects.





