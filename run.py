import subprocess

ffmpeg_command = [
                        'ffmpeg', '-y',
                        '-loop', '1',
                        '-i', 'media/tp.jpg',
                        '-t', str(3),
                        '-vf',
                        # f"scale=16:9:force_original_aspect_ratio=increase,"
                        # f"crop=16:9,"
                        f"zoompan=z='zoom+0.0005':d=25*60",
                        '-r', str(25),
                        '-pix_fmt', 'yuv420p',
                        '-c:v', 'libx264',
                        '-preset', 'fast',
                        'resultados/resultado.mp4'
                    ]

subprocess.run(ffmpeg_command, check=True)