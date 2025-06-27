import time
import subprocess
import herramientas


async def motion(imagen):

    current_timestamp_int = int(time.time())
    print("Ésto es current time stamp: ", current_timestamp_int)

    print("Esto es imagen en monomotion: ", imagen)

    ffmpeg_command = [
                            'ffmpeg', '-y',
                            '-loop', '1',
                            '-i', 
                            f'{imagen}',
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
                            f'resultados/{current_timestamp_int}.mp4'
                        ]
    
    print("Comando:")
    print(ffmpeg_command)
    
    subprocess.run(ffmpeg_command, check=True)

    return f'resultados/{current_timestamp_int}.mp4'

async def cinema(lista):

    lista = herramientas.lista_archivos('media')
    print("Ésto es lista:", lista)    

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
                                f'resultados1/{elemento}.mp4'
                            ]
        
        print("Comando:")
        print(ffmpeg_command)
        
        subprocess.run(ffmpeg_command, check=True)