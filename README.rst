Yet Another Micro Web Framework
-------------------------------
is very simplistic yet another micro web framework made in python for study purposes.

It is built around `WebOb <https://webob.org/>`_ `Request` and `Response` classes,
that wrap around wsgi environment dictionary.

There is only one dependency to run it - WebOb,
so you can install deps with

.. code-block:: shell

    pip install WebOb

or

.. code-block:: shell

    pip install -r requirements.txt

On top of WebOb, YAMWF introduces some capabilities for registering your controllers for multiple
routes and adding parameters to them. Here's example from example_app:

.. code-block:: python

    @register('home/')
    @register('home/{foo:int}')
    def home(request, **kwargs):
        if 'foo' in kwargs:
            return Response(body='{0}, nice choice!'.format(kwargs.get('foo', '')))
        return Response(
            body='Well hello there, stranger. '
            + 'Please pick up your favorite integer and add it to path.',
        )

Note that this code doesn't use request object, but you can do whatever you want with it
and it provides a lot of additional info. Also note that also you can use different types for path
parameters, using complex type like dicts, tuples etc may introduce vulnerabilities to your app.
(And btw you just shouldn't use yamwf for production).

To run example app with wsgiref.simple_server:

.. code-block:: shell

  python app.py

And then navigate to lacalhost:8080.

Or you can use different servers like uwsgi or gunicorn passing to them
wsgi_app instance from app.py. And if you happen to write a new app - don't forget
to import your controllers before actually starting app!

So now you can just explore source code to see if there's something
interesting (there are not). Main logic, however, resides inside yamwf/routing.py,
so you can just check it. Have fun!
