Pyt - Customized Interactive Tutorial for Python
------------------------------------------------

This is a flexible tutorial platform for python, where an administrator
has the flexibility to add new tutorials and quizzes based on the requirements.

Please create an application in stormpath for user management. It provides
the functionality to create new users, login and logout, and also maintain
information about the current progress of the user in the tutorial.

There is additional functionality for an administrator to add new tutorials
and quizzes from the website without a need for tinkering with the database.

A requirements.py file is provided which lists all the dependencies for the
project. A virtualenv environment is recommended for installing the dependencies,
without affecting the local environment.

A sample locust configuration is included, which can be used to test the load
handled by the server.

The views are rendered using the bootstrap template. A different template
can be used if needed.

Note : It uses Trinket to allow the user to run python programs in the browser.
This makes it not necessary to switch to a terminal to execute python.
Trinket provides support for a variety of builtin plugins. If 
more flexibility is needed, one can setup a python server in the backend 
