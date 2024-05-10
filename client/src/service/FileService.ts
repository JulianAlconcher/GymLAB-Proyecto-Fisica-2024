const getVideoFromServer = async (videoPath : string) : Promise<Response> => {
    try {
        const videoResponse = await fetch(`http://localhost:8080/getVideo?video_path=${videoPath}`, {  //parametro con videoFile.name
            method: 'GET',
            headers: {
                'Range': 'bytes=0-' // Solicitar todo el archivo
            },
            cache: 'no-store' // Deshabilitar el almacenamiento en caché de la respuesta
        });

        return videoResponse
    }catch(error){
        console.log('Error al obtener el video',error)
        throw error
    }
}

const uploadFile = async (formData: FormData) : Promise<Response> => {
    try {
      const response = await fetch('http://localhost:8080/upload', { method: 'POST', body: formData });
     return response
    } catch (error) {
      console.error('Error uploading data:', error);
      throw error
    }
  };

const getFileFromServer = async () : Promise<Response> => {
    try {
    const response = await fetch('http://localhost:8080/getFile', { method: 'GET' });
    return response
    } catch (error) {
        console.error('Error al obtener data', error);
        throw error
    }
}



export default {
    uploadFile,
    getVideoFromServer,
    getFileFromServer,
    
}