import { useEffect, useState } from "react";

function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return !!localStorage.getItem("token"); // Controllo iniziale al caricamento
  });

  useEffect(() => {
    const checkAuth = () => {
      setIsAuthenticated(!!localStorage.getItem("token")); // Aggiorna ogni volta che il token cambia
    };

    // Esegui un primo controllo
    checkAuth();

    // Ascolta i cambiamenti su localStorage per logout/login
    window.addEventListener("storage", checkAuth);

    return () => window.removeEventListener("storage", checkAuth);
  }, []);

  return isAuthenticated;
}

export default useAuth;
