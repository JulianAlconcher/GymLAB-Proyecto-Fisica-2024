import pesa from "/pesa.png"
import {useNavigate } from "react-router-dom";


function Header(){
    {
        const navigate = useNavigate();
        const actualPath = window.location.pathname;
        const enabledLinkGymLab = actualPath !== '/loading'
        
    return(
        <div>
        <header className="bg-black text-white py-4 px-6">
        <div className="container mx-auto flex justify-between items-center">
          <div className= "flex items-center" 
            onClick={() => enabledLinkGymLab ? navigate("/") : null} 
            style={{ cursor: 'pointer' }}
          >
            <img src={pesa} alt="Gym Icon" className="h-8 mr-2" />
            <h1 className="text-2xl font-bold font-inter">
              GymLAB
            </h1>
          </div>
          <nav className="flex space-x-4">
            <button className="hover:text-gray-300" onClick={() => navigate("/guide")}  disabled={actualPath === '/loading'}>Guía de uso</button>
            <button className="hover:text-gray-300" onClick={() => navigate("/about")}  disabled={actualPath === '/loading'}>Informacion</button>
          </nav>
        </div>
      </header>
  </div>

    )
}
}

export default Header