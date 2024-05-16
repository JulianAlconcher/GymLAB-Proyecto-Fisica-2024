import React, { useState, FormEvent, ChangeEvent } from 'react';
import fileService from "../../service/FileService";
import ExerciseOptions from './ExerciseOptions';
import { ExerciseOption } from '../../enums/enumsExercise';

interface FormComponentProps {
  onSubmitSuccess: () => void;
  setVideoURL: React.Dispatch<React.SetStateAction<string | null>>;
}

function FormComponent({ onSubmitSuccess, setVideoURL }: FormComponentProps): JSX.Element {
  const [exercise, setExercise] = useState<ExerciseOption | null>(ExerciseOption.Bicep);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [weight, setWeight] = useState<string>("20");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      if (!exercise || !videoFile || !weight) {
        alert('Por favor, complete todos los campos.');
        return;
      }

      const formData = new FormData();
      formData.append('exercise', exercise);
      formData.append('video', videoFile);
      formData.append('weight', weight);

      await uploadFile(formData);
      const responseData = await getFileFromServer();
      const jsonData = await responseData.json();
      console.log(jsonData);

      await getVideoFromServerAndHandleResponse();

      onSubmitSuccess();
    } catch (error) {
      console.error('Error handling submit:', error);
      alert('Ocurrió un error al procesar el formulario. Por favor, inténtelo de nuevo.');
    }
  };

  const uploadFile = async (formData: FormData): Promise<void> => {
    try {
      await fileService.uploadFile(formData);
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
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
    <form onSubmit={handleSubmit}>
      <div className="sm:col-span-3">
        <div className="m-2"> Ejercicio:
          <ExerciseOptions value={exercise || null} onChange={setExercise} />
        </div>
      </div>
      <div className="m-2"> Video:
        <label className="rounded-md m-2 bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
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
        <input className="border-2 bg-white rounded-md m-2 focus:ring-0 sm:text-sm sm:leading-6" value={weight} onChange={(event: ChangeEvent<HTMLInputElement>) => setWeight(event.target.value)} />
      </div>
      <button type="submit" className="rounded-md m-2 bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Enviar</button>
    </form>
  );
}

export default FormComponent;
