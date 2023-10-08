import React, { useState, useEffect } from "react";
import "../styles/outputTable.css";
import add from "../images/add-3.7s-200px.png";
import { useNavigate } from 'react-router-dom'
import axios from "axios";

// This file contains the functionality to render the output of the backtest algorithm

const OutputTable = () => {
  const [analysisData, setAnalysisData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const response = JSON.parse(sessionStorage.getItem("analysisResponse"));
    console.log("response:", response);
    if (response) {
      const dataObjects = response.data.split("\n").filter(Boolean);
      const analysisArray = dataObjects.map((data, index) => ({
        id: index,
        ...JSON.parse(data)
      }));
      setAnalysisData(analysisArray);
    }
  }, []);

  const handleAdd = async (id) => {
    try {
      // Find the entry with the matching id from analysisData
      const entry = analysisData.find((item) => item.id === id);
  
      if (!entry) {
        console.error(`Entry with id ${id} not found.`);
        return;
      }
      const userId = sessionStorage.getItem("userId")
      const data = { entry, userId }
      const response = await axios.post("/port/portfolios", data);
      console.log(response)
      navigate('/portfolio')
    } catch (error) {
      console.error("Error adding entry:", error);
    }
  };


  return (
    <div className="output-container">
      <table className="tab-container">
        <thead>
          <tr className="tr">
            <th>Assets</th>
            <th>Sharpe Ratio</th>
            <th>Cumulative Returns</th>
          </tr>
        </thead>
        <tbody>
          {analysisData.map((entry) => (
            <tr key={entry.id}>
              <td className="td-assets">{`${entry["Ticker1"]} - ${entry["Ticker2"]}`}</td>
              <td className="td">{entry["Sharpe Ratio"]}</td>
              <td className="td">{entry["Cumulative Returns"]}</td>
              <td className="td-button">
                <button onClick={() => handleAdd(entry.id)} className="td-button">
                  <img src={add} atl="addButton" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OutputTable;
