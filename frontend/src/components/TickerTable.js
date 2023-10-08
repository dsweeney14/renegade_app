import axios from "axios";
import React, { useEffect, useState } from "react";
import { NavDropdown, Nav } from 'react-bootstrap';

const TickerTable = ({ symbol, price }) => {
  const [tickers, setTickers] = useState([]);
  const [filter, setFilter] = useState("GBP");

  const fetchData = async () => {
    try {
      const response = await axios.get("tickers/tickers");
      const tableData = response.data;
      setTickers(tableData);
    } catch (error) {
      // Handle any errors
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
    const timer = setInterval(() => {
      fetchData();
    }, 15000);
    return () => {
      clearInterval(timer);
    };
  }, []);

  const filteredTickers = tickers.filter((ticker) =>
    ticker.symbol.endsWith(filter)
  );

  const sortedTickers = [...filteredTickers].sort(
    (a, b) => parseFloat(b.price) - parseFloat(a.price)
  );

  const handleFilterClick = (ending) => {
    setFilter(ending);
  };

  return (
    <div>
      <Nav variant="tabs" className="justify-content-end">
        {/* Create filter links using NavDropdown from react-bootstrap */}
        <Nav.Item>
          <Nav.Link active>Quote Currency: {filter}</Nav.Link>
        </Nav.Item>
        <NavDropdown title="Fiat Quotes" id="nav-dropdown">
          <NavDropdown.Item onClick={() => handleFilterClick('TRY')}>TRY</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('EUR')}>EUR</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('BRL')}>BRL</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('ARS')}>ARS</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('BIDR')}>BIDR</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('GBP')}>GBP</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('IDRT')}>IDRT</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('NGN')}>NGN</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('PLN')}>PLN</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('RON')}>RON</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('RUB')}>RUB</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('UAH')}>UAH</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('USD')}>USD</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('ZAR')}>ZAR</NavDropdown.Item>
        </NavDropdown>
        <NavDropdown title="Crypto Quotes" id="nav-dropdown">
          <NavDropdown.Item onClick={() => handleFilterClick('USDT')}>USDT</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('TUSD')}>TUSD</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('BUSD')}>BUSD</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('BNB')}>BNB</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('BTC')}>BTC</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('ETH')}>ETH</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('DAI')}>DAI</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('USDC')}>USDC</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('VAI')}>VAI</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('XRP')}>XRP</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('TRX')}>TRX</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('DOGE')}>DOGE</NavDropdown.Item>
          <NavDropdown.Item onClick={() => handleFilterClick('DOT')}>DOT</NavDropdown.Item>
        </NavDropdown>
        {/* Add more filter links as needed */}
      </Nav>

      <table className="table">
        <thead>
          <small>Binance Exchange Data (Updates: 15s)</small>
          <tr>
            <th>Ticker</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          {sortedTickers.map((ticker, index) => (
            <tr key={index}>
              <td>{ticker.symbol}</td>
              <td>{ticker.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TickerTable;
