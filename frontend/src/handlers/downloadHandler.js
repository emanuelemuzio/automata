export async function handleDownload(response) {

  let errorMessage;

  switch (response.status) {
    case 200:
      return response;
    case 304:
      return response;
    case 401:
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";   
      break;
    default:
      const data = await response.json();
      errorMessage = data.detail ?? "Si è verificato un errore.";
      break;
  }

  throw new Error(errorMessage); 
}
