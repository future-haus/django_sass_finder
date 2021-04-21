# django_sass_finder
a Django finder that compiles Sass files

## Installation
### WARNING: MAKE SURE YOU HAVE NO SASS PACKAGES INSTALLED (other than libsass)!

run `pip install django_sass_finder`, then put django_sass_finder in your `INSTALLED_APPS`, and
finally list your static file finders as so:

```py
STATICFILES_FINDERS = [
    # add the default Django finders as this setting will override the default
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # our finder
    'django_sass_finder.finders.ScssFinder',
]
```

## Configuration
The following variables need to bet set in your settings file:

```py
SCSS_ROOT = 'web/src/scss'
SCSS_COMPILE = ['styles.scss']
```

If you are including some node_modules or other files in your scss files, you can specify where to look for these:

```py
SCSS_INCLUDE_PATHS = ['node_modules']
```

### Optional settings 

django_sass_finder defaults to using a temporary directory, but if you want to keep the css files around after compile and collect you can specify your own:

```py
CSS_COMPILE_DIR = 'tmp'
```

## Usage
run `python manage.py collectstatic` to compile your Sass files and put them in the STATIC_ROOT.

## License
This package is licensed under the MIT license.
