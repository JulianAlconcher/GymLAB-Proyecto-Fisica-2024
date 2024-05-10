import { ChangeEvent, FormEvent, useEffect, useRef, useState } from 'react';
import fileService from "../../service/FileService"
import VideoComponent from './VideoComponent';
import ExerciseOptions from './ExerciseOptions';
import { ExerciseOption } from '../../enums/enumsExercise';

function VideoTableComponent(): JSX.Element {
  const [exercise, setExercise] = useState<ExerciseOption | null>(ExerciseOption.Bicep);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [weight, setWeight] = useState<string>("20");
  const [videoURL, setVideoURL] = useState<string | null>(null); // Estado para almacenar la URL del video
  const videoRef = useRef<HTMLVideoElement>(null);


  useEffect(() => {
    // Verificar si el componente de video se ha montado
    if (videoRef.current) {
      // Acciones a realizar una vez que el componente se ha montado, como configurar el videoURL o reproducir el video
      if (videoURL) {
        videoRef.current.src = videoURL;
        videoRef.current.load();
        videoRef.current.play();
      }
    }
  }, [videoURL]);

  
  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
        // Verificar si todos los campos están completos
        console.log(exercise);
        console.log(videoFile);
        console.log(weight);
        if (!exercise || !videoFile || !weight) {
            alert('Por favor, complete todos los campos.');
            return;
        }

        // Crear el objeto FormData
        const formData = new FormData();
        formData.append('exercise', exercise);
        formData.append('video', videoFile);
        formData.append('weight', weight);

        // Subir el archivo al servidor
        await uploadFile(formData);

        // Obtener la respuesta del servidor y convertirla a JSON
        const responseData = await getFileFromServer();
        const jsonData = await responseData.json();
        console.log(jsonData);

        // Obtener el video del servidor y manejar la respuesta
       await getVideoFromServerAndHandleResponse();
        
    } catch (error) {
        console.error('Error handling submit:', error);
        alert('Ocurrió un error al procesar el formulario. Por favor, inténtelo de nuevo.');
    }
};

// Función para subir el archivo al servidor
const uploadFile = async (formData: FormData): Promise<void> => {
    try {
        await fileService.uploadFile(formData);
    } catch (error) {
        console.error('Error uploading file:', error);
        throw error;
    }
};

// Función para obtener el archivo del servidor
const getFileFromServer = async (): Promise<Response> => {
    try {
        return await fileService.getFileFromServer();
    } catch (error) {
        console.error('Error getting file from server:', error);
        throw error;
    }
};

// Función para obtener el video del servidor y manejar la respuesta (Lo podria separar en dos pero fue)
const getVideoFromServerAndHandleResponse = async () => {
    try {
        const responseGetVideo = await fileService.getVideoFromServer(videoFile?.name as string);
        handleVideoResponse(responseGetVideo, setVideoURL);
        
    } catch (error) {
        console.error('Error fetching video:', error);
        throw error;
    }
};

  const handleVideoResponse = async (response: Response, setVideoURL: React.Dispatch<React.SetStateAction<string | null>>): Promise<void> => {
    if (response.ok) {
      const blob = await response.blob();
      const videoURL = URL.createObjectURL(blob);
      setVideoURL(videoURL);
    } else {
      console.error('Failed to get video from server');
    }
};


  return (
    <>
      <div className="m-5 bg-slate-500 h-full">
        <form onSubmit={handleSubmit}>
          <div className="sm:col-span-3">
            <div className="m-2"> Ejercicio:
             <ExerciseOptions value={exercise || null} onChange={setExercise}/>
            </div>
          </div>
          <div className="m-2"> Video:
            <label className="relative cursor-pointer m-2 rounded-md p-2 bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500">
              <span>Cargar video</span>
              <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={(event: ChangeEvent<HTMLInputElement>) => {
                if (event.target.files) {
                  setVideoFile(event.target.files[0]);
                }
              }} />
            </label>
            <span>{videoFile ? videoFile.name : null}</span>
          </div>
          <div className="sm:col-span-4">
            <label className="m-2">Peso: </label>
            <input className="border-2 bg-transparent m-2 focus:ring-0 sm:text-sm sm:leading-6" value={weight} onChange={(event: ChangeEvent<HTMLInputElement>) => setWeight(event.target.value)} />
          </div>
          <button type="submit" className="rounded-md m-2 bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Enviar</button>
        </form>
        {videoURL && (
         <VideoComponent videoRef={videoRef} />
        )}
      </div>
    </>
  )
}

export default VideoTableComponent;
