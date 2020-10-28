# LinvieTheater

## Description
A Web application that collect thousands of movies for user to watch, comment and bookmark.

The application makes use of Python's Flask framework, Jinja templating library and WTForms.
Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool. 

**Installation via requirements.txt**

```shell
$ cd Linvie
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```
When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:Linvie' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *Linvie* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Configuration

The *Linvie/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
* `SQLALCHEMY_DATABASE_URI`: Database URI.
* `TEST_SQLALCHEMY_DATABASE_URI`: Database URI for test.


## Testing

You can directly type
````shell
$  python -m pytest
```` 
Or run tests from PyCharm Configuration `pytest in tests`.
* You do ***NOT*** need to modify the test data file path.
* All test case that add object in to database will delete it after testing.





