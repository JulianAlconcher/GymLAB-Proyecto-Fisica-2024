import { useState, useEffect } from 'react';

import fileService from "../../service/FileService";
import Graphic from './Graph';

interface GraficosComponent {
  setShowGraph: React.Dispatch<React.SetStateAction<boolean>>;
}

function GraficosComponent(): JSX.Element {
  const [velocityData, setVelocityData] = useState<{ tiempo: number[]; velocidadInstantanea: number[] }>({ tiempo: [], velocidadInstantanea: [] });
  const [acelerationData, setAcelerationData] = useState<{ tiempo: number[]; aceleracionInstantanea: number[] }>({ tiempo: [], aceleracionInstantanea: [] });

  useEffect(() => {
      fetchData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[]);

  const fetchData = async () => {
    try {
      const responseData = await getFileFromServer();
      const jsonData = await responseData.json();

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const tiempo = jsonData.map((frame: any) => frame.TimeStamp);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const velocidadInstantanea = jsonData.map((frame: any) => frame.velocidad_instantanea);

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const aceleracionInstantanea = jsonData.map((frame: any) => frame.aceleracion_instantanea);

      setVelocityData({ tiempo, velocidadInstantanea });

      setAcelerationData({ tiempo, aceleracionInstantanea });

      /*
        Hacer lo mismo para los graficos de posicion y aceleracion, 
        para pasarle los datos al componente Graphic.
      */
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
          title='Velocidad Instantanea en funcion del tiempo' 
          type='scatter'
          xAxisName='Tiempo (segs)' 
          yAxisName='Velocidad (mts/segs)'
          x={velocityData.tiempo} 
          y={velocityData.velocidadInstantanea} 
        />
        {
          /*
        <Graphic 
          title='Posicion en funcion del tiempo' 
          type='scatter'
          xAxisName='Tiempo (segs)' 
          yAxisName= 
          x={} 
          y={} 
        />
        */
        <Graphic 
          title='Aceleracion en funcion del tiempo' 
          type='scatter'
          xAxisName='Tiempo (segs)' 
          yAxisName= 'Aceleracion (mts/segs^2)'
          x={acelerationData.tiempo} 
          y={acelerationData.aceleracionInstantanea}
          
          
        />
        } 
      </div>
    </>
  );
}

export default GraficosComponent;
