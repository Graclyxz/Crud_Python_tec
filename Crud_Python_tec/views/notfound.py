from pyramid.view import notfound_view_config


@notfound_view_config(renderer='Crud_Python_tec:templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}
