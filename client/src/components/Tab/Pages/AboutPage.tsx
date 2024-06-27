import React from 'react'

const AboutPage: React.FC = () => {
     return (
      <div className="font-sans p-6 max-w-5xl mx-auto bg-gray-100 rounded-lg shadow-md">
        <h1 className="text-3xl text-center text-gray-800 mb-6">¿Sabías que? Cuando vas al gimnasio estás trabajando con física...</h1>
        <section className="mb-6">
          <p className="text-gray-600">
          Cuando ingresas al gimnasio o te embarcas en una rutina de ejercicios , no solo estás desafiando tus músculos y tu sistema cardiovascular; 
          También te involucras con los principios fundamentales de la física. Las leyes del movimiento de Sir Isaac Newton, que describen la relación 
          entre un cuerpo y las fuerzas que actúan sobre él, desempeñan un papel importante a la hora de dar forma a su experiencia de ejercicio. 
          
            </p>
          <p className="text-gray-600">
          Utilizando GymLAB vamos a ver como las leyes de la Fisica afectan en nuestro entrenamiento y brindaremos informacion sobre como optimizar sus ejercicios.
            </p>
        </section>
        
        <section className="mb-6">
          <h2 className="text-2xl text-gray-700 mb-2">Velocidad y Aceleracion</h2>
          <h2 className="text-xl text-gray-700 mb-2 font-bold">Velocidad</h2>
          <p className="text-gray-600 font-bold ">
          La velocidad es el cambio de posición de un objeto con respecto al tiempo 
          </p>
          <p className="text-gray-600">
            Para el caso del ejercicio de Curl de Bicep se calcula a partir de la posicion de la muñeca entre dos tiempos.
          </p>
          <p className="text-gray-600">
            La idea es capturar la posicion entre cada frame del video y de esta manera poder almacenar la velocidad con la que se mueve el brazo.
          </p>
          <p className="text-gray-600">
          La formula es la siguiente:
          </p>
          <img src="/Velocidad.png" alt="Velocidad" width="75%" className="h-auto"/>
          <h2 className="text-xl text-gray-700 mb-2 font-bold">Aceleracion</h2>
          <p className="text-gray-600 font-bold">
           La aceleración es el cambio de velocidad de un objeto en un cierto período de tiempo. 
           Es como medir cuánto más rápido o más lento algo se mueve.
          </p>
          <p className="text-gray-600">
           Se calcula a partir de los datos obtenidos anteriormente de la velocidad y se calcula la diferencia entre la Velocidad
           entre cada par de frames 
          </p>
          <p className="text-gray-600">
           La formula es la siguiente:
          </p>
          <img src="/Aceleracion.png" alt="Velocidad" width="55%" className="h-auto"/>

        </section>
        <section className="mb-6">
          <h2 className="text-2xl text-gray-700 mb-2 font-bold">Fuerza</h2>
          <p className="text-gray-600">
            Para calcular la fuerza maxima que se realiza se tuvo en cuenta lo siguiente:
          </p>
          <img src="/Fuerza.png" alt="Fuerzas" width="75%" className="h-auto m-2"/>
          <p className="text-gray-600">
            Y luego de calcular los distintos puntos de inercia podemos calcular la fuerza del bicep que es lo que nos interesa en este ejercicio:
          </p>
          <img src="/Fuerza2.png" alt="Calculo de Fuerzas" width="75%" className="h-auto m-2 "/>
          
        </section>
        <section>
          <h2 className="text-2xl text-gray-700 mb-2 font-bold">Energia</h2>
          <p className="text-gray-600">
            La energia nos importa calcularlo ya que vamos a poder saber cuantas calorias estamos gastando cuando realizamos el ejercicio de Curl de Bicep.
          </p>
          <p className="text-gray-600">
            Para ello calculamos: Energia <b> Potencial Gravitatoria</b>, la Energia <b>Cinética</b> y la Energia <b>Mecánica</b>.
          </p>
          <p className="text-gray-600">
            Para luego a partir de esta ultima poder obtener las calorias que se consumen al realizar el ejercicio.
          </p>
          <img src="/Energia1.png" alt="Energias" width="75%" className="h-auto m-2"/>
          <img src="/Energia2.png" alt="Calculo de Calorias" width="75%" className="h-auto m-2"/>

        </section>
      </div>
    );
  };

  
  export default AboutPage;