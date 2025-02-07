import { Link, useLocation } from "react-router-dom";
import "../styles/Navbar.css";
import Logo from "./Logo";

function Navbar() {
  const location = useLocation();
  const showNavbar = location.pathname === "/" || location.pathname === "/login";

  if (!showNavbar) return null;

  return (
    <header className="p-3 bg-dark text-white">
      <div className="container">
        <div className="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
          <Link to="/" className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-decoration-none fs-4">
            <Logo width="72" height="72" />
          </Link>

          <Link to="/" className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-decoration-none fs-4 text-light">
            <span className="fs-2">Automata</span>
          </Link>

          <div className="text-end">
            <button type="button" className="btn btn-outline-light me-2">
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              </button>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
