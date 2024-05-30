/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect } from 'react';
import fileService from "../../service/FileService";
import Graphic from './Graph';

interface GraficosComponentProps {
  currentTime: number;
}

function GraficosComponent({ currentTime }: GraficosComponentProps): JSX.Element {
  const [velocitySData, setVelocitySData] = useState<{ tiempo: number[]; velocitySuavizedData: number[] }>({ tiempo: [], velocitySuavizedData: [] });
  const [acelerationSData, setAcelerationSData] = useState<{ tiempo: number[]; aceleracionSuavizedInstantanea: number[] }>({ tiempo: [], aceleracionSuavizedInstantanea: [] });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const responseData = await fileService.getFileFromServer();
        const jsonData = await responseData.json();

        const tiempo = jsonData.map((frame: any) => frame.TimeStamp);
        const velocitySuavizedData = jsonData.map((frame: any) => frame.velocidad_instantanea_suavizada);
        const aceleracionSuavizedInstantanea = jsonData.map((frame: any) => frame.aceleracion_instantanea_suavizada);

        setVelocitySData({ tiempo, velocitySuavizedData });
        setAcelerationSData({ tiempo, aceleracionSuavizedInstantanea });

      } catch (error) {
        console.error('Error fetching velocity data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="m-5 p-4 grid grid-rows-2 grid-cols-1 gap-1 h-full w-full">
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
  );
}

export default GraficosComponent;