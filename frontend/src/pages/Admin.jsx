import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/authService";
import "../styles/Admin.css";
import useAuth from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

function Admin() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { userRole, isAuthenticated } = useAuth();

    const [newUser, setNewUser] = useState({ full_name: "", username: "", pwd: "", role: "USER" });
    const [isCreating, setIsCreating] = useState(false);

    useEffect(() => {
        if (userRole === null) return;

        if (userRole !== "ADMIN") {
            navigate("/dashboard");
            return;
        }
        fetchUsers();
    }, [userRole, navigate]);

    const fetchUsers = async () => {
        setLoading(true);
        try {
            const response = await fetchWithAuth("/users");
            if (!response.ok) throw new Error("Errore nel recupero utenti");

            const data = await response.json();
            setUsers(data);
        } catch (error) {
            setError("Impossibile caricare la lista utenti");
            console.error("Errore nel recupero utenti:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (userId) => {
        if (!window.confirm("Sei sicuro di voler eliminare questo utente?")) return;

        try {
            const response = await fetchWithAuth(`/user/delete?user_id=${userId}`, {
                method: "GET",
            });
            if (!response.ok) throw new Error("Errore nella cancellazione dell'utente");

            setUsers(users.filter((user) => user.id !== userId)); 
        } catch (error) {
            console.error("Errore nell'eliminazione dell'utente:", error);
            alert("Errore nell'eliminazione dell'utente");
        }
    };

    const handleCreateUser = async () => {
        setIsCreating(true);
        try {
          const requestBody = {
            username: newUser.username,
            full_name: newUser.full_name,
            pwd: newUser.pwd,  
            id: null,  
            disabled: false  
          };
    
          const response = await fetchWithAuth("/users/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody),
          });
    
          if (!response.ok) throw new Error("Errore nella creazione dell'utente");
    
          const createdUser = await response.json();
          setUsers([...users, createdUser]); 
          setNewUser({ full_name: "", username: "", pwd: "", role: "USER" });  
          alert("Utente creato con successo!");
        } catch (error) {
          console.error("Errore nella creazione dell'utente:", error);
          alert("Errore nella creazione dell'utente");
        } finally {
          setIsCreating(false);
        }
      };

    if (loading) return <p>Caricamento utenti...</p>;
    if (error) return <p className="text-danger">{error}</p>;

    return (
        <div className="container mt-4">
            <h2>Gestione Utenti</h2>
            <table className="table table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Ruolo</th>
                        <th>Azioni</th>
                    </tr>
                </thead>
                <tbody>
                    {users.length > 0 ? (
                        users.map((user) => (
                            <tr key={user.id}>
                                <td>{user.id}</td>
                                <td>{user.full_name}</td>
                                <td>{user.username}</td>
                                <td>{user.role}</td>
                                <td>
                                    <button className="btn btn-sm btn-danger" onClick={() => handleDelete(user.id)}>
                                        Elimina
                                    </button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="5" className="text-center">Nessun utente trovato</td>
                        </tr>
                    )}
                </tbody>
            </table>

            {/* Bottone per aprire la modale */}
            <button className="btn btn-success mt-3" data-bs-toggle="modal" data-bs-target="#createUserModal">
                <i className="bi bi-person-add me-2"></i>
                Aggiungi Utente
            </button>

            {/* Modale Bootstrap per Creazione Utente */}
            <div className="modal fade" id="createUserModal" tabIndex="-1" aria-labelledby="createUserModalLabel" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title" id="createUserModalLabel">Crea Nuovo Utente</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            <form>
                                <div className="mb-3">
                                    <label className="form-label">Nome Completo</label>
                                    <input type="text" className="form-control" value={newUser.full_name}
                                        onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })} required />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Email (Username)</label>
                                    <input type="email" className="form-control" value={newUser.username}
                                        onChange={(e) => setNewUser({ ...newUser, username: e.target.value })} required />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input type="password" className="form-control" value={newUser.pwd}
                                        onChange={(e) => setNewUser({ ...newUser, pwd: e.target.value })} required />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Ruolo</label>
                                    <select className="form-select" value={newUser.role}
                                        onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}>
                                        <option value="USER">USER</option>
                                        <option value="ADMIN">ADMIN</option>
                                    </select>
                                </div>
                            </form>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Chiudi</button>
                            <button type="button" className="btn btn-primary" onClick={handleCreateUser} disabled={isCreating}>
                                {isCreating ? "Creando..." : "Crea Utente"}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Admin;
