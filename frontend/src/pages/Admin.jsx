import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/authService";
import "../styles/Admin.css";
import useAuth from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

function Admin() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [editingUser, setEditingUser] = useState(null);
    const [editedData, setEditedData] = useState({ "pwd": null });
    const navigate = useNavigate();
    const { userRole } = useAuth();

    const handleEdit = (user) => {
        setEditingUser(user.id);
        setEditedData(user);
    };

    const handleChange = (e) => {
        setEditedData({ ...editedData, [e.target.name]: e.target.value });
    };

    const handleSave = async () => {
        try {

            await fetchWithAuth(`/user?idx=${editedData.id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(editedData),
            });

            fetchUsers();
            setEditingUser(null);

        } catch (error) {
            alert(error.message)
        }
    };

    const [newUser, setNewUser] = useState({ id: null, full_name: "", username: "", pwd: "", role: "USER" });
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
            const data = await fetchWithAuth("/user/all");
            
            setUsers(data);

        } catch (error) {
            alert(error.message)
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async (userId) => {
        try {
            await fetchWithAuth(`/user/toggle?idx=${userId}`, {
                method: "GET"
            }); 
            
            fetchUsers();

        } catch (error) {
            console.error("Errore nel toggle dello stato utente", error);
        }
    };

    const handleDelete = async (userId) => {
        if (!window.confirm("Sei sicuro di voler eliminare questo utente?")) return;

        try {
            await fetchWithAuth(`/user?idx=${userId}`, {
                method: "DELETE",
            });

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
                role: newUser.role,
                id: null,
                disabled: false
            };

            const createdUser = await fetchWithAuth("/user", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestBody),
            });

            setUsers([...users, createdUser]);
            setNewUser({ id: null, full_name: "", username: "", pwd: "", role: "USER" });
            alert("Utente creato con successo!");

        } catch (error) {
            alert(error.message);
        } finally {
            setIsCreating(false);
        }
    };

    if (loading) return <p>Caricamento utenti...</p>;

    return (
        <div className="container">
            <h2>Gestione Utenti</h2>
            <table className="table table-hover">
                <thead>
                    <tr className="text-center">
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Ruolo</th>
                        <th>Azioni</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user) => (
                        <tr key={user.id} className="text-center">
                            <td>{user.id}</td>
                            <td>
                                {editingUser === user.id ? (
                                    <input
                                        type="text"
                                        name="full_name"
                                        className="form-control"
                                        value={editedData.full_name || ""}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    user.full_name
                                )}
                            </td>
                            <td>
                                {editingUser === user.id ? (
                                    <input
                                        type="email"
                                        name="username"
                                        className="form-control"
                                        value={editedData.username || ""}
                                        onChange={handleChange}
                                    />
                                ) : (
                                    user.username
                                )}
                            </td>
                            <td>
                                {editingUser === user.id ? (
                                    <select
                                        name="role"
                                        className="form-select"
                                        value={editedData.role || "USER"}
                                        onChange={handleChange}>
                                        <option value="USER">USER</option>
                                        <option value="ADMIN">ADMIN</option>
                                    </select>
                                ) : (
                                    user.role
                                )}
                            </td>
                            {editingUser === user.id ? (
                                <td>
                                    <button className="btn btn-success" onClick={handleSave}>
                                        <i className="bi bi-check-circle"></i>
                                    </button>
                                </td>
                            ) : (
                                <td>
                                    <button className="btn btn-primary me-2" title="Modifica" onClick={() => handleEdit(user)}>
                                        <i className="bi bi-pencil-square"></i>
                                    </button>
                                    <button className="btn btn-danger me-2" title="Elimina" onClick={() => handleDelete(user.id)}>
                                        <i className="bi bi-trash"></i>
                                    </button>
                                    <button
                                        className={`btn ${user.disabled ? "btn-success" : "btn-warning"}`}
                                        onClick={() => handleToggle(user.id)}>

                                        {
                                            user.disabled
                                                ?
                                                <i title="Abilita" className="bi bi-unlock-fill"></i>
                                                :
                                                <i title="Disabilita" className="bi bi-lock-fill"></i>
                                        }
                                    </button>
                                </td>
                            )}
                        </tr>
                    ))}
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
        </div >
    );
}

export default Admin;
