import NavColumn from "./NavColumn";
import "../styles/addPortfolio.css";
import OutputTable from "./createPortfolioTable";

// This file renders the components for the add portfolio page. (the page where you can add assets to your portfolio)

const AddPortfolio = () => {
  
  return (
    <div className="add-portfolio-container">
      <h1 className="add-portfolio-heading">Create Portfolio</h1>
      <div className="nav-column-container">
        <NavColumn />
      </div>
      <div className="output-container">
        <OutputTable />
      </div>
      
    </div>
  );
};

export default AddPortfolio;
