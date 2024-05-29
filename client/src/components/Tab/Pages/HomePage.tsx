import CardExercise from '../../CardExercise';
import { useState } from 'react';
import StartDialog from '../../StartDialog';


function PaginaInicio() {
  const [dialog, setDialog] = useState(false);
 

  const handleStartClick = () => {
      setDialog(true);
  };

  const handleCloseDialog = () => {
      setDialog(false);
  };

  return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-200">
          <StartDialog isOpen={dialog} onClose={handleCloseDialog} />
          <div className="text-center">
              <h1 className="text-4xl font-bold mt-3">GymLAB</h1>
              <p className="text-lg text-gray-600 mb-8">¡Testea vos mismo tus ejercicios del gimnasio!</p>
              <button className="bg-black hover:bg-gray-800 text-white font-bold py-2 px-4 rounded mb-4" onClick={handleStartClick}>
                  Comienza YA
              </button>
              <p className="text-lg text-gray-500">O prueba uno de nuestros ejemplos</p>
              <div className="grid grid-cols-4 gap-2 w-full">
                  <CardExercise imagePath='/EjemploBiceps.png' exerciseName='Curl Biceps' description='Ejemplo curl de biceps parado con mancuernas de 15kg'/>
                  <CardExercise imagePath='/EjemploSentadilla.png' exerciseName='Sentadillas' description='Ejemplo sentadillas con barra, con un peso de 60kg'/>
                  <CardExercise imagePath='/EjemploPressPlano.png' exerciseName='Press Plano' description='Ejemplo press plano en banco con mancuernas de 15kg'/>
                  <CardExercise imagePath='/EjemploPressInclinado.png' exerciseName='Press Inclinado' description='Ejemplo press inclinado con mancuernas de 15kg'/>
              </div>
          </div>
      </div>
  );
}

export default PaginaInicio;