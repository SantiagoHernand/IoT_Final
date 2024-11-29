import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Adc from './adc.tsx';
import Ultrasonico from './ultrasonico.tsx';
import Bmp from './bmp.tsx';
import Acelerometro from './acelerometro.tsx';
import GraficaSensorDistancia from './App.tsx';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
   <React.StrictMode>
    <Acelerometro/>
    <Bmp/>
    <Ultrasonico/>
    <Adc/>
    <GraficaSensorDistancia/>
  </React.StrictMode>
);
