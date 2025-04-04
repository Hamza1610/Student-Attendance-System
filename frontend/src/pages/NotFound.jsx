import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/NotFound.css'; // Import custom CSS for styling and animations

const NotFound = () => {
  useEffect(() => {
    document.title = "404 - Page Not Found";
  }, []);

  return (
    <div className="not-found-container">
      <div className="error-code">404</div>
      <div className="message">
        Oops! The page you're looking for could not be found.
      </div>
      <div className="animation-container">
        <div className="ufo">
          <div className="body"></div>
          <div className="glass"></div>
          <div className="light"></div>
        </div>
      </div>
      <Link to="/" className="home-link">
        <span className="home-icon">🏠</span> Back to Home
      </Link>
    </div>
  );
};

export default NotFound;
// import { Link } from 'react-router-dom';

// const NotFound = () => {
//   return (
//     <div className='not-found'>
//       <h1>404 - Page Not Found</h1>
//       <Link to="/">Go to Home</Link>
//     </div>
//   );
// };

// export default NotFound;
