export async function handleResponse(response) {

  let data; 

  if(response.body){
    data = await response.json()
  }
  else{
    data = await response;
  }

  let errorMessage;

  switch (response.status) {
    case 200:
      return data;
    case 304:
      return data;
    case 401:
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";   
      break;
    default:
      errorMessage = data.detail ?? "Si è verificato un errore.";
      break;
  }

  throw new Error(errorMessage); 
}
