// import { useState } from 'react';
// import GraphTableComponent from "./components/Tab/GraphTableComponent";
// import VideoTableComponent from "./components/Tab/VideoTableComponent";
import Header from "./components/Tab/Header";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/Tab/Pages/HomePage';
import AboutPage from './components/Tab/Pages/AboutPage';
import ContactPage from './components/Tab/Pages/ContactPage';
import MainPage from "./components/Tab/Pages/MainPage";
import GuidePage from "./components/Tab/Pages/GuidePage";
import Loading from "./components/Loading";

function App() {
  return (
    <Router>
    <div className="min-h-screen bg-white">
      <Header />
     <Routes>
          <Route path="/" Component={HomePage} />
          <Route path="/about" Component={AboutPage} />
          <Route path="/main" Component={MainPage} /> 
          <Route path="/contact" Component={ContactPage} />
          <Route path="/guide" Component={GuidePage} />
          <Route path="/loading" Component={Loading}/>
    </Routes>  
    </div>
    </Router>
  );
}

export default App;
