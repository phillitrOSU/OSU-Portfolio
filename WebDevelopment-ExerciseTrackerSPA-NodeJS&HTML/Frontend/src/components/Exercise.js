import React from 'react';
import { AiFillDelete, AiFillEdit } from 'react-icons/ai';

function Exercise({ exercise, onEdit, onDelete }) {
    return (
        <tr>
            <td>{exercise.name}</td>
            <td>{exercise.reps}</td>
            <td>{exercise.weight}</td>
            <td>{exercise.unit}</td>
            <td>{exercise.date.substring(0,10)}</td>
            <td className = 'tableButton'><AiFillDelete onClick={() => onDelete(exercise._id)} /></td>
            <td className = 'tableButton'><AiFillEdit onClick={() => onEdit(exercise)} /></td>
        </tr>
    );
}

export default Exercise;