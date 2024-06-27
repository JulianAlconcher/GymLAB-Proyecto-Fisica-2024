import React from 'react';

const GuidePage: React.FC = () => {
  return (
    <div className="font-sans p-6 max-w-5xl mx-auto bg-gray-100 rounded-lg shadow-md">
      <h1 className="text-3xl text-center text-gray-800 mb-6">Guía para utilizar GymLAB</h1>
      
      <section className="mb-6">
        <h2 className="text-2xl text-gray-700 mb-2">Paso 1: Grabación del Video</h2>
        <p className="text-gray-600">
          Para utilizar nuestra aplicacion debes tener grabado un video del ejercicio que se desea analizar.
          El video debe estar grabado a una distancia de 2 metros de distancia entre la camara y la persona que realiza el ejercicio.
        </p>
        <p className="text-gray-600 font-bold"> Imagen Ilustrativa:</p>
        <img src="/DistanciaFisica.png" alt="Subir video" width="60%" className="h-auto"/>
        <p className="text-gray-600 "> 
        Tambien recomendamos que el video este bien claro y que el sitio de grabacion disponga de buena iluminacion para asegurar una mejor calidad</p>
      </section>
      
      <section className="mb-6">
        <h2 className="text-2xl text-gray-700 mb-2">Paso 2: Subir un video de tu ejercicio</h2>
        <p className="text-gray-600">
          Una vez que ya hayas grabado tu video realizando el ejercicio, deberas subirlo a la aplicacion.
          </p>
        <p className="text-gray-600 mb-4">
          Pero previo a la subida del video se deben completar un formulario para la obtencion de datos.
        </p>
        <img src="/formularioGuia.png" alt="Completar Formulario" className="h-auto mb-4"/>
        <p className="text-gray-600">
          <b>Peso(kg):</b> se debe indicar el peso actual de la persona que esta realizando el ejercicio.
        </p>
        <p className="text-gray-600">
         <b> Altura(cm):</b> se debe indicar la altura actual de la persona que esta realizando el ejercicio.
        </p>
        <p className="text-gray-600">
         <b> Peso de la mancuerna(kg):</b> Debe indicar el peso de la mancuerna con la cual realiza el ejercicio.
        </p>
        <p className="text-gray-600">
         <b> Medida del Antebrazo(cm):</b> Es uno de los datos mas imporantes, recomendamos que el antebrazo se mida con la mejor presicion posible.
        </p>
       
        <p className="text-gray-600"> Luego se debe seleccionar el <b>Ejercicio</b> que esta realizando y su <b>nivel</b> en el gimnasio</p>
        <p className="text-gray-600 mb-4"> Una vez completados estos datos se puede proceder a subir el video (El formato puede ser <b>MP4 o MOV </b>)</p>
        <img src="/FormularioGuia2.png" alt="Subir video" width="50%" className="h-auto mb-4"/>

      </section>
      
      <section className="mb-6">
        <h2 className="text-2xl text-gray-700 mb-2">Paso 3: Analizar el video</h2>
        <p className="text-gray-600">
          Una vez que el video se haya subido, la aplicación analizará el ejercicio utilizando la Fisica y devolverá un resumen detallado. 
        </p>
        <p className="text-gray-600 mb-4">
          Y podra observar el video con todos sus datos correspondientes y sus graficos como el siguiente: 
        </p>
        <img src="/MuestraGraficos.png" alt="Análisis de video" width="75%" className="h-auto mb-4"/>
      </section>
      
      <section className="mb-6">
        <h2 className="text-2xl text-gray-700 mb-2">Paso 4: Descarga del resumen</h2>
        <p className="text-gray-600">
          Después del análisis, podrás ver un resumen detallado de tu ejercicio. Esto incluirá estadísticas clave como 
          velocidad, aceleración, fuerza y energía. Utiliza esta información para mejorar tu técnica y optimizar tu rendimiento.
        </p>
        <img src="/PDF.png" alt="Resumen de ejercicio"  width="40%" className="h-auto"/>
      </section>
    </div>
  );
};

export default GuidePage;
