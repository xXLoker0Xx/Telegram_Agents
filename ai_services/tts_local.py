# ai_services/tts_local.py
import os
import torch
import uuid
from pathlib import Path
from TTS.api import TTS

class XTTSWrapper:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.base_dir = Path(__file__).parent  # Ajusta según tu estructura
        self.model_dir = self.base_dir / "models" / "xtts"
        self.model = None
        self._setup_directories()
        print("xTTS model activated")
        
    def _setup_directories(self):
        """Crea los directorios necesarios para el almacenamiento de audio"""
        
        self.received_dir = Path("received_audio")
        self.output_dir = Path("output_audio")

        self.received_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    def load_model(self):
        """Carga el modelo XTTS solo cuando es necesario"""
        if not self.model:
            self.model = TTS(
            model_path=str(self.model_dir),
            config_path=str(self.model_dir / "config.json"),  # Ruta absoluta
            progress_bar=False
        ).to(self.device)
        return self.model

    async def process_audio(self, text: str, source_audio_path: Path) -> Path:
        """Procesa la clonación de voz de forma asíncrona"""
        try:
            # Generar nombre único para el archivo de salida
            output_filename = f"output_{uuid.uuid4().hex}.wav"
            output_path = self.output_dir / output_filename
            
            # Cargar modelo y generar audio
            print("Cargando el modelo...")
            tts = self.load_model()
            print("modelo cargado")
            tts.tts_to_file(
                text=text,
                speaker_wav=str(source_audio_path),
                language="es",
                file_path=str(output_path)
            )
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Error en la generación de audio: {str(e)}")

    async def save_incoming_audio(self, file) -> Path:
        """Guarda el audio recibido y devuelve su ruta"""
        try:
            filename = f"input_{uuid.uuid4().hex}.wav"
            save_path = self.received_dir / filename
            
            # Descargar y guardar el archivo
            await file.download_to_drive(custom_path=str(save_path))
            
            # Verificar que el archivo existe
            if not save_path.exists():
                raise FileNotFoundError("El archivo no se guardó correctamente")
                
            return save_path
            
        except Exception as e:
            raise RuntimeError(f"Error al guardar audio: {str(e)}")

# Instancia singleton para reutilizar el modelo
xtts_engine = XTTSWrapper()