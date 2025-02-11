import { useEffect, useState } from "react";
import * as jwtDecode from "jwt-decode";
import { refreshAccessToken } from "../api/authService";

function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true)
  const [userRole, setUserRole] = useState(null);

  function checkTokenValidity() {
    setIsLoading(true);
    const token = localStorage.getItem("token");
    if (!token) {
      return false
    }; 

    try {
      const decodedToken = jwtDecode.jwtDecode(token);
      const currentTime = Date.now() / 1000;  

      if (decodedToken.exp < currentTime) {
        return false;  
      }
      
      setUserRole(decodedToken.role);
      return true;
    } catch (error) {
      return false;
    } finally {
      setIsLoading(false);
    }
  }

  async function handleTokenRefresh() {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const decodedToken = jwtDecode.jwtDecode(token);
      const currentTime = Date.now() / 1000;
      const timeLeft = decodedToken.exp - currentTime;

      if (timeLeft < 300) {  
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
    setIsAuthenticated(checkTokenValidity());  
    const interval = setInterval(handleTokenRefresh, 120000);  
    return () => clearInterval(interval);
  }, []);

  return { isAuthenticated, userRole, logout, isLoading };
}

export default useAuth;
