import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Zona from './components/zona';
import Crimen from './components/crimen.jsx';
import Emergencia from './components/emergencia.jsx';
import { AuthClient } from "@dfinity/auth-client";
import './styles.css'; // Asegúrate de agregar los estilos nuevos aquí

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authClient, setAuthClient] = useState(null);

  useEffect(() => {
    const initAuth = async () => {
      const client = await AuthClient.create();
      setAuthClient(client);
      const isAuthenticated = await client.isAuthenticated();
      setIsAuthenticated(isAuthenticated);
    };
    initAuth();
  }, []);

  const handleLogin = async () => {
    if (authClient) {
      await authClient.login({
        identityProvider: "https://identity.ic0.app/#authorize",
        onSuccess: () => {
          setIsAuthenticated(true);
        },
      });
    }
  };

  const handleLogout = async () => {
    if (authClient) {
      await authClient.logout();
      setIsAuthenticated(false);
    }
  };

  return (
    <Router>
      <header className="header">
        <div className="header-content">
          <Link to="/" className="header-logo">TechTitans</Link>
          {isAuthenticated ? (
            <nav className="nav-bar">
              <Link to="/zona" className="menu-button">Zona</Link>
              <Link to="/crimen" className="menu-button">Crimen</Link>
              <Link to="/emergencia" className="menu-button">Reportar</Link>
            </nav>
          ) : null}
          {isAuthenticated ? (
            <div className="container">
              <button className="login-button" onClick={handleLogout}>
                Cerrar Sesión
              </button>
            </div>
          ) : (
            <div className="container">
              <button className="login-button" onClick={handleLogin}>
                Iniciar Sesión
              </button>
            </div>
          )}
        </div>
      </header>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/zona" element={<Zona />} />
          <Route path="/crimen" element={<Crimen />} />
          <Route path="/emergencia" element={<Emergencia />} />
        </Routes>
      </main>
    </Router>
  );
}

function Home() {
  return (
    <div className="home-page">
      <h2 className="main-heading">Bienvenido a DroneGuard</h2>
      <p className="main-text">Transportate seguro.</p>
    </div>
  );
}

export default App;
