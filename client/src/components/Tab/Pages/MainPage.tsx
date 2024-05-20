import React, { useState } from 'react'
import VideoTableComponent from '../VideoTableComponent';
import GraphTableComponent from '../GraphTableComponent';

const MainPage: React.FC = () => {

    const [showGraph, setShowGraph] = useState(false); 
    
    return (
    <div className="grid grid-cols-2 grid-flow-col gap-4 ">
    <VideoTableComponent setShowGraph={setShowGraph} /> {}
    {showGraph && <GraphTableComponent />} {}
  </div>  
  )
  };

  
  export default MainPage;