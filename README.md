# django_analytics
__django_analytics is a middleware for Django that tracks visitors.__

## Installation

1. Run `pip install git+https://github.com/trdwll/django_analytics.git`
2. Add `'django_analytics'` to your __INSTALLED_APPS__.
3. Add `'django_analytics.middleware.PageViewsMiddleware'` to your __MIDDLEWARE__.
4. Run `python manage.py migrate`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)