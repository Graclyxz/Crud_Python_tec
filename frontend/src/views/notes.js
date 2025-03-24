import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/notes.css';

const Notes = () => {
    const [notes, setNotes] = useState([]);
    const [title, setTitle] = useState('');
    const [text, setText] = useState('');
    const [editNoteId, setEditNoteId] = useState(null);

    useEffect(() => {
        fetchNotes();
    }, []);

    const fetchNotes = async () => {
        try {
            const response = await axios.get('/notes/all');
            setNotes(response.data);
        } catch (error) {
            console.error('Error fetching notes:', error);
        }
    };

    const handleAddNote = async () => {
        try {
            await axios.post('/notes', { title, text });
            fetchNotes();
            setTitle('');
            setText('');
        } catch (error) {
            console.error('Error adding note:', error);
        }
    };

    const handleUpdateNote = async (id) => {
        try {
            const response = await axios.put(`/notes/update/${id}`, { title, text });
            setNotes(notes.map(note => (note.id === id ? response.data : note)));
            fetchNotes();
            setTitle('');
            setText('');
            setEditNoteId(null);
        } catch (error) {
            console.error('Error updating note:', error);
        }
    };

    const handleDeleteNote = async (id) => {
        try {
            await axios.delete(`/notes/delete/${id}`);
            setNotes(notes.filter(note => note.id !== id));
        } catch (error) {
            console.error('Error deleting note:', error);
        }
    };

    const handleEditNote = (note) => {
        setTitle(note.title);
        setText(note.text);
        setEditNoteId(note.id);
    };

    return (
        <div className="notes-container">
            <h1>Notas</h1>
            <div className="input-container">
                <input
                    type="text"
                    placeholder="Título"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <textarea
                    placeholder="Texto"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                ></textarea>
                <button onClick={editNoteId ? () => handleUpdateNote(editNoteId) : handleAddNote}>
                    {editNoteId ? 'Actualizar Nota' : 'Agregar Nota'}
                </button>
            </div>
            <ul>
                {notes.map(note => (
                    <li key={note.id}>
                        <h2>{note.title}</h2>
                        <p>{note.text}</p>
                        <div className="note-buttons">
                            <button onClick={() => handleEditNote(note)}>Editar</button>
                            <button onClick={() => handleDeleteNote(note.id)}>Eliminar</button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Notes;