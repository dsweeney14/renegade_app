import React, { useState, useEffect } from "react";
import axios from "axios";
import remove from "../images/1564505_close_delete_exit_remove_icon.png";

// This file contains the functionality that renders the current portfolio component

const CurrentPortfolios = ({onViewClick}) => {
  const [portfolios, setPortfolios] = useState([]);
  const [activeStates, setActiveStates] = useState([]);
  const [isActive, setIsActive] = useState(false);

  const fetchData = async () => {
    try {
      const userId = sessionStorage.getItem("userId");
      const response = await axios.get(`/port/portfolios?userId=${userId}`);
      const activePortfolios = response.data;
      setPortfolios(activePortfolios);

      setActiveStates(activePortfolios.map((portfolio) => portfolio.isActive));
    } catch (error) {
      console.log("Error fetching data: ", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleActivation = async (portfolio, index) => {
    setActiveStates((prevStates) => {
      const newStates = [...prevStates];
      newStates[index] = !newStates[index];
      return newStates;
    });

    const dataToSend = {
      id: portfolio.id,
      asset1: portfolio.asset1,
      asset2: portfolio.asset2,
      user_id: portfolio.user_id,
    };

    if (isActive == false) {
      try {
        const response = await axios.post("/trade/initiate", dataToSend);
        setActiveStates((prevStates) => {
          const newStates = [...prevStates];
          newStates[index] = !newStates[index];
          return newStates;
        });
      } catch (error) {
        console.error("Error sending message:", error);
      }
    } else {
      try {
        const response = await axios.post("/trade/close", dataToSend);
        setIsActive(false);
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };

  const handleRemove = async (portfolioId) => {
    try {
      await axios.delete(`/trade/trades/${portfolioId}`);
      await axios.delete(`/port/portfolios/${portfolioId}`);
      window.location.reload();
    } catch (error) {
      console.error("Error deleting portfolio or table:", error);
    }
  };

  return (
    <div>
      <h2 className="current-port-heading">Current Portfolio</h2>
      {portfolios.length === 0 ? (
        <p className="no-active-message">
          You have no active pairs in your portfolio, run our algorithm to find
          new pairs!
        </p>
      ) : (
        <table className="current-table">
          <thead>
            <tr>
              <th className="asset-heading">Trading Pairs</th>
              <th></th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {portfolios.map((portfolio, index) => (
              <tr key={portfolio.portfolio_id}>
                <td className="assets">{`${portfolio.asset1} - ${portfolio.asset2}`}</td>
                <button
                  onClick={() => onViewClick(portfolio.id)}
                  className="view-button"
                >
                  View
                </button>
                <button
                  onClick={() => handleActivation(portfolio, index)}
                  className={`activation-button ${
                    activeStates[index] ? "active" : "deactive"
                  }`}
                >
                  {activeStates[index] ? "Deactivate" : "Activate"}
                </button>
                <button
                  onClick={() => handleRemove(portfolio.id)}
                  className="remove"
                >
                  <img src={remove} alt="remove button" />
                </button>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default CurrentPortfolios;
