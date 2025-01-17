import React, { useState } from "react";
import "../../styles/Header.css";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleMenu = () => {
    setMenuOpen((prev) => !prev);
  };


  const handleClose = (route) => {
    setMenuOpen(false);
    window.location.href = route;
    
  };

  

  return (
    <div
      className="header-root"
      style={{ backgroundColor: "#2C3E50", color: "#ECF0F1" }}
    >
      <div className="app-bar">
        <div
          className="toolbar"
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "10px 20px",
          }}
        >
          <button
            className="menu-button"
            onClick={handleMenu}
            aria-label="menu">
            ☰
          </button>
          <div
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "10px 20px",
                width: '100%'
            }}>
            <h1
                className="title"
                style={{ margin: 0, fontSize: "24px", fontWeight: "bold" }}
            >
                SAS
            </h1>
            <div
                className="nav-buttons"
                style={{ display: "flex", gap: "15px" }}
            >
                <button
                    className="nav-button"
                    onClick={() => handleClose('/')}
                    style={{
                        backgroundColor: "transparent",
                        border: "2px solid #1ABC9C",
                        padding: "8px 15px",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontWeight: "bold",
                    }}
                    >
                Home
                </button>
                <button
                    className="nav-button"
                    onClick={() => handleClose('attendance')}
                    style={{
                        backgroundColor: "transparent",
                        border: "2px solid #1ABC9C",
                        padding: "8px 15px",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontWeight: "bold",
                    }}
                    >
                Attendance
                </button>

                <button
                    className="nav-button"
                    onClick={() => handleClose('students')}
                    style={{
                        backgroundColor: "transparent",
                        border: "2px solid #1ABC9C",
                        padding: "8px 15px",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontWeight: "bold",
                    }}>
                    Students
                </button>

                <button
                    onClick={() => handleClose('profile')}
                    className="nav-button"
                    style={{
                        backgroundColor: "transparent",
                        border: "2px solid #1ABC9C",
                        padding: "8px 15px",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontWeight: "bold",
                    }}
                    >
                    Profile
                </button>

            </div>
            </div>

        </div>
        {menuOpen && (
          <>
            <div
              className="overlay"
              onClick={() => handleClose('/')}
              style={{
                position: "fixed",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                backgroundColor: "rgba(0, 0, 0, 0.5)",
                zIndex: 998,
              }}
            ></div>
            <div
              className="menu"
              style={{
                position: "fixed",
                top: 0,
                left: 0,
                width: "250px",
                height: "100%",
                zIndex: 999,
                padding: "20px",
                display: "flex",
                flexDirection: "column",
                gap: "15px",
              }}
            >
                <h2 >SAS</h2>
                <div
                    className="menu-item"
                    onClick={() => handleClose('/')}
                    style={{
                    fontSize: "18px",
                    cursor: "pointer",
                    padding: "10px",
                    borderBottom: "1px solid #1ABC9C",
                    }}  
                    >
                    Home
                </div>
                <div
                    className="menu-item"
                    onClick={() => handleClose('attendance')}
                    style={{
                    fontSize: "18px",
                    cursor: "pointer",
                    padding: "10px",
                    borderBottom: "1px solid #1ABC9C",
                    }}
                >
                    Attendance
                </div>

                <div
                    className="menu-item"
                    onClick={() => handleClose('students')}
                    style={{
                    fontSize: "18px",
                    cursor: "pointer",
                    padding: "10px",
                    borderBottom: "1px solid #1ABC9C",
                    }}
                >
                    Students
                </div>

                <div
                    className="menu-item"
                    onClick={() => handleClose('profile')}
                    style={{
                    fontSize: "18px",
                    cursor: "pointer",
                    padding: "10px",
                    borderBottom: "1px solid #1ABC9C",
                    }}
                >
                    Profile
                </div>

            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Header;
