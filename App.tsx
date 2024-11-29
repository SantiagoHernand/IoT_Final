import React, { useEffect, useState } from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
} from "recharts";

interface Ultrasonico {
    fecha: string;
    id: number;
    valor_distancia_cm: number;
}

function GraficaSensorDistancia() {
    const [data, setData] = useState<Ultrasonico[]>([]);

    async function fetchData() {
        console.log("Usando dummy data...");
        try {
            // Dummy data para pruebas
            const dummyData = [
                { valor_distancia_cm: 30.0, fecha: "2003-11-05", id: 6 },
                { valor_distancia_cm: 25.5, fecha: "2003-11-06", id: 7 },
                { valor_distancia_cm: 20.2, fecha: "2003-11-07", id: 8 },
                { valor_distancia_cm: 35.8, fecha: "2003-11-08", id: 9 },
            ];
            setData(dummyData); // Establece los datos ficticios
            console.log("Datos ficticios establecidos:", dummyData);
        } catch (error) {
            console.error("Error al establecer datos ficticios:", error);
        }
    }

    useEffect(() => {
        fetchData(); // Llama a la función para establecer los datos
    }, []);

    return (
        <div>
            <LineChart
                width={1}
                height={1}
                data={data}
                margin={{ top: 10, right: 30, left: 20, bottom: 10 }}
            >
                <XAxis dataKey="fecha" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="valor_distancia_cm" stroke="#8884d8" />
            </LineChart>
        </div>
    );
}

export default GraficaSensorDistancia;