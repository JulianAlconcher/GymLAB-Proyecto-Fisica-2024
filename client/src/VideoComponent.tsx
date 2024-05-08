import { ChangeEvent, FormEvent, useRef, useState } from 'react';

function VideoComponent(): JSX.Element {
  const [exercise, setExercise] = useState<string>("Curl de Biceps");
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [weight, setWeight] = useState<string>("20");
  const [videoURL, setVideoURL] = useState<string | null>(null); // Estado para almacenar la URL del video
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleExerciseChange = (event: ChangeEvent<HTMLSelectElement>) => {
    setExercise(event.target.value);
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setVideoFile(event.target.files[0]);
    }
  };

  const handleWeightChange = (event: ChangeEvent<HTMLInputElement>) => {
    setWeight(event.target.value);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!exercise || !videoFile || !weight) {
      alert('Por favor, complete todos los campos.');
      return;
    }

    const formData = new FormData();
    formData.append('exercise', exercise);
    formData.append('video', videoFile);
    formData.append('weight', weight);

    requestProcessing(formData);
  }

  const requestProcessing = async (formData: FormData) => {
    try {
      const response = await fetch('http://localhost:8080/upload', { method: 'POST', body: formData });
      if (response.ok) {
        getFileFromServer(response);
      } else {
        console.error('Failed to upload data');
      }
    } catch (error) {
      console.error('Error uploading data:', error);
    }
  };

  const getFileFromServer = async (response: Response) => {
    const infoString = await response.text();
    console.log('JSON Data:', infoString);
    const fileResponse = await fetch('http://localhost:8080/getFile', { method: 'GET' });
    if (fileResponse.ok) {
      const json = await fileResponse.json();
      console.log(json);
      getVideoFromServer(); // Llamar a la función para obtener el video después de recibir el archivo
      setVideoURL("prueba")
    } else {
      console.error('Failed to get file from server');
    }
  };

  const getVideoFromServer = async () => {
    try {
        const videoResponse = await fetch("http://localhost:8080/getVideo", { 
            method: 'GET',
            headers: {
                'Range': 'bytes=0-' // Solicitar todo el archivo
            },
            cache: 'no-store' // Deshabilitar el almacenamiento en caché de la respuesta
        });

        if (videoResponse.ok) {
            const blob = await videoResponse.blob(); // Obtener el contenido del video como un Blob
            const videoURL = URL.createObjectURL(blob); // Crear una URL para el Blob
            if (videoRef.current) {
            videoRef.current.src = videoURL; // Establecer la URL como origen del video
            videoRef.current.load(); // Cargar el video
            videoRef.current.play();
            setVideoURL(videoURL); 
            }// Establecer la URL del video en el estado
        } else {
            console.error('Failed to get video from server');
        }
    } catch (error) {
        console.error('Error fetching video:', error);
    }
};

  return (
    <>
      <div className="m-5 bg-slate-500 h-full">
        <form onSubmit={handleSubmit}>
          <div className="sm:col-span-3">
            <div className="m-2"> Ejercicio:
              <select className="m-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6" value={exercise} onChange={handleExerciseChange}>
                <option value="Curl de Biceps">Curl de Biceps</option>
                <option value="Sentadilla">Sentadilla</option>
                <option value="Press banco plano">Press banco plano</option>
                <option value="Press banco inclinado">Press banco inclinado</option>
              </select>
            </div>
          </div>
          <div className="m-2"> Video:
            <label className="relative cursor-pointer m-2 rounded-md p-2 bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500">
              <span>Cargar video</span>
              <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileChange} />
            </label>
            <span>{videoFile ? videoFile.name : null}</span>
          </div>
          <div className="sm:col-span-4">
            <label className="m-2">Peso: </label>
            <input className="border-2 bg-transparent m-2 focus:ring-0 sm:text-sm sm:leading-6" value={weight} onChange={handleWeightChange} />
          </div>
          <button type="submit" className="rounded-md m-2 bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Enviar</button>
        </form>
        {videoURL && (
          <video className="m-2" ref={videoRef}controls autoPlay>
            {/* <source src="http://localhost:8080/getVideo" />
            Your browser does not support the video tag. */}
          </video>
        )}
      </div>
    </>
  )
}

export default VideoComponent;
