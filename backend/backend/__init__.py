from pyramid.config import Configurator
from backend.routes import includeme


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.add_static_view(name='static', path='backend:static', cache_max_age=3600)
        config.include(includeme)
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.models')
        config.scan()
    return config.make_wsgi_app()
