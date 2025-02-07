import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/authService";
import "../styles/UserDocuments.css";

function UserDocuments() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchDocuments() {
      try {
        const response = await fetchWithAuth("/documents/user_documents");

        if (!response.ok) {
          throw new Error("Errore nel recupero dei documenti.");
        }

        const data = await response.json();
        setDocuments(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchDocuments();
  }, []);

  const handleDownload = async (id, filename) => {
    try {
      const response = await fetchWithAuth(`/documents/download/${id}`);

      if (!response.ok) {
        throw new Error("Errore nel download del file.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename || `document_${id}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Errore durante il download:", error);
    }
  };

  return (
    <div className="documents-container">
      <h2>I Miei Documenti</h2>

      {loading && <p>Caricamento in corso...</p>}
      {error && <p className="error-message">{error}</p>}

      {!loading && !error && documents.length === 0 && <p>Non hai documenti caricati.</p>}

      {!loading && !error && documents.length > 0 && (
        <table className="documents-table">
          <thead>
            <tr>
              <th>Nome File</th>
              <th>Estensione</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id}>
                <td>{doc.filename}</td>
                <td>{doc.extension}</td>
                <td>
                  <button className="download-button" onClick={() => handleDownload(doc.id, doc.filename)}>
                    Scarica
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default UserDocuments;
