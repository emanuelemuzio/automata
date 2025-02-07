import { useState } from "react";
import { fetchWithAuth } from "../api/authService";
import "../styles/UploadDocument.css";

function UploadDocument() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setUploadStatus(null); // Reset dello stato del messaggio
    } else {
      setUploadStatus("Errore: Devi selezionare un file PDF.");
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("Seleziona prima un file PDF.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetchWithAuth("/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json()

      if (!response.ok) throw new Error("Errore durante il caricamento del file.");

      setUploadStatus("File caricato con successo!");
      setFile(null);
    } catch (error) {
      setUploadStatus(error.message);
    }
  };

  return (
    <div className="upload-container">
      <h2>Carica un Documento PDF</h2>

      <input type="file" accept="application/pdf" onChange={handleFileChange} />

      {file && <p className="file-name">📄 {file.name}</p>}

      <button className="upload-button" onClick={handleUpload} disabled={!file}>
        Carica
      </button>

      {uploadStatus && <p className={`upload-status ${uploadStatus.includes("Errore") ? "error" : "success"}`}>
        {uploadStatus}
      </p>}
    </div>
  );
}

export default UploadDocument;
