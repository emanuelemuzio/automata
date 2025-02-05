import { Link, useLocation } from "react-router-dom";
import "../styles/Navbar.css";

function Navbar() {
  const location = useLocation();
  const showNavbar = location.pathname === "/" || location.pathname === "/login"; 

  if (!showNavbar) return null;  

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="nav-logo">Automata</Link>
        <div className="nav-links">
          <Link to="/login">Accedi</Link>
          <Link to="/dashboard">Dashboard</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
