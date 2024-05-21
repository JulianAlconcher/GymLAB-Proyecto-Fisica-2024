import pesa from "/pesa.png"
import { Link, useNavigate } from "react-router-dom";

function Header(){

    {
        const navigate = useNavigate();
    return(
        <div>
        <header className="bg-black text-white py-4 px-6">
        <div className="container mx-auto flex justify-between items-center">
          <div className= "flex items-center">
            <img src={pesa} alt="Gym Icon" className="h-8 mr-2" />
            <h1 className="text-2xl font-bold font-inter"onClick={() => navigate('/')}style={{ cursor: 'pointer' }}>
              GymLAB
            </h1>
          </div>
          <nav className="flex space-x-4">
            <button className="hover:text-gray-300" onClick={() => navigate("/guide")}>Guía de uso</button>
            <button className="hover:text-gray-300" onClick={() => navigate("/about")}>Como Funciona</button>
           <button className="hover:text-gray-300" onClick={() => navigate("/contact")}>Contacto</button>
          </nav>
        </div>
      </header>
  </div>

    )
}
}

export default Header