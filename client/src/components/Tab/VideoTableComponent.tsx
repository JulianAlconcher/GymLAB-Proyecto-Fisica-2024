/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useRef, useState } from 'react';
import VideoComponent from './VideoComponent';
import GraficosComponent from './GraphTableComponent'; // Importar correctamente

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

  return (
    <div className="m-5 grid grid-cols-2">
      <div><VideoComponent videoRef={videoRef} /></div>
      <div><GraficosComponent currentTime={currentTime} /></div>
    </div>
  );
}

export default VideoTableComponent;