import React, { useState } from 'react';
import { HackatonITA_backend } from "../../../declarations/HackatonITA_backend";

const Emergencia = () => {
  const [zona, setZona] = useState('');
  const [crimen, setCrimen] = useState('');

  const handleSet = async () => {
    try {
      await HackatonITA_backend.set(zona, crimen);
      alert(`Datos guardados: Zona: ${zona}, Crimen: ${crimen}`);
    } catch (err) {
      console.error("Error al guardar los datos:", err);
    }
  };

  return (
    <div className="page-container">
      <h1 className ="page-heading">Agregar Zona y Crimen</h1>
      <div>
        <label>Zona:</label>
        <input type="text" value={zona} onChange={(e) => setZona(e.target.value)} />
      </div>
      <div>
        <label>Crimen:</label>
        <input type="text" value={crimen} onChange={(e) => setCrimen(e.target.value)} />
      </div>
      <button className="menu-button" onClick={handleSet}>Guardar</button>
    </div>
  );
};

export default Emergencia;
