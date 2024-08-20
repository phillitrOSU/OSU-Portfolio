import React from 'react';
import ExerciseList from '../components/ExerciseList';
import { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

function HomePage({ setExerciseToEdit }) {
    // Use the history for updating
    const history = useHistory();

    // Use state to bring in the data
    const [exercises, setExercises] = useState([]);

    // RETRIEVE the list of exercises
    const loadExercises = async () => {
        const response = await fetch('/exercises');
        const exercises = await response.json();
        setExercises(exercises);
    } 
    
    // UPDATE an exercise
    const onEditExercise = async exercise => {
        setExerciseToEdit(exercise);
        history.push("/edit-exercise");
    }

    // DELETE an exercise
    const onDeleteExercise = async _id => {
        const response = await fetch(`/exercises/${_id}`, { method: 'DELETE' });
        if (response.status === 204) {
            const getResponse = await fetch('/exercises');
            const exercises = await getResponse.json();
            setExercises(exercises);
        } else {
            console.error(`Failed to delete exercise with _id = ${_id}, status code = ${response.status}`)
        }
    }

    // LOAD the exercises
    useEffect(() => {
        loadExercises();
    }, []);

    // DISPLAY the movies
    return (
        <>
            <article>
                <h2>Let's tally up your hardwork!</h2>
                <p>Record and view your exercises below.</p>
                <ExerciseList 
                    exercises={exercises} 
                    onEdit={onEditExercise} 
                    onDelete={onDeleteExercise} 
                />
            </article>
        </>
    );
}

export default HomePage;