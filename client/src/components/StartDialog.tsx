import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '../components/Tab/Dialog';
import ExerciseOptions from './Tab/ExerciseOptions';
import { ChangeEvent, FormEvent, useState } from 'react';
import fileService from "../service/FileService"
import { ExerciseOption } from '../enums/enumsExercise';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';

interface StartDialogProps {
    isOpen: boolean;
    onClose: () => void;
}

export const StartDialog: React.FC<StartDialogProps> = ({ isOpen, onClose }) => {
    const [exercise, setExercise] = useState<ExerciseOption | null>(ExerciseOption.Bicep);
    const [videoFile, setVideoFile] = useState<File | null>(null);
    const [weight, setWeight] = useState<string>("20");
    const navigate = useNavigate();

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        navigate('/loading');
        try {
            // Verificar si todos los campos están completos
            if (!exercise || !videoFile || !weight) {
                alert('Por favor, complete todos los campos.');
                return;
            }
    
            // Crear el objeto FormData
            const formData = new FormData();
            formData.append('exercise', exercise);
            formData.append('video', videoFile);
            formData.append('weight', weight);
    
            // Subir el archivo al servidor
            await uploadFile(formData);
    
            // Obtener la respuesta del servidor y convertirla a JSON 
            const responseData = await getFileFromServer();
            const jsonData = await responseData.json();
            console.log(jsonData);
    
            // Obtener el video del servidor y manejar la respuesta
            const videoURL = await getVideoFromServerAndHandleResponse();
    
            // Esperar a que videoURL se establezca antes de navegar
            if (videoURL) {
                navigate('/main', { state: { videoURL, jsonData } }); // Manda blob a main y jsondata para los graficos
                onClose(); // Cierra la ventana
            } else {
                console.error('videoURL is null');
            }
        } catch (error) {
            console.error('Error handling submit:', error);
            alert('Ocurrió un error al procesar el formulario. Por favor, inténtelo de nuevo.');
        }
    };
    
    const getVideoFromServerAndHandleResponse = async (): Promise<string | null> => {
        try {
            const responseGetVideo = await fileService.getVideoFromServer(videoFile?.name as string);
            return await handleVideoResponse(responseGetVideo);
        } catch (error) {
            console.error('Error fetching video:', error);
            throw error;
        }
    };
    
    const handleVideoResponse = async (response: Response): Promise<string | null> => {
        if (response.ok) {
            const blob = await response.blob();
            const videoURL = URL.createObjectURL(blob);
            return videoURL;
        } else {
            console.error('Failed to get video from server');
            return null;
        }
    };

    const getFileFromServer = async (): Promise<Response> => {
        try {
            return await fileService.getFileFromServer();
        } catch (error) {
            console.error('Error getting file from server:', error);
            throw error;
        }
    };

    const uploadFile = async (formData: FormData): Promise<void> => {
        try {
            await fileService.uploadFile(formData);
        } catch (error) {
            console.error('Error uploading file:', error);
            throw error;
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>Formulario de Ejercicios</DialogTitle>
                    <DialogDescription>Completa los datos solicitados para probar tus ejercicios</DialogDescription>
                </DialogHeader>
                <form onSubmit={handleSubmit}>
                    <div className="grid flex-1 gap-2">
                        <div className="grid grid-cols-2 w-full gap-4 items-center">
                            <label className="w-1/3">Peso:</label>
                            <input className="w-2/3 focus:ring-0 sm:text-sm sm:leading-6" style={{ width: '100px' }} value={weight} onChange={(event: ChangeEvent<HTMLInputElement>) => setWeight(event.target.value)} />
                        </div>
                        <div className="grid grid-cols-2 w-full items-center">
                            <label className="w-1/3">Ejercicio:</label>
                            <div className="w-auto">
                                <ExerciseOptions value={exercise || null} onChange={setExercise} />
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4 w-full items-center">
                            <label className="w-1/3">Video:</label>
                            <input id="file-upload" name="file-upload" type="file" className="w-auto" onChange={(event: ChangeEvent<HTMLInputElement>) => {
                                if (event.target.files) {
                                    setVideoFile(event.target.files[0]);
                                }
                            }} />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="contained" type="submit">Comenzar</Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
};

export default StartDialog;
