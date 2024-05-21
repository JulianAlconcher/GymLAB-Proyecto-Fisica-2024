import { useState, useEffect } from 'react';
import CircularProgress from '@mui/material/CircularProgress';

export const Loading = () => {
  const frasesMotivacionales = [
    "Calentando los músculos...",
    "Pasando de cartesianas a polares...",
    "Cargando la barra...",
    "Derivando la velocidad, derivando la posicion...",
  ];

  const [indiceFrase, setIndiceFrase] = useState(0);

  useEffect(() => {
    const intervalo = setInterval(() => {
      setIndiceFrase(prevIndice => (prevIndice + 1) % frasesMotivacionales.length);
    }, 5000);

    return () => clearInterval(intervalo);
  }, [frasesMotivacionales.length]);

  return (
    <div className='bg-white flex h-screen justify-center items-center flex-col'>
      <CircularProgress />
      <div className='text-3xl font-bold text-black mt-4'>{frasesMotivacionales[indiceFrase]}</div>
    </div>
  )
}

export default Loading;
