import React, { useState } from "react";
import ReactDOM from "react-dom";
import Webcam from "react-webcam";

const videoConstraints = {
  width: 350,
  height: 350,
  facingMode: "user"
};

function CameraOn() {
  const webcamRef = React.useRef(null);
  const [image, setImage] = useState(undefined);
  const capture = React.useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
    console.log(imageSrc);
  }, [webcamRef]);
  return (
    <div>
     <h2 className="mb-4 cam">
       Ready to capture
      </h2>
      {!image ? (
        <div>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
          />
        </div>
      ) : (
        <img src={image} alt="test-ilustartion" />
      )}
      <br />
      <button className="btn btn-warning" onClick={() => (!image ? capture() : setImage(undefined))}>
        {!image ? "Capture photo" : "take photo"}
      </button>
    </div>
  );
}

export default CameraOn;


