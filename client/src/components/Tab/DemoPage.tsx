import React, { useEffect, useRef, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import Graphic from './Graph';  

interface FrameData {
  TimeStamp: number;
  velocidad_instantanea_suavizada: number;
  aceleracion_instantanea_suavizada: number;
}

const DemoPage: React.FC = () => {
  const location = useLocation();
  const { videoURL, dataURL } = location.state as { videoURL: string; dataURL: string };

  const videoRef = useRef<HTMLVideoElement>(null);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [velocitySData, setVelocitySData] = useState<{ tiempo: number[]; velocitySuavizedData: number[] }>({ tiempo: [], velocitySuavizedData: [] });
  const [acelerationSData, setAcelerationSData] = useState<{ tiempo: number[]; aceleracionSuavizedInstantanea: number[] }>({ tiempo: [], aceleracionSuavizedInstantanea: [] });

  useEffect(() => {
    if (videoRef.current) {
      const handleTimeUpdate = () => setCurrentTime(videoRef.current!.currentTime);
      videoRef.current.addEventListener('timeupdate', handleTimeUpdate);
      
      // Reproducir el video automáticamente
      videoRef.current.play();
      
      return () => videoRef.current?.removeEventListener('timeupdate', handleTimeUpdate);
    }
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(dataURL);
        const jsonData: FrameData[] = await response.json();

        const tiempo = jsonData.map(frame => frame.TimeStamp);
        const velocitySuavizedData = jsonData.map(frame => frame.velocidad_instantanea_suavizada);
        const aceleracionSuavizedInstantanea = jsonData.map(frame => frame.aceleracion_instantanea_suavizada);

        setVelocitySData({ tiempo, velocitySuavizedData });
        setAcelerationSData({ tiempo, aceleracionSuavizedInstantanea });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [dataURL]);

  return (
    <div className="m-5 grid grid-cols-2 gap-4">
      <div>
        <video ref={videoRef} src={videoURL} controls className="w-full h-full" />
      </div>
      <div>
        <div className="grid grid-rows-2 gap-2">
          <Graphic 
            title="Velocidad Instantanea SUAVIZADA en funcion del tiempo" 
            type="scatter"
            xAxisName="Tiempo (segs)" 
            yAxisName="Velocidad SUAVIZADA (mts/segs)"
            x={velocitySData.tiempo} 
            y={velocitySData.velocitySuavizedData} 
            currentTime={currentTime}
          />
          <Graphic 
            title="Aceleracion SUAVIZADA en funcion del tiempo" 
            type="scatter"
            xAxisName="Tiempo (segs)" 
            yAxisName="Aceleracion SUAVIZADA (mts/segs^2)"
            x={acelerationSData.tiempo} 
            y={acelerationSData.aceleracionSuavizedInstantanea} 
            currentTime={currentTime}
          />
        </div>
        <div className="mt-4">
          <Link to="/">
            <button className="px-4 py-2 bg-blue-500 text-white font-bold rounded hover:bg-blue-700">
              Volver al menú
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default DemoPage;
