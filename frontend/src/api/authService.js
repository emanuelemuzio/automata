import config from "../config";

export async function loginUser(username, password) {
  try {
    const response = await fetch(`${config.BACKEND_URL}/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "password",
        username: username,
        password: password,
        scope: "",
        client_id: "string",
        client_secret: "string"
      }),
    });

    if (!response.ok) {
      throw new Error("Invalid credentials");
    }

    const data = await response.json();
    return {
      success: true,
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      tokenType: data.token_type
    };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function refreshAccessToken() {
  const refreshToken = localStorage.getItem("refresh_token");
  if (!refreshToken) return null;

  try {
    const response = await fetch(`${BACKEND_URL}/refresh-token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }), 
    });

    if (!response.ok) {
      throw new Error("Failed to refresh token");
    }

    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    return data.access_token;
  } catch (error) {
    console.error("Token refresh failed:", error);
    return null;
  }
}

export async function fetchWithAuth(url, options = {}) {
  let token = localStorage.getItem("token");

  if (!options.headers) options.headers = {};
  options.headers["Authorization"] = `Bearer ${token}`;

  let response = await fetch(url, options);

  if (response.status === 401) { // Token scaduto
    token = await refreshAccessToken();
    if (!token) {
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
      return;
    }

    options.headers["Authorization"] = `Bearer ${token}`;
    response = await fetch(`${BACKEND_URL}${url}`, options); // Ritenta la richiesta con il nuovo token
  }

  return response;
}
