import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const CreateExercisePage = () => {

    const [name, setName]       = useState('');
    const [reps, setReps]         = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');
    
    const history = useHistory();

    const CreateExercise = async () => {
        const newExercise = { name, reps, weight, unit, date };
        const response = await fetch('/exercises', {
            method: 'post',
            body: JSON.stringify(newExercise),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if(response.status === 201){
            alert("Successfully added the exercise!");
        } else {
            alert(`Failed to add exercise, status code = ${response.status}`);
        }
        history.push("/");
    };


    return (
        <>
        <article>
            <h2>Okay stud -- what have you accomplished this week?</h2>
            <p><i>Let's write it down!</i></p>
            <form onSubmit={(e) => { e.preventDefault();}}>
                <fieldset>
                    <legend>Enter your exercise</legend>
                    <label htmlFor="name">Exercise name</label>
                    <input
                        type="text"
                        placeholder="squats, press, etc."
                        value={name}
                        onChange={e => setName(e.target.value)} 
                        id="name" />
                    
                    <label htmlFor="reps">Reps</label>
                    <input
                        type="number"
                        placeholder="10, 20, etc."
                        value={reps}
                        onChange={e => setReps(e.target.value)} 
                        id="reps" />

                    <label htmlFor="weight">Amount of weight</label>
                    <input
                        type="number"
                        value={weight}
                        placeholder="30, 40, etc."
                        onChange={e => setWeight(e.target.value)} 
                        id="weight" />

                    <label htmlFor="unit">Weight Unit:</label>
                    <select id = "unit" name = "unit" value={unit} onChange={e => setUnit(e.target.value)} >
                        <option>Select Unit</option>
                        <option value="lbs">lbs</option>
                        <option value="kgs">kgs</option>
                    </select>
                    
                    <label htmlFor="date">Date Performed</label>
                    <input
                        type="date"
                        value={date}
                        placeholder="01-01-01"
                        onChange={e => setDate(e.target.value)} 
                        id="date" />
                    
                    <label htmlFor="submit">
                    <button
                        type="submit"
                        onClick={CreateExercise}
                        id="submit"
                    >Add Exercise</button></label>
                </fieldset>
                </form>
            </article>
        </>
    );
}

export default CreateExercisePage;