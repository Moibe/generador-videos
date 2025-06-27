import io
import time
import globales
import random
import herramientas
import gradio_client
from fastapi import HTTPException, status
from huggingface_hub import InferenceClient


servidor = globales.servidor

def procesa_dni(platillo):

    print("Estoy en procesa DNI...")

    print("Y esto es contents: ", platillo)

    time.sleep(18)

    prompt = globales.previo + platillo
    print("Platillo enviado:", platillo) 

    try:

        dict_espacios = conexion_firebase.obtenDato('nowme', servidor, 'espacios')

        espacios_habilitados = [
        nombre for nombre, config in dict_espacios.items()
        if config.get("habilitado", False) # Usamos .get() para evitar KeyError si 'habilitado' no existe
        ]

        print(f"Espacios habilitados: {espacios_habilitados}")
        
        espacio_aleatorio_elegido = random.choice(espacios_habilitados)
        configuracion_espacio = dict_espacios[espacio_aleatorio_elegido]
        print(f"La configuración completa para '{espacio_aleatorio_elegido}' es: {configuracion_espacio}")

        client = gradio_client.Client(configuracion_espacio['ruta'], hf_token=globales.llave)
        #kwargs = selected_space_config['static_kwargs']

        result = client.predict(
        #**kwargs,
        prompt=prompt,
        #negative_prompt="live animals",
        # seed=42,
        # randomize_seed=True,
        width=786,
        height=568,
        # guidance_scale=3.5,
        # num_inference_steps=28,
        api_name=configuracion_espacio['api_name']       
        )

        #Cuando es GPU, debe de restar segundos disponibles de HF 
        herramientas.restaSegundosGPU(globales.work_cost)

        print("Platillo generado:", platillo)
        return result[0]

    except Exception as e:     
        print("Excepción: ", e)        
        # Opción para regresar imagen genérica. (ya no porque se envía desde backend.)
        # return "default.png"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )

def genera_platillo_gpu(platillo):

    prompt = globales.previo + platillo
    print("Platillo enviado:", platillo) 

    try:

        dict_espacios = conexion_firebase.obtenDato('nowme', servidor, 'espacios')

        espacios_habilitados = [
        nombre for nombre, config in dict_espacios.items()
        if config.get("habilitado", False) # Usamos .get() para evitar KeyError si 'habilitado' no existe
        ]

        print(f"Espacios habilitados: {espacios_habilitados}")
        
        espacio_aleatorio_elegido = random.choice(espacios_habilitados)
        configuracion_espacio = dict_espacios[espacio_aleatorio_elegido]
        print(f"La configuración completa para '{espacio_aleatorio_elegido}' es: {configuracion_espacio}")

        client = gradio_client.Client(configuracion_espacio['ruta'], hf_token=globales.llave)
        #kwargs = selected_space_config['static_kwargs']

        result = client.predict(
        #**kwargs,
        prompt=prompt,
        #negative_prompt="live animals",
        # seed=42,
        # randomize_seed=True,
        width=786,
        height=568,
        # guidance_scale=3.5,
        # num_inference_steps=28,
        api_name=configuracion_espacio['api_name']       
        )

        #Cuando es GPU, debe de restar segundos disponibles de HF 
        herramientas.restaSegundosGPU(globales.work_cost)

        print("Platillo generado:", platillo)
        return result[0]

    except Exception as e:     
        print("Excepción: ", e)        
        # Opción para regresar imagen genérica. (ya no porque se envía desde backend.)
        # return "default.png"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )

def genera_platillo_inference(platillo):

    dict_modelos = conexion_firebase.obtenDato('nowme', servidor, 'modelos')

    modelos_habilitados = [
        nombre for nombre, config in dict_modelos.items()
        if config.get("habilitado", False) # Usamos .get() para evitar KeyError si 'habilitado' no existe
        ]
    
    print(f"Modelos habilitados: {modelos_habilitados}")

    modelo_aleatorio_elegido = random.choice(modelos_habilitados)
    configuracion_modelo = dict_modelos[modelo_aleatorio_elegido]
    print(f"La configuración completa para '{modelo_aleatorio_elegido}' es: {configuracion_modelo}")


    creditos_restantes_inference = conexion_firebase.obtenDato('nowme', servidor, 'inferencias')
    
    #print("Los créditos restantes de hf-inference que tienes son: ", creditos_restantes_inference)
    if creditos_restantes_inference > 0:
        provedor_seleccionado = globales.proveedor
    else:
        provedor_seleccionado = globales.proveedor_back

    prompt = globales.previo + platillo
    print("Platillo enviado:", platillo)
       
    client = InferenceClient(
            provider= provedor_seleccionado,
            model=configuracion_modelo['ruta'],
            api_key=globales.llave
        )    
    
    print("Cree cliente: ", client)
    time.sleep(0)

    try: 
        image = client.text_to_image(
        prompt,
        #negative_prompt="live animals",        
        width=784, #786
        height=560, #568
        num_inference_steps=16
        ) 

        #Detenido momentaneamente por cambio a firebase.
        herramientas.restaSegundosInference(globales.inference_cost)              
        
    except Exception as e:
        print("Excepción: ", e)
        if "Gateway Time-out" in str(e): 
            print("GATEWAY TIME-OUT 💀")
            #modelo=globales.inferencia_backup #Con el nuevo paradigma ya no hay cambio de modelo.
            #Escribe en txt el nuevo modelo.
            #herramientas.modificaModeloActual(modelo)        
        error_impreso = f"Error: {e}"
        print(error_impreso)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    img_io = io.BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)
    print("Platillo generado:", platillo)
    return img_io    