import GraphTableComponent from "./components/Tab/GraphTableComponent"
import VideoTableComponent from "./components/Tab/VideoTableComponent"
import Header from "./components/Tab/Header"

function App() {
  
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <div className="grid grid-cols-2 grid-flow-col gap-4">
        <VideoTableComponent />
        <GraphTableComponent />
      </div>
    </div>
  );
}

export default App;