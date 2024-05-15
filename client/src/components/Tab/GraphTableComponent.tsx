import { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import fileService from "../../service/FileService";

function GraficosComponent(): JSX.Element {
  const [velocityData, setVelocityData] = useState<{ tiempo: number[]; velocidadInstantanea: number[] }>({ tiempo: [], velocidadInstantanea: [] });

  useEffect(() => {
      fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const responseData = await getFileFromServer();
      const jsonData = await responseData.json();

      const tiempo = jsonData.map((frame: any) => frame.TimeStamp);
      const velocidadInstantanea = jsonData.map((frame: any) => frame.velocidad_instantanea);

      setVelocityData({ tiempo, velocidadInstantanea });
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
      <div className="m-5 bg-gray-200 border-2 border-black rounded-lg p-2 h-full">
        <h1 className="text-3xl m-2">Gráfico de Velocidad Instantánea</h1>
        {velocityData && (
          <div>
            <Plot
              data={[
                {
                  type: 'scatter',
                  x: velocityData.tiempo,
                  y: velocityData.velocidadInstantanea,
                  mode: 'lines',
                  marker: { color: 'blue' },
                  name: 'Velocidad Instantánea'
                }
              ]}
              layout={{ title: 'Gráfico de Velocidad Instantánea en función del Tiempo' }}
              style={{ width: '100%', height: '400px' }}
            />
          </div>
        )}
      </div>
    </>
  );
}

export default GraficosComponent;
