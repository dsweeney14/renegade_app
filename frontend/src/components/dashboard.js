import React from "react";
import { useAuthContext } from "../authContext";
import NavColumn from "./NavColumn";
import TickerTable from "./TickerTable";

import "../styles/dashboard.css";

// This file contains the components of the Dashboard page. 

const Dashboard = () => {
  const auth = useAuthContext();

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-heading">DASHBOARD</h1>
      <div className="content-container">
        <div className="nav-column-container">
          <NavColumn />
        </div>
        <div className="table-container">
          <TickerTable />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
