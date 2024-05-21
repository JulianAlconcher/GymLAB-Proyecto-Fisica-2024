import React, { useState } from 'react';
import VideoTableComponent from '../VideoTableComponent';
import GraphTableComponent from '../GraphTableComponent';

const MainPage: React.FC = () => {
  const [refresh, setRefresh] = useState(false);

  return (
    <div className="grid grid-cols-2 grid-flow-col gap-4">
      <VideoTableComponent setRefresh={setRefresh} />
      <GraphTableComponent key={refresh ? "refresh-true" : "refresh-false"} />
    </div>
  );
};

export default MainPage;
