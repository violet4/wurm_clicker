import './App.css';

import axios from 'axios';

import $ from "jquery";

import React, { useState, useEffect } from "react";



const get_image_click_coordinates = (event) => {
  var rect = event.target.getBoundingClientRect();
  console.log(rect)
  console.log("event.clientX", event.clientX)
  console.log("event.clientY", event.clientY)

  var x = Math.round(event.clientX - rect.left); //x position within the element.
  var y = Math.round(event.clientY - rect.top);  //y position within the element.
  axios.get(`/click/${x}/${y}`)
};



const ImageComponent = ({url}) => {
  const [image, setImage] = useState("");

  useEffect(() => {
    const fetchImage = async () => {
      const response = await fetch(url);
      const imageBlob = await response.blob();
      const imageObjectURL = URL.createObjectURL(imageBlob);
      setImage(imageObjectURL);
    };

    fetchImage();
    const intervalId = setInterval(() => {
      fetchImage();
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      {image ?
        <img
          id={"my_image"}
          src={image} alt="Screen Shot"
          onClick={get_image_click_coordinates}
        />
        : <p>Loading...</p>
      }
    </div>
  );
};

function App() {
  return (
    <div className="App">
      {/* <header className="App-header">
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}

      <ImageComponent url={"/screenshot"}/>

    </div>
  );
}

export default App;
