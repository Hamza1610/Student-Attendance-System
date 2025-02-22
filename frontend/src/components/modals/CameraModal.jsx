import React, { useState } from "react";
import { useStudents } from "../../contexts/StudentContext";
import "../../styles/Modal.css";
import FaceRecognitionAttendance from "../attendance/AttendanceCamera";

const CameraModal = ({ classDetail, isOpen, onClose }) => {

    console.log("Detail 1:", classDetail);
    
    return (
        <div className="modal-overlay-bg" >
        <div className="modal-content">
            <button className="modal-close" onClick={onClose} aria-label="Close">
            &times;
            </button>
            <div className="modal-actions" style={{
                padding: '20px',
            }}>
                <FaceRecognitionAttendance  classDetail={classDetail}/>
            </div>
        </div>
        </div>
    );
};

export default CameraModal;
