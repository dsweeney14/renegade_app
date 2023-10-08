import React from "react";
import { useAuthContext } from "../authContext";
import { logout } from "../auth";
import UseLogout from "./logout"
import transparentLogo from "../images/renegade-high-resolution-logo-color-on-transparent-background.png";

import '../styles/NavColumn.css'

// This file contains the functionality for the navigation column

const NavColumn = () => {
  const auth = useAuthContext();
  const redirectLogout = UseLogout()
  const handleLogout = () => {
    logout();
    auth.logoutContext();
    redirectLogout();
  };

  return (
    <div className="navcolumn-container">
      <img className="img" src={transparentLogo} alt="Logo" />
      <ul className="nav flex-column">
        <li className="nav-item">
          <a className="nav-link active" aria-current="page" href="/dashboard">
            Dashboard
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/portfolio">
            Portfolio
          </a>
        </li>
        <a className="button" onClick={handleLogout}>
          Logout
        </a>
      </ul>
    </div>
  );
};

export default NavColumn;
