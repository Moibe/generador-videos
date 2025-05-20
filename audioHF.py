from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch
import time

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")
#synthesiser = pipeline("text-to-speech", "Sandiago21/speecht5_finetuned_facebook_voxpopuli_spanish") 
#synthesiser = pipeline("text-to-speech", "jjyaoao/speecht5_voxpopuli_spanish")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
# You can replace this embedding with your own as well.

dialogo = """
Las piedras preciosas son, en esencia, minerales, rocas o materiales orgánicos que han sido seleccionados por su 
belleza, durabilidad y rareza, lo que les confiere un gran valor. Son objetos de deseo y admiración desde hace milenios, 
utilizados en joyería, objetos de arte y como símbolos de estatus o poder.
"""

unix_timestamp_float = time.time()
start_time = time.time()  # Registra el tiempo de inicio
speech = synthesiser("Lo del puto perro", forward_params={"speaker_embeddings": speaker_embedding})
end_time = time.time()    # Registra el tiempo de finalización

# Calcula la duración
duration = end_time - start_time

sf.write(f"audioHF_ms_{unix_timestamp_float}_{duration}s.wav", speech["audio"], samplerate=speech["sampling_rate"])
