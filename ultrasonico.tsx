'use client';
import React, { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts"; // Importación de componentes de recharts

interface ultrasonico{
  id: number;
  distancia_valor: number;
  fecha: string;
}

function Ultrasonico() {
  const [data, setData] = useState<ultrasonico[]>([]);

  async function fetchData() {
    console.log("FechData");
    try {
      const response = await axios.get("http://localhost:8000/ultrasonico");
      console.log("API Response: ", response.data);
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Failed to fetch data. Please check the API or your connection.");
    }
  }

  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      if (document.visibilityState === "visible") {
        fetchData();
      }
    }, 5000); // Fetch every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (

      <div className="ultrasonico">
          <h1>Ultrasonico</h1>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={data.slice(-15)}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <XAxis dataKey="fecha" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="distancia_valor" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Ultrasonico;