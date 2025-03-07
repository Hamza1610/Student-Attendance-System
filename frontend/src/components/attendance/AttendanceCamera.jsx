import React, { useEffect, useRef, useState } from "react";
import * as faceapi from "face-api.js";
import Webcam from "react-webcam";
import '../../styles/AttendanceCamera.css'
import { useAttendance } from "../../contexts/AttendanceContext";
import apiClient from "../../services/api";


const FaceRecognitionAttendance = ({ classData, onClose }) => {
  // console.log("From FaceRecognitionAttendance Component:", classData);
  const webcamRef = useRef(null);
  const [modelsLoaded, setModelsLoaded] = useState(false);
  const [detections, setDetections] = useState([]);

  const { markAttendance, setError } = useAttendance();

  const handleMarkAttendance = async () => {
    try {
      markAttendance(classData, detections, webcamRef);
      onClose(null);
    } catch (error) {
      console.log(error);
      setError("Failed to mark attendance");
    }
  }
  // Load face-api.js models
  useEffect(() => {
    const loadModels = async () => {
      const MODEL_URL = "/models"; // Ensure models are in the public/models directory
      await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
      await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
      await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
      setModelsLoaded(true);
    };
    loadModels();
  }, []);

  // Perform face detection
  const detectFaces = async () => {
    if (
      webcamRef.current &&
      webcamRef.current.video.readyState === 4 &&
      modelsLoaded
    ) {
      const video = webcamRef.current.video;
      const detections = await faceapi
        .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks()
        .withFaceDescriptors();
      setDetections(detections); // Store detected faces
    }
  };



  useEffect(() => {
    const interval = setInterval(detectFaces, 100); // Detect faces every 100ms
    return () => clearInterval(interval);
  }, [modelsLoaded]);

  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ position: "relative", display: 'inline-block' }}>
          <Webcam
            ref={webcamRef}
            videoConstraints={{
              width: 600,
              height: 400,
              facingMode: "user",
            }}
            style={{
              borderRadius: "8px",
              border: "2px solid #ccc"
            }}
          />
          {detections.map((detection, index) => (
            <div
              key={index}
              style={{
                position: "absolute",
                border: "2px solid red",
                left: detection.detection.box.x,
                top: detection.detection.box.y,
                width: detection.detection.box.width,
                height: detection.detection.box.height,
              }}
            />
          ))}
          {detections.length > 0 && <p>{detections.length}st face(s) detected!</p>}
          {/* detections: shou;;d be replace with the image captured instead */}
          <button className="camera-btn" onClick={() => markAttendance(classData, detections, webcamRef)}>Record attendance</button>
      </div>
    </div>
  );
};

export default FaceRecognitionAttendance;
