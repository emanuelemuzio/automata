import { Link } from "react-router-dom";

function Home() {
  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Benvenuto in Automata</h1>
      <p>Unisciti a noi per sfruttare l'AI e l'automazione!</p>
      <Link to="/login">
        <button style={{ fontSize: "16px" }}>Accedi</button>
      </Link>
    </div>
  );
}

export default Home;
