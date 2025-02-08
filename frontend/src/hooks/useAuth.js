import { useEffect, useState } from "react";
import * as jwtDecode from "jwt-decode";
import { refreshAccessToken } from "../api/authService";

function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState(null);

  function checkTokenValidity() {
    const token = localStorage.getItem("token");
    if (!token) return false; 

    try {
      const decodedToken = jwtDecode.jwtDecode(token);
      const currentTime = Date.now() / 1000; // Convertiamo in secondi 

      if (decodedToken.exp < currentTime) {
        return false; // Il token è già scaduto
      }
      
      setUserRole(decodedToken.role);
      return true;
    } catch (error) {
      console.log(error)
      return false;
    }
  }

  async function handleTokenRefresh() {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const decodedToken = jwtDecode.jwtDecode(token);
      const currentTime = Date.now() / 1000;
      const timeLeft = decodedToken.exp - currentTime;

      if (timeLeft < 300) { // Se mancano meno di 5 minuti alla scadenza, rinnova il token
        const newToken = await refreshAccessToken();
        if (!newToken) {
          logout();
        } else {
          setIsAuthenticated(true);
          setUserRole(jwtDecode(newToken).role);
        }
      }
    } catch (error) {
      console.error("Error decoding token:", error);
      logout();
    }
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    setIsAuthenticated(false);
    setUserRole(null);
  }

  useEffect(() => {
    setIsAuthenticated(checkTokenValidity()); // Aggiorna lo stato all'avvio
    const interval = setInterval(handleTokenRefresh, 120000); // Controlla ogni due minuti
    return () => clearInterval(interval);
  }, []);

  return { isAuthenticated, userRole, logout };
}

export default useAuth;
