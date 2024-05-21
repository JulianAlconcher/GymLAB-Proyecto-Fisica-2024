import React from 'react';

interface CardProps {
  imagePath: string;
  exerciseName: string;
  description: string;

}

const CardExercise: React.FC<CardProps> = ({ imagePath,exerciseName, description }) => {
    return (
      <div className="flex flex-wrap justify-center my-10">
        <div className="bg-white w-64 m-4 border border-dashed border-gray-100 shadow-md rounded-lg overflow-hidden"> {/* AquÃ he ajustado el ancho a w-64 */}
          <img src={imagePath} alt="" className="w- h-64 object-cover object-center" />
          <div className="p-4">
            <p className=" text-gray-900 font-semibold">{exerciseName}</p>
            <span className="text-gray-700">{description}</span>
            <div className="mt-8">
              <a href="#" className="px-4 py-2 bg-black shadow-lg border rounded-lg text-white uppercase font-semibold tracking-wider focus:outline-none focus:shadow-outline hover:bg-gray-800 active:bg-gray-700">Ver Demo</a>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  
export default CardExercise;