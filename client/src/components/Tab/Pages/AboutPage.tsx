import React from 'react'

const AboutPage: React.FC = () => {
     return (
      <div className="font-sans p-6 max-w-5xl mx-auto bg-gray-100 rounded-lg shadow-md">
        <h1 className="text-3xl text-center text-gray-800 mb-6">¿Sabías que? Cuando vas al gimnasio estás trabajando con física...</h1>
        <section className="mb-6">
          <p className="text-gray-600">
          Cuando ingresas al gimnasio o te embarcas en una rutina de ejercicios , no solo estás desafiando tus músculos y tu sistema cardiovascular; También te involucrarás con los principios fundamentales de la física. Las leyes del movimiento de Sir Isaac Newton, que describen la relación entre un cuerpo y las fuerzas que actúan sobre él, desempeñan un papel importante a la hora de dar forma a su experiencia de ejercicio. En este blog, exploraremos cómo las leyes de Newton afectan su entrenamiento y brindaremos información sobre cómo optimizar su régimen de ejercicios.
            </p>
        </section>
        
        <section className="mb-6">
          <h2 className="text-2xl text-gray-700 mb-2">Primera Ley de Newton</h2>
          <p className="text-gray-600">
            La primera ley de Newton, también conocida como la ley de la inercia, establece que un objeto en reposo permanecerá en reposo y un objeto en movimiento permanecerá en movimiento a menos que actúe sobre él una fuerza externa.
          </p>
        </section>
        <section className="mb-6">
          <h2 className="text-2xl text-gray-700 mb-2">Segunda Ley de Newton</h2>
          <p className="text-gray-600">
            La segunda ley de Newton establece que la fuerza neta que actúa sobre un objeto es igual a la masa del objeto multiplicada por su aceleración (F = ma).
          </p>
        </section>
        <section>
          <h2 className="text-2xl text-gray-700 mb-2">Tercera Ley de Newton</h2>
          <p className="text-gray-600">
            La tercera ley de Newton establece que para cada acción, hay una reacción igual y opuesta.
          </p>
        </section>
      </div>
    );
  };

  
  export default AboutPage;