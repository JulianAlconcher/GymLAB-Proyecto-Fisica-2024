import React from 'react';
import { useNavigate } from 'react-router-dom';

interface CardProps {
  imagePath: string;
  exerciseName: string;
  description: string;
  videoURL: string;
  dataURL: string;
}

const CardExercise: React.FC<CardProps> = ({ imagePath, exerciseName, description, videoURL, dataURL }) => {
  const navigate = useNavigate();

  const handleDemoClick = () => {
    navigate('/demo', { state: { videoURL, dataURL } });
  };

  return (
    <div className="flex flex-wrap justify-center">
      <div className="bg-white w-64 m-4 border border-dashed border-gray-100 shadow-md rounded-lg overflow-hidden">
        <img src={imagePath} alt="" className="w-full h-64 object-cover object-center" />
        <div className="p-4">
          <p className="text-gray-900 font-semibold">{exerciseName}</p>
          <span className="text-gray-700">{description}</span>
          <div className="mt-5">
            <button
              className="px-4 py-2 bg-black shadow-lg border rounded-lg text-white uppercase font-semibold tracking-wider focus:outline-none focus:shadow-outline hover:bg-gray-800 active:bg-gray-700"
              onClick={handleDemoClick}
            >
              Ver Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardExercise;
