// Import dependencies
import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { useState } from 'react';

// Import Components, styles, media
import Navigation from './components/Navigation';
import './App.css';

// Import Pages
import HomePage from './pages/HomePage';
import CreateExercisePage from './pages/CreateExercisePage';
import EditExercisePage from './pages/EditExercisePage';

// Define the function that renders the content in routes using State.
function App() {

  const [exerciseToEdit, setExerciseToEdit] = useState([]);

  return (
    <>
      <Router>

          <header>
            <h1>Workout Logger</h1>
            <p>You do the <b>work</b> and we'll keep <b>track</b>.</p>
          </header>

          <Navigation />

          <main>
            <Route path="/" exact>
              <HomePage setExerciseToEdit={setExerciseToEdit} />
            </Route>

            <Route path="/create-exercise">
              <CreateExercisePage />
            </Route>
            
            <Route path="/edit-exercise">
              <EditExercisePage  exerciseToEdit={exerciseToEdit} />
            </Route>
          </main>

          <footer>
            <p>2022 Copyright Trevor Phillips</p>
          </footer>

      </Router>
    </>
  );
}

export default App;