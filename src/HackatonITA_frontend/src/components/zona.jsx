import React, { useState, useEffect } from 'react';
import { HackatonITA_backend } from "../../../declarations/HackatonITA_backend";

const Zonas = () => {
  const [zonas, setZonas] = useState([]);
  const [crimenes, setCrimenes] = useState([]);
  const [selectedZona, setSelectedZona] = useState('');

  useEffect(() => {
    const fetchZonas = async () => {
      try {
        // Llamada para obtener todas las zonas (únicas)
        const allZonas = await HackatonITA_backend.getAllZonas();
        setZonas([...new Set(allZonas)]); // Elimina duplicados de zonas
      } catch (err) {
        console.error("Error al obtener las zonas:", err);
      }
    };
    fetchZonas();
  }, []);

  const handleZonaChange = async (e) => {
    const zona = e.target.value;
    setSelectedZona(zona);

    try {
      // Llamada para obtener crímenes de la zona seleccionada
      const result = await HackatonITA_backend.getCrimenesByZona(zona);
      setCrimenes(result);
    } catch (err) {
      console.error("Error al obtener crímenes:", err);
    }
  };

  return (
    <div className="page-container">
      <h1 className ="page-heading">Buscar Crímenes por Zona</h1>
      <label className="page-description">Selecciona una Zona:</label>
      <select onChange={handleZonaChange}>
        <option value="">Seleccione</option>
        {zonas.map((zona, index) => (
          <option key={index} value={zona}>
            {zona}
          </option>
        ))}
      </select>

      <div>
        <h2 className="info-box">Crímenes en {selectedZona}:</h2>
        <ul>
          {crimenes.map((crimen, index) => (
            <li key={index}>{crimen}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Zonas;
