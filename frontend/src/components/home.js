import React from "react";
import { useNavigate } from "react-router-dom";
import transparentLogo from "../images/renegade-high-resolution-logo-color-on-transparent-background.png";

import "../styles/home.css";

// This file contains renders the splash page. 

const HomePage = () => {
  const navigate = useNavigate();

  const handleRegisterClick = () => {
    navigate("/register");
  };

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <div className="main-home">
      <div className="container-home">
        <img className="img" src={transparentLogo} alt="Logo" />
        <div className="button-wrapper">
          <button className="button" onClick={handleLoginClick}>
            Login
          </button>
          <button className="button" onClick={handleRegisterClick}>
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
