import React, { useState } from "react";
import { useAuthContext } from "../authContext";
import NavColumn from "./NavColumn";
import CurrentPortfolios from "./currentPortfolios";
import Recommendations from "./viewRecommendations";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import LoadingScreen from "./AnalysisLoading";
import back from "../images/2203523_arrow_back_botton_left_icon.png";
import "../styles/portfolio.css";

// This is the main file for the portfolio component.

const PortfolioMain = () => {
  const auth = useAuthContext();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [cancelSource, setCancelSource] = useState(null);
  const [tradeData, setTradeData] = useState([]);
  const [mode, setMode] = useState("default");

  const initiateAnalysis = async () => {
    const source = axios.CancelToken.source();
    setCancelSource(source);

    try {
      setIsLoading(true);
      const response = await axios.get("/backtest/initiate", {
        cancelToken: source.token,
      });
      const jsonResponse = JSON.stringify(response);
      sessionStorage.setItem("analysisResponse", jsonResponse);
      setIsLoading(false);
      navigate("/addPortfolio");
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log("Request canceled: ", error.message);
      } else {
        setIsLoading(false);
        console.log(error);
      }
    }
  };

  const cancel = async () => {
    const send = await axios.post("/backtest/initiate");
    console.log(send);
    if (cancelSource) {
      cancelSource.cancel("Operation canceled by the user.");
      setIsLoading(false);
    }
  };

  const handleView = async (id) => {
    const response = await axios.get(`/trade/trades/${id}`);
    setTradeData(response.data);
    setMode("viewing");
  };

  const handleBack = () => {
    setMode("default")
  };

  return (
    <div className="portfolio-container">
      <h1 className="portfolio-heading">PORTFOLIO</h1>
      <div className="content-container">
        <div className="nav-column-container">
          <NavColumn />
        </div>
        {mode === "default" && (
          <div
            className={`active-portfolio-container ${
              isLoading ? "hidden" : ""
            }`}
          >
            <CurrentPortfolios onViewClick={handleView} />
          </div>
        )}
        {mode === "viewing" && (
          <div className="recommendations-container">
            <button onClick={handleBack} className="back-button">
              <img src={back} atl="backButton" /> Back to Portfolio
            </button>
            <Recommendations tradeData={tradeData} />
          </div>
        )}
        {isLoading ? (
          <div className="loading-screen">
            <LoadingScreen onCancel={cancel} />
          </div>
        ) : (
          <div className="button-div">
            <button
              className="portfolio-button"
              onClick={initiateAnalysis}
              disabled={isLoading}
            >
              {isLoading ? "Loading..." : "Find Pairs"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PortfolioMain;
