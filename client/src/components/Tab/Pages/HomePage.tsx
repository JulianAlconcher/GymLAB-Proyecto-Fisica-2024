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
              <h1 className="text-4xl font-bold">GymLAB</h1>
              <p className="text-lg text-gray-600 mb-6">¡Testea vos mismo tus ejercicios del gimnasio!</p>
              <button className="bg-black hover:bg-gray-800 text-white font-bold py-2 px-4 rounded mb-4" onClick={handleStartClick}>
                  Comienza YA
              </button>
              <p className="text-lg text-gray-500">O prueba uno de nuestros ejemplos</p>
              <div className='flex flex-grow'>
                <div className="grid grid-cols-4 gap-2 w-full">
                <CardExercise imagePath='/EjemploBiceps4.png' exerciseName='Curl Biceps 7.5kg' description='Ejemplo curl de biceps parado con mancuernas de 7.5kg' videoURL='/processed_video.mp4' dataURL='/pose_data.json' />
                <CardExercise imagePath='/EjemploBiceps3.png' exerciseName='Curl Biceps 10kg' description='Ejemplo curl de biceps parado con mancuernas de 10kg' videoURL='/processed_video.mp4' dataURL='/pose_data.json' />
                <CardExercise imagePath='/EjemploBiceps2.png' exerciseName='Curl Biceps 12.5kg' description='Ejemplo curl de biceps parado con mancuernas de 12.5kg' videoURL='/processed_video.mp4' dataURL='/pose_data.json' />
                <CardExercise imagePath='/EjemploBiceps.png' exerciseName='Curl Biceps 15kg' description='Ejemplo curl de biceps parado con mancuernas de 15kg' videoURL='/processed_video.mp4' dataURL='/pose_data.json' />
                </div>
              </div>
          </div>
      </div>
  );
}

export default PaginaInicio;