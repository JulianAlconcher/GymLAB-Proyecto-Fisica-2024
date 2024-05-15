import { useState } from 'react';
import GraphTableComponent from "./components/Tab/GraphTableComponent"
import VideoTableComponent from "./components/Tab/VideoTableComponent"
import Header from "./components/Tab/Header"

function App() {
  const [showGraph, setShowGraph] = useState(false); // Estado para controlar la visibilidad de GraphTableComponent

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <div className="grid grid-cols-2 grid-flow-col gap-4">
        <VideoTableComponent setShowGraph={setShowGraph} /> {/* Pasamos setShowGraph como prop a VideoTableComponent */}
        {showGraph && <GraphTableComponent />} {/* Mostramos GraphTableComponent solo si showGraph es true */}
      </div>
    </div>
  );
}

export default App;
