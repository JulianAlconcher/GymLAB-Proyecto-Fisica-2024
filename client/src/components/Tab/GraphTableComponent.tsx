import { useState, useEffect } from 'react';

import fileService from "../../service/FileService";
import Graphic from './Graph';

interface GraficosComponent {
  setShowGraph: React.Dispatch<React.SetStateAction<boolean>>;
}

function GraficosComponent(): JSX.Element {
  const [velocitySData, setVelocitySData] = useState<{ tiempo: number[]; velocitySuavizedData: number[] }>({ tiempo: [], velocitySuavizedData: [] });
  const [acelerationSData, setAcelerationSData] = useState<{ tiempo: number[]; aceleracionSuavizedInstantanea: number[] }>({ tiempo: [], aceleracionSuavizedInstantanea: [] });
  
  useEffect(() => {
      fetchData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[]);

  const fetchData = async () => {
    try {
      const responseData = await getFileFromServer();
      const jsonData = await responseData.json();

      console.log(jsonData);

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const tiempo = jsonData.map((frame: any) => frame.TimeStamp);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const velocitySuavizedData = jsonData.map((frame: any) => frame.velocidad_instantanea_suavizada);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const aceleracionSuavizedInstantanea = jsonData.map((frame: any) => frame.aceleracion_instantanea_suavizada);

      setVelocitySData({ tiempo, velocitySuavizedData });
      setAcelerationSData({ tiempo, aceleracionSuavizedInstantanea });

    } catch (error) {
      console.error('Error fetching velocity data:', error);
    }
  };

  const getFileFromServer = async (): Promise<Response> => {
    try {
      return await fileService.getFileFromServer();
    } catch (error) {
      console.error('Error getting file from server:', error);
      throw error;
    }
  };

  return (
    <>
      <div className="m-5  p-4 grid grid-rows-3 grid-cols-1 gap-1 h-full">
         <Graphic 
          title='Velocidad Instantanea SUAVIZADA en funcion del tiempo' 
          type='scatter'
          xAxisName='Tiempo (segs)' 
          yAxisName='Velocidad SUAVIZADA (mts/segs)'
          x={velocitySData.tiempo} 
          y={velocitySData.velocitySuavizedData} 
        />
        <Graphic 
          title='Aceleracion SUAVIZADA en funcion del tiempo' 
          type='scatter'
          xAxisName='Tiempo (segs)' 
          yAxisName= 'Aceleracion SUAVIZADA (mts/segs^2)'
          x={acelerationSData.tiempo} 
          y={acelerationSData.aceleracionSuavizedInstantanea}          
        />
        
      </div>
    </>
  );
}

export default GraficosComponent;
