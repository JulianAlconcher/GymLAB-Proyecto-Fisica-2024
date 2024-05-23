import React, { useState } from 'react';
import VideoTableComponent from '../VideoTableComponent';
import GraphTableComponent from '../GraphTableComponent';
import Loading from '../../Loading';

const MainPage: React.FC = () => {
  const [refresh, setRefresh] = useState(false);
  const [loading, setLoading] = useState(false);

  return (
    <div>
    <div>{loading ? <Loading /> : ""}</div>
      <div className="grid grid-cols-2 grid-flow-col gap-4">
        <VideoTableComponent setRefresh={setRefresh} setLoading={setLoading}/>
        {!loading && <GraphTableComponent key={refresh ? "refresh-true" : "refresh-false"} />}
      </div>
    </div>
  );
};

export default MainPage;
