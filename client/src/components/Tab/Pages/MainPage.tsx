import React from 'react';
import VideoTableComponent from '../VideoTableComponent';
import GraphTableComponent from '../GraphTableComponent';
import { useLocation } from 'react-router-dom';

const MainPage: React.FC = () => {
  const location = useLocation();
  
  const { videoURL } = location.state || {};

  return (
    <div>
      <div className="grid grid-cols-2 grid-flow-col gap-4">
        <VideoTableComponent videoURL={videoURL} />
        <GraphTableComponent />
      </div>
    </div>
  );
};

export default MainPage;
