import subprocess
import herramientas

lista = herramientas.lista_archivos('media')

for elemento in lista: 

    ffmpeg_command = [
                            'ffmpeg', '-y',
                            '-loop', '1',
                            '-i', 
                            f'media/{elemento}',
                            '-t', str(3),
                            '-vf',
                            f"scale=1280:720:force_original_aspect_ratio=increase,"
                            f"crop=1280:720,"
                            f"zoompan=z='zoom+0.0005':d=1500", #al zoom actual le vas a aumentar 
                            '-r', str(25),
                            '-pix_fmt', 'yuv420p',
                            '-c:v', 'libx264',
                            '-preset', 'fast',
                            '-movflags', '+faststart',  # Agregar esta línea
                            f'resultados/{elemento}.mp4'
                        ]
    
    print("Comando:")
    print(ffmpeg_command)
    
    subprocess.run(ffmpeg_command, check=True)