import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const PrivateRoute = ({ component: Component, ...rest }) => {
    const { currentUser } = useAuth();

    // This lofgic will redirect user tyo login page if haven't logged 
    if (!currentUser) {
        return <Navigate to="/login" />;
    }

    return <component {...rest} />;
};

export default PrivateRoute;
