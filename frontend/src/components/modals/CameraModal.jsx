import React, { useState } from "react";
import { useStudents } from "../../contexts/StudentContext";
import "../../styles/Modal.css";
import FaceRecognitionAttendance from "../attendance/AttendanceCamera";

const CameraModal = ({ classData, onClose }) => {

    console.log("From CameraModal Component", classData);
    if (!classData) {
        console.log("From CameraModal Component: No classData found");
        return
    }

    return (
        <div className="modal-overlay-bg" >
        <div className="modal-content">
            <button className="modal-close" onClick={() => onClose(null)} aria-label="Close">
            &times;
            </button>
            <div className="modal-actions" style={{
                padding: '20px',
            }}>
                <FaceRecognitionAttendance  classData={classData} onClose={onClose}/>
            </div>
        </div>
        </div>
    );
};

export default CameraModal;
