const API_URL = import.meta.env.VITE_API_URL;

export const fetchData = async (endpoint, options = {}) => {
  const token = localStorage.getItem("token");
  const tokenType = localStorage.getItem("token_type");

  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `${tokenType} ${token}` } : {}), // 👈 Ora aggiungiamo anche `token_type`
  };

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error("Errore nella risposta API");
    }

    return await response.json();
  } catch (error) {
    console.error("Errore API:", error);
    return null;
  }
};
