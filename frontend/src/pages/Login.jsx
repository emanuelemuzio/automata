import { useState, useEffect } from "react";
import { loginUser } from "../api/authService";
import { useNavigate, useLocation } from "react-router-dom";
import useAuth from "../hooks/useAuth"; 
import "../styles/Login.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthenticated = useAuth();

  useEffect(() => {
    if (isAuthenticated && location.pathname === "/login") {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate, location.pathname]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const response = await loginUser(username, password);

    if (response.success) {
      localStorage.setItem("token", response.token);
      localStorage.setItem("token_type", response.tokenType);

      // Se l'utente veniva da una rotta protetta, lo riporta lì
      const redirectTo = location.state?.from?.pathname || "/dashboard";
      navigate(redirectTo, { replace: true });
    } else {
      setError(response.error);
    }
  };

  return (
    <div className="login-container">
      <h2>Accedi</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Login</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default Login;