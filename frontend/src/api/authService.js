import config from "../config";
import { handleResponse } from "../handlers/errorHandler";
import { handleDownload } from "../handlers/downloadHandler";

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

    const data = await handleResponse(response);

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

    const data = await handleResponse(response);

    localStorage.setItem("token", data.access_token);
    return data.access_token;
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function fetchWithAuth(url, options = {}) {
  try {
    let token = localStorage.getItem("token");

    if (!options.headers) options.headers = {};
    options.headers["Authorization"] = `Bearer ${token}`;

    let response = await fetch(`${config.BACKEND_URL}${url}`, options);

    let data;

    if(url.includes("download")){
      data = await handleDownload(response)
    } else{
      data = await handleResponse(response)
    }

    return data
  }
  catch (error) {
    return { success: false, error: error.message };
  }
}
