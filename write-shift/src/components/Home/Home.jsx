import React, { useState } from 'react';
import './Home.css';

function Home() {
    const [file, setFile] = useState(null);  // Track the selected file
    const [outputText, setOutputText] = useState('');  // Track the generated text

    // Function to handle file selection
    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        setFile(selectedFile);  // Set the selected file in state
    };

    // Function to handle image upload and fetch predicted text from backend
    const handleImageUpload = (file) => {
        const formData = new FormData();
        formData.append('image', file);

        fetch('http://localhost:5000/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log("Predicted character:", data.character);
            setOutputText(data.character);  // Set the generated text in state
        })
        .catch(error => console.error("Error:", error));
    };

    // Call this when user clicks 'Upload and Recognize'
    const handleFileUpload = () => {
        if (file) {
            handleImageUpload(file);  // Upload the file and recognize the text
        } else {
            alert('Please select a file first.');
        }
    };

    return (
        <>
            <section className='video-sect'>
                <video autoPlay loop muted playsInline>
                    <source src="/Written-Text.mp4" type="video/mp4" />
                </video>
            </section>

            <section className="content-sect">
                <div className="content-wrapper">
                    <div className="upload-area">
                        <input 
                            type="file" 
                            className='file-selector' 
                            onChange={handleFileChange}
                        />
                        <p> Drag and drop a file here, or click to select a file </p>
                        <button onClick={handleFileUpload}>Upload and Recognize</button>
                    </div>

                    <div className="text-display">
                        <h2> Generated Text </h2>
                        <p className="output-text">{outputText}</p>
                    </div>
                </div>
            </section>
        </>
    );
}

export default Home;
