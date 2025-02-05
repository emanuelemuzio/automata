const API_URL = import.meta.env.VITE_API_URL;

export const loginUser = async (username, password) => {
  // Creazione del body in formato x-www-form-urlencoded
  const formData = new URLSearchParams();
  formData.append("grant_type", "password");
  formData.append("username", username);
  formData.append("password", password);
  formData.append("scope", "");
  formData.append("client_id", "string");
  formData.append("client_secret", "string");

  try {
    const response = await fetch(`${API_URL}/token`, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Credenziali non valide");
    }

    const data = await response.json();
    
    // Salviamo il token e il tipo di token
    return { success: true, token: data.access_token, tokenType: data.token_type };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
