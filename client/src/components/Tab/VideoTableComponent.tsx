/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useRef, useState } from 'react';
import VideoComponent from './VideoComponent';
import GraficosComponent from './GraphTableComponent'; // Importar correctamente
import { Link } from 'react-router-dom';
import FileService from '../../service/FileService';

interface VideoTableComponentProps {
  videoURL: string;
}

function VideoTableComponent({ videoURL }: VideoTableComponentProps): JSX.Element {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [currentTime, setCurrentTime] = useState<number>(0);

  useEffect(() => {
    const handleTimeUpdate = () => {
      if (videoRef.current) {
        setCurrentTime(videoRef.current.currentTime);
      }
    };

    if (videoRef.current) {
      videoRef.current.addEventListener('timeupdate', handleTimeUpdate);
    }

    return () => {
      if (videoRef.current) {
        videoRef.current.removeEventListener('timeupdate', handleTimeUpdate);
      }
    };
  }, []);

  useEffect(() => {
    if (videoRef.current) {
      if (videoURL) {
        videoRef.current.src = videoURL;
        videoRef.current.load();
        videoRef.current.play();
      }
    }
  }, [videoURL]);

  const handleClick = async () => {
    try {
        const response = await FileService.getPDFFromServer();
        const pdfBlob = await response.blob();
        const url = URL.createObjectURL(pdfBlob);
        window.open(url);
    } catch (error) {
        console.error('Error in handleClick:', error);
    }
};

  return (
    <div className="m-5 grid grid-cols-2">
      <div><VideoComponent videoRef={videoRef} /></div>
      <div><GraficosComponent currentTime={currentTime} /></div>
      <div className="mt-4 mb-4 grid grid-cols-2 gap-2">
          <Link to="/">
            <button className="px-4 py-2 w-full bg-blue-500 text-white font-bold rounded hover:bg-blue-700">
              Volver al menú
            </button>
            
          </Link>

            <button onClick={handleClick} className="px-4 py-2 w-full bg-red-600 text-white font-bold rounded hover:bg-blue-700">
              DESCARGAR PDF
            </button>
        </div>
    </div>
  );
}

export default VideoTableComponent;