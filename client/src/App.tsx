import GraphTableComponent from "./components/Tab/GraphTableComponent"
import VideoTableComponent from "./components/Tab/VideoTableComponent"


function App() {
  
  return (
    <div className="grid grid-col-2 grid-flow-col gap-4  " >
      <VideoTableComponent />
      <GraphTableComponent/>
    </div>
  )
}

export default App
