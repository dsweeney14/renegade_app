import { createRoot } from "react-dom/client";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RegisterForm from "./components/register";
import LoginForm from "./components/login";
import HomePage from "./components/home";
import Dashboard from "./components/dashboard";
import { AuthProvider } from "./authContext";
import { RequireAuth } from "./components/requireAuth";
import PortfolioMain from "./components/portfolio";
import AddPortfolio from "./components/addPortfolio";

// This is the main file that renders the front end

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="">
          <Routes>
            <Route path="/login" element={<LoginForm />} />
            <Route path="/register" element={<RegisterForm />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/portfolio" element={<RequireAuth><PortfolioMain /></RequireAuth>} />
            <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
            <Route path="/addPortfolio" element={<RequireAuth><AddPortfolio /></RequireAuth>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};

createRoot(document.getElementById("root")).render(<App />);
