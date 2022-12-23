# ImageGallery

This software can be used to create an image gallery. This should be hosted in
Heroku, or you have to change the settings.

## Requirements
This project is supported only on python versions <= 3.6.

## Installation

Recommended way is to have this all in a virtualenv.

These instructions are for UNIX based OS. On Windows, please see how you can
install virtualenv for you OS. Also, if you are using Windows, consider using
Windows 10 Bash.


Install virtualenv:
```
[sudo] pip3 install virtualenv
```


Then create a new folder for virtualenvs and create a new virtualenv
```
cd 
mkdir venvs
cd venvs
virtualenv imagegallery
```

Then activate it
```
source imagegallery/bin/activate
```

Now, depending on your shell, you should see that you are in imagegallery
virtualenv. For example, on bash you can see (imagegallery) in front of the
bottom line.

Then clone the repository and go inside it.
```
cd 
git clone https://github.com/Alqio/imagegallery.git
cd imagegallery
```


Install all required modules.
```
pip3 install -r requirements.txt
```

And then wait for everything to install.


You can run the server like this:
```
python3 manage.py runserver
```


## Errors

django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly
configured. Please supply the ENGINE value. Check settings documentation for
more details.

- comment the last line of settings.py (cant load local info from db, only on
  heroku)


django.db.utils.ProgrammingError: relation "images_album" does not exist
LINE 1: ...bum"."description", "images_album"."creator" FROM "images_al...

- 1. create the table manually (images_album table).
- 2. remove old migrations
- 3. trace the error message up. For example, the last line that was my code was in forms.py. Apparently that crashed stuff. Comment those lines out until it works :)

