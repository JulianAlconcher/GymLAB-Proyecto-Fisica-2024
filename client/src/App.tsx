import { useState } from 'react';
import GraphTableComponent from "./components/Tab/GraphTableComponent";
import VideoTableComponent from "./components/Tab/VideoTableComponent";
import Header from "./components/Tab/Header";

function App() {
  const [showGraph, setShowGraph] = useState(false); 

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <div className="grid grid-cols-2 grid-flow-col gap-4 bg-[#333333]">
        <VideoTableComponent setShowGraph={setShowGraph} /> {}
        {showGraph && <GraphTableComponent />} {}
      </div>
    </div>
  );
}

export default App;
