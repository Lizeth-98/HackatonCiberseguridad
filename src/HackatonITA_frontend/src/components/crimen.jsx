import React, { useState, useEffect } from 'react';
import { HackatonITA_backend } from "../../../declarations/HackatonITA_backend";

const Crimenes = () => {
  const [crimenes, setCrimenes] = useState([]);
  const [zonas, setZonas] = useState([]);
  const [selectedCrimen, setSelectedCrimen] = useState('');

  useEffect(() => {
    const fetchCrimenes = async () => {
      try {
        // Llamada para obtener todos los crímenes (únicos)
        const allCrimenes = await HackatonITA_backend.getAllCrimenes();
        console.log(allCrimenes)
        setCrimenes([...new Set(allCrimenes)]); // Elimina duplicados de crímenes
      } catch (err) {
        console.error("Error al obtener los crímenes:", err);
      }
    };
    fetchCrimenes();
  }, []);

  const handleCrimenChange = async (e) => {
    const crimen = e.target.value;
    setSelectedCrimen(crimen);

    try {
      // Llamada para obtener zonas donde ocurrió el crimen seleccionado
      const result = await HackatonITA_backend.getZonasByCrimen(crimen);
      setZonas(result);
    } catch (err) {
      console.error("Error al obtener zonas:", err);
    }
  };

  return (
    <div className="page-container">
      <h1 className ="page-heading">Buscar Zonas por Crimen</h1>
      <label className="page-description">Selecciona un Crimen:</label>
      <select onChange={handleCrimenChange}>
        <option value="">Seleccione</option>
        {crimenes.map((crimen, index) => (
          <option key={index} value={crimen}>
            {crimen}
          </option>
        ))}
      </select>

      <div>
        <h2 className="info-box">Zonas donde ocurrió {selectedCrimen}:</h2>
        <ul>
          {zonas.map((zona, index) => (
            <li key={index}>{zona}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Crimenes;
