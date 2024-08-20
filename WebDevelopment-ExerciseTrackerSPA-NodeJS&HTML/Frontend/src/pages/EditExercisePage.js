import React from 'react';
import { useHistory } from "react-router-dom";
import { useState } from 'react';

export const EditExercisePage = ({ exerciseToEdit }) => {
 
    const [name, setName]       = useState(exerciseToEdit.name);
    const [reps, setReps]       = useState(exerciseToEdit.reps);
    const [weight, setWeight]   = useState(exerciseToEdit.weight);
    const [unit, setUnit]       = useState(exerciseToEdit.unit);
    const [date, setDate]       = useState(exerciseToEdit.date);
    
    const history = useHistory();

    console.log(date)

    const editExercise = async () => {
        console.log(`Adding exercise with ${name}, ${reps}, ${weight}, ${unit}, ${weight}. ${date}`)
        const response = await fetch(`/exercises/${exerciseToEdit._id}`, {
            method: 'PUT',
            body: JSON.stringify({ 
                name: name,
                reps: reps,
                weight: weight,
                unit: unit,
                date: date
            }),
            headers: {'Content-Type': 'application/json',},
        });
        if (response.status === 200) {
            alert("Successfully edited exercise!");
        } else {
            const errMessage = await response.json();
            alert(`Failed to update exercise. Status ${response.status}. ${errMessage.Error}`);
        }
        history.push("/");
    }

    return (
        <>
        <article>
            <h2>Need to change something?</h2>
            <p><i>Let's do some editing...</i></p>
            {/* <p>Update the name, reps, weight, unit or date.</p> */}
            <form onSubmit={(e) => { e.preventDefault();}}>
                <fieldset>
                    <legend>Update Any Field</legend>

                    <label htmlFor="name">Exercise name</label>
                    <input
                        type="text"
                        value={name}
                        onChange={e => setName(e.target.value)} 
                        id="name" />
                    
                    <label htmlFor="reps">Number of Reps</label>
                    <input
                        type="number"
                        value={reps}
                        onChange={e => setReps(e.target.value)} 
                        id="reps" />

                    <label htmlFor="weight">Amount of Weight</label>
                    <input
                        type="number"
                        value={weight}
                        onChange={e => setWeight(e.target.value)} 
                        id="reps" />
                    
                    <label for="unit">Choose a unit:</label>
                    <select id = "unit" name = "unit" value={unit} onChange={e => setUnit(e.target.value)} >
                        <option value="lbs">lbs</option>
                        <option value="kgs">kgs</option>
                    </select>
                    
                    <label htmlFor="date">Date Performed</label>
                    <input
                        type="date"
                        value={date.substring(0,10)}
                        onChange={e => setDate(e.target.value)} 
                        id="reps" />

                    <label htmlFor="submit">
                    <button
                        onClick={editExercise}
                        id="submit"
                    >Save</button> Update the exercise</label>
                </fieldset>
                </form>
            </article>
        </>
    );
}
export default EditExercisePage;