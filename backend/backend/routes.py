def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('add_note', '/notes')
    config.add_route('get_notes', '/notes')
    config.add_route('get_note', '/notes/{id}')
    config.add_route('update_note', '/notes/{id}')
    config.add_route('delete_note', '/notes/{id}')