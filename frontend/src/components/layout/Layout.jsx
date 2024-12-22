import React from 'react';
import { Outlet } from 'react-router-dom';

import Header from './Header';
import Footer from './Footer';
import '../../styles/Layout.css';

const Layout = (props) => {
    console.log(props);
    
    return (
        <div className="layout">
            <Header />
            <div className="layout-content">
                <main className="main-content">
                    {/* <Outlet /> */}
                    {props.children}
                </main>
            </div>
            <Footer />
        </div>
    );
};

export default Layout;