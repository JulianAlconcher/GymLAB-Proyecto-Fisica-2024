
import React from 'react';
import { NivelExperienciaOption } from '../../enums/enumsExercise';

interface NivelExperienciaOptionsProps {
    value: NivelExperienciaOption | null;
    onChange: (value: NivelExperienciaOption) => void;
}

const NivelExperienciaOptions: React.FC<NivelExperienciaOptionsProps> = ({ value, onChange }) => {
    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedOption = e.target.value as NivelExperienciaOption; // Convertimos el valor a ExerciseOption
        onChange(selectedOption); // Llamamos a la función onChange con el valor seleccionado
    };

    return (
        <select value={value || ''} onChange={handleChange} className="m-2 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6">
            {Object.values(NivelExperienciaOption).map(option => (
                <option key={option} value={option}>{option}</option>
            ))}
        </select>
    );
};

export default NivelExperienciaOptions;
