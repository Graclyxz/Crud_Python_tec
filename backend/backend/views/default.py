from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from ..models import Note

@view_config(route_name='home', renderer='backend:templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(models.MyModel)
        one = query.filter(models.MyModel.name == 'one').one()
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'backend'}


#Crear notas con titulo y texto
@view_config(route_name='add_note', renderer='json', request_method='POST')
def add_note_view(request):
    try:
        title = request.json_body.get('title', '').strip()
        text = request.json_body.get('text', '').strip()
        if not title or not text:
            return Response(json_body={"error": "El título y el texto no pueden estar vacíos"}, status=400)
        
        new_note = Note(title=title, text=text)
        request.dbsession.add(new_note)
        request.dbsession.flush()  # Guarda en la BD
        
        return {"message": "Nota creada", "id": new_note.id}
    
    except SQLAlchemyError:
        return Response(json_body={"error": "Error en la base de datos"}, status=500)

#Listar todas las notas
@view_config(route_name='get_notes', renderer='json', request_method='GET')
def get_notes_view(request):
    try:
        notes = request.dbsession.query(Note).all()
        return [{"id": note.id, "title": note.title, "text": note.text} for note in notes]
    except SQLAlchemyError:
        return Response(json_body={"error": "Error en la base de datos"}, status=500)

#Listar las notas por ID
@view_config(route_name='get_note', renderer='json', request_method='GET')
def get_note_view(request):
    try:
        note_id = int(request.matchdict['id'])
        note = request.dbsession.query(Note).filter_by(id=note_id).first()
        if note is None:
            return Response(json_body={"error": "Nota no encontrada"}, status=404)
        return {"id": note.id, "title": note.title, "text": note.text}
    except SQLAlchemyError:
        return Response(json_body={"error": "Error en la base de datos"}, status=500)

#Actualizar notas por ID
@view_config(route_name='update_note', renderer='json', request_method='PUT')
def update_note_view(request):
    try:
        note_id = int(request.matchdict['id'])
        note = request.dbsession.query(Note).filter_by(id=note_id).first()
        if note is None:
            return Response(json_body={"error": "Nota no encontrada"}, status=404)
        
        title = request.json_body.get('title', '').strip()
        text = request.json_body.get('text', '').strip()
        if not title or not text:
            return Response(json_body={"error": "El título y el texto no pueden estar vacíos"}, status=400)
        
        note.title = title
        note.text = text
        request.dbsession.flush()  # Guarda en la BD
        
        return {"message": "Nota actualizada", "id": note.id}
    except SQLAlchemyError:
        return Response(json_body={"error": "Error en la base de datos"}, status=500)
    
#Eliminar notas por ID
@view_config(route_name='delete_note', renderer='json', request_method='DELETE')
def delete_note_view(request):
    try:
        note_id = int(request.matchdict['id'])
        note = request.dbsession.query(Note).filter_by(id=note_id).first()
        if note is None:
            return Response(json_body={"error": "Nota no encontrada"}, status=404)
        
        request.dbsession.delete(note)
        request.dbsession.flush()  # Guarda en la BD
        
        return {"message": "Nota eliminada", "id": note.id}
    except SQLAlchemyError:
        return Response(json_body={"error": "Error en la base de datos"}, status=500)
    
db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
