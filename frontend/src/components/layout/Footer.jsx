import React from 'react';

const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer style={{ textAlign: 'center', padding: '1em 0', background: '#f1f1f1' }}>
            <p>&copy; {currentYear} Student Attendance System. All rights reserved.</p>
        </footer>
    );
};

export default Footer;