import React, { useEffect, useState } from "react";
import "../styles/analysisLoading.css";

// This file contains the functionality for the loading screen while the backtest algorithm is running.

const LoadingScreen = ({ onCancel }) => {
  const [loadingIconHTML, setLoadingIconHTML] = useState("");

  useEffect(() => {
    const fetchLoadingIconHTML = async () => {
      try {
        const response = await fetch("/loadingIcon.html");
        const htmlContent = await response.text();
        setLoadingIconHTML(htmlContent);
      } catch (error) {
        console.error("Failed to fetch loading icon HTML:", error);
      }
    };

    fetchLoadingIconHTML();
  }, []);
  return (
    <div className="loading-container">
      <div
        className="loading-icon-container"
        dangerouslySetInnerHTML={{ __html: loadingIconHTML }}
      />
      <h2 className="main-message">
        Please wait while our analysis software is running.
      </h2>
      <h3 className="sub-message">
        Allow for up to 60 minutes while the program finds you profitable
        opportunities!
      </h3>
      <button className="loading-button" onClick={onCancel}>
        Cancel
      </button>
    </div>
  );
};

export default LoadingScreen;
