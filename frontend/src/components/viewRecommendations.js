import React from "react";
import "../styles/portfolio.css";

const Recommendations = ({ tradeData }) => {
  return (
    <div className="recommendation-container">
      <h2 className="recommendation-heading">Recommendations</h2>
      {tradeData.length === 0 ? (
        <p>No trade recommendations available.</p>
      ) : (
        <table className="recommendation-table">
          <thead>
            <tr>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {tradeData.map((trade, index) => (
              <tr key={index}>
                <td className="recommendations">{trade.recommendation}</td>
                <td className="time">{trade.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Recommendations;
