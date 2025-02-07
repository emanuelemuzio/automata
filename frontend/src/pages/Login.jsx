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
    if (isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const response = await loginUser(username, password);

    if (response.success) {
      localStorage.setItem("token", response.access_token);
      localStorage.setItem("refresh_token", response.refresh_token);

      const redirectTo = location.state?.from?.pathname || "/dashboard";
      navigate(redirectTo, { replace: true });
    } else {
      setError(response.error);
    }
  };

  return (
    <main className="form-signin">
      <div className="container">
        <form onSubmit={handleSubmit}>
          <h1 className="h3 mb-3 fw-normal">Please sign in</h1>

          <div className="form-floating">
            <input type="email" className="form-control" id="floatingInput" placeholder="Email" value={username} onChange={(e) => setUsername(e.target.value)} required />
            <label htmlFor="floatingInput">Email address</label>
          </div>
          <div className="form-floating">
            <input type="password" className="form-control" id="floatinPassword" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <label htmlFor="floatingPassword">Password</label>
          </div>

          <button className="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
        </form>
        {error && <p className="error-message">{error}</p>}
      </div>
    </main>

  );
}

export default Login;
