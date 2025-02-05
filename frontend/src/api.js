const API_URL = import.meta.env.VITE_API_URL;

fetch(`${API_URL}/api/endpoint`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error("Errore nella richiesta API:", error));
