import { useState } from "react";
import pesa from "/pesa.png"

function Header(){

    {
        const [showModal, setShowModal] = useState(false);
      
        const toggleModal = () => {
          setShowModal(!showModal);
        };
    

    return(
        <div>
        <header className="bg-black text-white py-4 px-6">
        <div className="container mx-auto flex justify-between items-center">
          <div className= "flex items-center">
            <img src={pesa} alt="Gym Icon" className="h-8 mr-2" />
            <h1 className="text-2xl font-bold font-inter">GymLAB</h1>
          </div>
          <nav className="flex space-x-4">
          <button className="hover:text-gray-300" onClick={toggleModal}>Guía de uso</button>
            <a href="#" className="hover:text-gray-300">Sobre nosotros</a>
            {/* Aaca podemos agregar mas botones, deje estos como una prueba */}
          </nav>
        </div>
      </header>

        {showModal && (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded-lg">
        {/* Contenido de la modal */}
        <h2 className="text-lg font-bold mb-4">Guía de uso</h2>
        <p>
            Lo primero que se debera seleccionar es que tipo de ejercicio va a analizar el cual puede ser 
            elegido dentro de la lista desplegable, como se observa en la imagen
            <img src="/Paso1.png" alt="Paso 1" className="mb-4 w-3/4 h-auto" />
            Aca continua la guia... todavia le falta 

        </p>
        <button className="mt-4 px-4 py-2 bg-gray-900 text-white rounded-md" onClick={toggleModal}>Cerrar</button>
      </div>
    </div>
         )}
  </div>

    )
}
}

export default Header