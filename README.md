# ImageGallery

This software can be used to create an image gallery. This should be hosted in
Heroku, or you have to change the settings.


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


