import 'dotenv/config';
import express from 'express';
import * as exercise from './exercise-model.mjs';

const PORT = process.env.PORT;
const app = express();
app.use(express.json());


// CREATE controller ******************************************
app.post ('/exercises', (req,res) => { 
    exercise.createExercise(
        req.body.name, 
        req.body.reps, 
        req.body.weight,
        req.body.unit,
        req.body.date,
        )
        .then(exercise => {
            res.status(201).json(exercise);
        })
        .catch(error => {
            console.log(error);
            res.status(400).json({ Error: 'Invalid request' });
        });
});


// RETRIEVE controller ****************************************************
// GET exercises by ID
app.get('/exercises/:_id', (req, res) => {
    const exerciseId = req.params._id;
    exercise.findExerciseById(exerciseId)
        .then(exercise => { 
            if (exercise !== null) {
                res.json(exercise);
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }         
         })
        .catch(error => {
            res.status(400).json({ Error: 'Request failed' });
        });

});

// GET exercises filtered by name, reps, weight, unit or date.
app.get('/exercises', (req, res) => {
    let filter = {};
    // filter by name
    if(req.query.name !== undefined){
        filter = { name: req.query.name };
    }
    // filter by reps
    if(req.query.reps !== undefined){
        filter = { reps: req.query.reps };
    }
    // filter by weight
    if(req.query.weight !== undefined){
        filter = { weight: req.query.weight };
    }
    // filter by unit
    if(req.query.unit !== undefined){
        filter = { unit: req.query.unit };
    }
    // filter by date
    if(req.query.date !== undefined){
        filter = { date: req.query.date };
    }
    exercise.findExercises(filter, '', 0)
        .then(exercises => {
            res.send(exercises);
        })
        .catch(error => {
            console.error(error);
            res.send({ Error: 'Request failed' });
        });
});

// UPDATE controller ************************************
app.put('/exercises/:_id', (req, res) => {
    if(req.body.name === undefined || req.body.reps === undefined || req.body.weight === undefined
        || req.body.unit === undefined || req.body.date === undefined){
            res.status(400).json({ Error: 'Missing property'})
            return
        }
    exercise.replaceExercise(req.params._id, req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(matchedCount => {
            if(matchedCount === 1){
                res.json({message: "Replaced exercise"});
            } else{
                res.status(404).json({ Error: 'Not Found' });
            }          
        })
        .catch(error => {
            console.error(error);
            res.status(400).json({ Error: 'Request failed.'}) 
        });
});

// DELETE Controller ******************************
app.delete('/exercises/:_id', (req, res) => {
    exercise.deleteById(req.params._id)
        .then(deletedCount => {
            if (deletedCount === 1) {
                console.log(deletedCount)
                res.status(204).send();
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.send({ error: 'Request failed' });
        });
});



app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});