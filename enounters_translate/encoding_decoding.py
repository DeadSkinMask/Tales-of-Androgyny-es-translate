import re

def encode_text(text):
    """
    Codifica el texto reemplazando caracteres especiales y encerrando frases en mayúsculas entre llaves cuadradas.
    """
    # Reemplazar saltos de línea y tabulaciones
    text = text.replace("\n", "[1n]").replace("\t", "[2n]")
    
    # Encontrar frases en mayúsculas y encerrarlas entre corchetes
    def replace_uppercase(match):
        return f"[{match.group(0)}]"
    
    # Expresión regular para encontrar palabras/frases en mayúsculas
    text = re.sub(r'\b[A-ZÁÉÍÓÚÑÜ]{2,}(?:\s+[A-ZÁÉÍÓÚÑÜ]{2,})*\b', replace_uppercase, text)
    
    return text

def decode_text(encoded_text):
    """
    Decodifica el texto revertiendo los cambios realizados por encode_text.
    """
    # Revertir los reemplazos de caracteres especiales
    text = encoded_text.replace("[1n]", "\n").replace("[2n]", "\t")
    
    # Función para quitar los corchetes y poner el texto en mayúsculas
    def remove_brackets(match):
        # El texto entre corchetes, en mayúsculas
        return match.group(1).upper()
    
    # Expresión regular para encontrar las frases dentro de corchetes
    text = re.sub(r'\[([A-Za-záéíóúüñÁÉÍÓÚÑÜ\s]+)\]', remove_brackets, text)
    
    return text

# Ejemplo de uso
texto_original = """Este es un EJEMPLO de texto.\nAquí hay otro PARÁGRAFO con M más contenido.\tY una tabulación."""
texto_codificado = encode_text(texto_original)
print("Texto codificado:")
print(texto_codificado)

# Supongamos que esto fue procesado por la API
texto_traducido = texto_codificado  # Solo para simular el flujo
texto_decodificado = decode_text(texto_traducido)
print("\nTexto decodificado:")
print(texto_decodificado)

def buscar_simbolos_con_espacios(texto):
    # Definir los símbolos que queremos buscar
    #simbolos = re.escape(r"[!&[]{}()$%:,#¿¡?@]")
    simbolos = re.escape(r"!&[]{}()$%:#?@")
    
    # Crear una lista para almacenar los resultados
    resultado = []
    
    # Usar expresión regular para encontrar los símbolos con sus posibles espacios antes o después
    matches = re.finditer(r"(\s*[" + simbolos + r"]\s*)", texto)
    
    # Iterar sobre los resultados encontrados
    for match in matches:
        # Agregar el texto encontrado (símbolo y espacios) al resultado
        resultado.append(match.group())
    
    return resultado

def reemplazar_simbolos_con_espacios(texto_entrada, array_simbolos):
    # El índice para recorrer el array de símbolos
    indice = 0
    resultado = []

    # Recorrer cada carácter del texto de entrada
    i = 0
    while i < len(texto_entrada):
        # Verificar si el carácter actual en el texto de entrada corresponde al símbolo en el array
        if indice < len(array_simbolos):
            simbolo_con_espacios = array_simbolos[indice]
            simbolo_sin_espacios = simbolo_con_espacios.strip()  # Eliminar los espacios para comparar solo el símbolo

            # Si el símbolo sin espacios coincide con el carácter actual en el texto
            if texto_entrada[i:i + len(simbolo_sin_espacios)] == simbolo_sin_espacios:
                # Reemplazar por el símbolo más los espacios
                resultado.append(simbolo_con_espacios)
                # Saltar el tamaño del símbolo en el texto de entrada
                i += len(simbolo_sin_espacios)
                # Mover al siguiente símbolo del array
                indice += 1
                continue
        
        # Si no encontramos una coincidencia, agregar el carácter actual al resultado
        resultado.append(texto_entrada[i])
        i += 1

    # Devolver el texto con los símbolos y los espacios
    return ''.join(resultado)

#### quita espacios innecesarios:
def ajustar_espacios(original, traducido):
    # Lista de símbolos a considerar
    simbolos = r"!&[]{}()$%:#¿¡?@"
    
    # Expresión regular para encontrar símbolos y sus espacios en el texto traducido
    patron = re.compile(fr"(\s?)([{re.escape(simbolos)}])(\s?)")
    trimmed = patron.sub(r"\2", traducido)
    
    array_simbols = buscar_simbolos_con_espacios(original)
    
    resultado = reemplazar_simbolos_con_espacios(trimmed, array_simbols)
    
    # Aplicar la función a todo el texto traducido

    return resultado

def ajustar_puntos_suspensivos(texto):
    # Expresión regular para encontrar puntos suspensivos con espacio antes
    patron = re.compile(r"\s+(\.\.\.)")
    # Eliminar el espacio antes de los puntos suspensivos
    return patron.sub(r"\1", texto)

def eliminar_espacios_dobles(original, texto_ajustado):
    # Verificar si el texto original contiene espacios dobles
    contiene_espacios_dobles = "  " in original
    if not contiene_espacios_dobles:
        # Eliminar espacios dobles en todo el texto ajustado
        texto_ajustado = re.sub(r"\s{2,}", " ", texto_ajustado)
    return texto_ajustado

#Funcion principal:
def ajustar_traduccion(original, traducido):
    # Ajustar espacios para los símbolos
    ajustado = ajustar_espacios(original, traducido)
    # Ajustar puntos suspensivos
    ajustado = ajustar_puntos_suspensivos(ajustado)
    # Eliminar espacios dobles si el texto original no los tiene
    ajustado = eliminar_espacios_dobles(original, ajustado)
    # Decodificar texto
    decodificado = decode_text(ajustado)
    print("\nTexto Original:", original)
    print("Texto Traducido:", traducido)
    print("Texto Ajustado:", ajustado)
    print("Texto Decodificado:", decodificado)

# Ejemplo de uso
original = "Hello! How are you? Look at this: #amazing... no spaces... [1n][1n][1n][1n] {Tales of Androginy}"
traducido = "¡ Hola ! ¿ Cómo estás ? Mira esto : # increíble ... no hay espacios ... [1n] [1n] [1n] [1n] {Tales of Androginy}"

ajustar_traduccion(original, traducido)

test_decode = decode_text("el [Velóz] murcielago [indú] come[1n]Papayas y [Peras] con un ñandu [añil]")
print("\nDecode Test:")
print(test_decode)
