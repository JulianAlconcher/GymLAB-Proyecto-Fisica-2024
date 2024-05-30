import React from 'react';
import VideoTableComponent from '../VideoTableComponent';
import { useLocation } from 'react-router-dom';

const MainPage: React.FC = () => {
  const location = useLocation();
  
  const { videoURL } = location.state || {};

  return (
    <div>
      <div className="">
        <VideoTableComponent videoURL={videoURL} />
      </div>
    </div>
  );
};

export default MainPage;