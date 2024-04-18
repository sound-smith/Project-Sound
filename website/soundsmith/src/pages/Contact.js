import '../App.css';
import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, useSearchParams, useNavigate } from "react-router-dom";
// import axios from 'axios';


const Contact = () => {
    const queryString = window.location.search.replace("?", "");
    const sp = new URLSearchParams(queryString);


    if (!sp.has("jwt")) {
        window.location.replace("http://localhost:3000");
    }

    const [emotionPredictions, setEmotionPredictions] = useState(null);
    const [description, setDescription] = useState('');

    const handleInputChange = (event) => {
        setDescription(event.target.value);
    };

    const handleBeginClick = async () => {
        let response;
        try {
            response = await fetch('http://localhost:8000/playlists/generate', {body:JSON.stringify({
              "description": description,
              "jwt": "66173c89b970969d7d8d5524",
              "keywords": "list of keywords",
              "mood": " "
            }),method:"POST",headers:{"Content-Type":"application/json","accept": "application/json"}});

            setEmotionPredictions(await response.json());

        } catch (error) {
            console.error('Error:', error);
        }
        console.log(emotionPredictions);
    };

    return (
        <div className="login">
            <header className="App-header">
                <h1 className="header-title">How are you feeling dawg</h1>
                <label className="header-label">You may put a few words or even a few sentences</label>
                <textarea
                    id="moodinput"
                    name="moodinput"
                    value={description}
                    onChange={handleInputChange}
                ></textarea>
                <div className="Clickable-text" onClick={handleBeginClick}>Generate Playlist</div>
                {emotionPredictions && (
                    <div>
                        <h2>Emotion Predictions below, now time to craft melodies</h2>
                        <pre>{JSON.stringify(emotionPredictions, null, 2)}</pre>
                    </div>
                )}
            </header>
        </div>
    );

};

export default Contact;