import React, { useState, useRef, useEffect } from 'react';

import VideoComponent from './VideoComponent';
import FormComponent from './FormComponent';

interface VideoTableProps {
  setShowGraph: React.Dispatch<React.SetStateAction<boolean>>;
}

function VideoTableComponent({ setShowGraph }: VideoTableProps): JSX.Element {
  const [videoURL, setVideoURL] = useState<string | null>(null); // Estado para almacenar la URL del video
  const videoRef = useRef<HTMLVideoElement>(null);
  const [showForm, setShowForm] = useState<boolean>(true);

  useEffect(() => {
    if (videoRef.current && videoURL) {
      videoRef.current.src = videoURL;
      videoRef.current.load();
      videoRef.current.play();
    }
  }, [videoURL]);

  const handleFormSubmitSuccess = () => {
    setShowForm(false);
    setShowGraph(true);
  };

  return (
    <div className="m-5 p4 h-full">
      {showForm ? (
        <FormComponent onSubmitSuccess={handleFormSubmitSuccess} setVideoURL={setVideoURL} />
      ) : (
        videoURL && <VideoComponent videoRef={videoRef} />
      )}
    </div>
  );
}

export default VideoTableComponent;
