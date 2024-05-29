import { useEffect, useRef } from 'react';
import VideoComponent from './VideoComponent';


interface VideoTableComponentProps {
  videoURL: string;
}
function VideoTableComponent({ videoURL }: VideoTableComponentProps): JSX.Element {

  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current) {
      // Acciones a realizar una vez que el componente se ha montado, como configurar el videoURL o reproducir el video
      if (videoURL) {
        videoRef.current.src = videoURL;
        videoRef.current.load();
        videoRef.current.play();
      }
    }
  }, [videoURL]);

  return (
    <>
      <div className="m-5">      
         <VideoComponent videoRef={videoRef} />      
      </div>
    </>
  )
}

export default VideoTableComponent;
