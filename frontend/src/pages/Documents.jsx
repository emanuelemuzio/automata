import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/authService";
import "../styles/Documents.css";  
import useAuth from "../hooks/useAuth";

function Documents() {
  const { isAuthenticated } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isAuthenticated) return;
    fetchDocuments();
  }, [isAuthenticated]);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const response = await fetchWithAuth("/document/by_user");
      if (!response.ok) throw new Error("Errore nel recupero dei documenti");

      const data = await response.json();
      setDocuments(data);
    } catch (error) {
      setError("Impossibile caricare la lista dei documenti");
      console.error("Errore nel recupero documenti:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
    } else {
      alert("Puoi caricare solo file PDF!");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Seleziona un file PDF da caricare");
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetchWithAuth("/document", {
        method: "PUT",
        body: formData,
      });

      if (!response.ok) throw new Error("Errore durante l'upload del documento");

      alert("Documento caricato con successo!");
      setSelectedFile(null);
      fetchDocuments();  
    } catch (error) {
      console.error("Errore nell'upload:", error);
      alert("Errore nell'upload del documento");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (documentId) => {
    if (!window.confirm("Sei sicuro di voler eliminare questo documento?")) return;

    try {
      const response = await fetchWithAuth(`/document?idx=${documentId}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Errore nell'eliminazione del documento");

      setDocuments(documents.filter((doc) => doc.id !== documentId));  
      alert("Documento eliminato con successo!");
    } catch (error) {
      console.error("Errore nell'eliminazione:", error);
      alert("Errore nell'eliminazione del documento");
    }
  };

  const handleDownload = async (documentId) => {
    try {
      const response = await fetchWithAuth(`/document/download?idx=${documentId}`);
      if (!response.ok) throw new Error("Errore nel download del documento");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "document.pdf";  
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (error) {
      console.error("Errore nel download:", error);
      alert("Errore nel download del documento");
    }
  };

  if (loading) return <p>Caricamento documenti...</p>;
  if (error) return <p className="text-danger">{error}</p>;

  return (
    <div className="container">
      <h2>I tuoi Documenti</h2>

      <div>
        <input type="file" className="form-control" accept="application/pdf" onChange={handleFileChange} />
        <button className="btn btn-primary mt-2" onClick={handleUpload} disabled={uploading}>
          {uploading ? "Caricamento..." : "Carica PDF"}
        </button>
      </div>

      <table className="table table-hover">
        <thead>
          <tr className="text-center">
            <th>ID</th>
            <th>Nome</th>
            <th>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {documents.length > 0 ? (
            documents.map((doc) => (
              <tr className="text-center" key={doc.id}>
                <td >{doc.id}</td>
                <td>{doc.filename}</td>
                <td>
                  <button title="Scarica" className="btn btn-success btn-sm me-2" onClick={() => handleDownload(doc.id)}>
                    <i className="bi bi-arrow-bar-down"></i>
                  </button>
                  <button title="Elimina" className="btn btn-sm btn-danger" onClick={() => handleDelete(doc.id)}>
                    <i className="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="text-center">Nessun documento disponibile</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Documents;
