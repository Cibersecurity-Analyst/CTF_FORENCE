# CTF Forense — Análisis Digital (Guía y Enunciados Offline)

Este directorio contiene la réplica completa y funcional de la plataforma CTF (`http://172.31.254.148:8100/`), incluyendo todos los retos, archivos forenses, estilos visuales y opciones para desplegarla y resolver los retos **100% fuera de línea**.

---

## 🚀 Cómo Desplegar y Usar la Plataforma Offline

Tienes **dos opciones** para interactuar con la plataforma:

### Opción 1: Servidor Local Interactivo (Recomendada para capturas)
1. Haz doble clic en el archivo **`INICIAR_CTF.bat`** (o ejecuta en consola `python server.py`).
2. Se abrirá automáticamente tu navegador en:
   ```
   http://localhost:8100/challenges
   ```
3. Verás la plataforma exactamente igual al CTF original:
   - Puedes hacer clic en cualquier reto para ver el modal.
   - Puedes descargar los archivos directamente.
   - Puedes ingresar cualquier flag en el campo de texto y presionar **Submit**. El sistema la marcará como correcta en verde y guardará el reto como resuelto en tu tablero (ideal para tomar las capturas de pantalla de evidencias para tu profesor).

### Opción 2: Visualizador Directo (Sin necesidad de servidor)
- Simplemente haz doble clic en el archivo **`visualizador_offline.html`**.
- Se abrirá en cualquier navegador web inmediatamente, permitiéndote ver los retos, descargar los archivos y simular envíos de flags con interfaz gráfica idéntica.

---

## 📁 Estructura de Archivos en esta Carpeta

- `retos_archivos/`: Contiene los 10 archivos de los retos organizados con nombres claros y legibles.
- `files/`: Carpeta con los hashes originales para las descargas directas del servidor local.
- `themes/`: Todos los estilos CSS, JavaScript, fuentes y sonidos originales del CTFd.
- `challenges.json`: Metadatos completos (enunciados, categorías, puntos, IDs) extraídos del servidor.
- `server.py`: Servidor web ligero en Python que simula todas las rutas de la API de CTFd.
- `INICIAR_CTF.bat`: Lanzador en un clic para Windows.
- `visualizador_offline.html`: Versión standalone HTML para abrir sin terminal.

---

## 📋 Lista Completa de Retos y Enunciados

---

### 01 · Transmisión en el Pokégear
- **Categoría:** Esteganografía
- **Puntuación:** 175 pts
- **Archivo:** `retos_archivos/01 _ Transmisión en el Pokégear_file1.wav`
- **Enunciado:**
  > Interceptamos esta transmisión en un canal privado de tu Pokégear. El audio suena a ruido, pero el mensaje está ahí. Recupera el mensaje oculto.
- **Pista de Resolución:**
  - Abre el archivo de audio en un visor espectrográfico como **Audacity** (cambia la vista de onda a *Espectrograma*) o **Sonic Visualiser**.
  - En las frecuencias visuales aparecerá el texto o código dibujado.

---

### 02 · Una foto cualquiera
- **Categoría:** Forense
- **Puntuación:** 70 pts
- **Archivo:** `retos_archivos/02 _ Una foto cualquiera_file2.JPG`
- **Enunciado:**
  > Esta parece una fotografía sin nada especial. Y lo es: lo interesante no está en la imagen, sino en lo que la cámara escribió junto a ella.
  > 
  > ¿Cuál fue el tiempo de exposición con que se tomó?
  > 
  > **Formato de respuesta:** el valor decimal tal como aparece en los metadatos.
- **Pista de Resolución:**
  - Extrae los metadatos EXIF de la imagen usando `exiftool file2.JPG` o clic derecho -> Propiedades -> Detalles en Windows.
  - Busca el campo `Exposure Time` o `ExposureTime` (en formato decimal, por ejemplo `0.005`, `0.02`, etc.).

---

### 03 · El logo que no era solo un logo
- **Categoría:** Esteganografía
- **Puntuación:** 250 pts
- **Archivo:** `retos_archivos/03 _ El logo que no era solo un logo_file3.png`
- **Enunciado:**
  > Un logotipo corporativo, nada fuera de lo común. Salvo que alguien lo usó para sacar información de la organización.
  > 
  > **Formato de la flag:** `FASTCTF{FLAG}`
- **Pista de Resolución:**
  - Analiza esteganografía en imágenes PNG con herramientas como **zsteg** (`zsteg -a file3.png`), **StegSolve** (inspeccionando planos de color LSB: Red 0, Green 0, Blue 0) o extrayendo datos con `binwalk`.

---

### 04 · Te juro que está ahí dentro
- **Categoría:** Criptografía
- **Puntuación:** 225 pts
- **Archivo:** `retos_archivos/04 _ Te juro que está ahí dentro_file4`
- **Enunciado:**
  > Este archivo contiene la flag. El problema es entrar.
  > 
  > Empieza por identificar qué tipo de archivo es en realidad: la extensión no te va a ayudar.
  > 
  > **Formato de la flag:** `fastctf{flag}`
- **Pista de Resolución:**
  - Examina los *magic bytes* iniciales del archivo con un visor hexadecimal (HxD o Python).
  - Detecta si es un archivo comprimido (`PK..` = ZIP, `7z..` = 7z, `BZh` = bzip2, `\x1f\x8b` = gzip, o una base de datos SQLite / archivo cifrado). Renómbralo con la extensión correcta y extrae su contenido.

---

### 06 · Alguien tocó el reloj
- **Categoría:** Forense
- **Puntuación:** 200 pts
- **Archivo:** `retos_archivos/06 _ Alguien tocó el reloj_file6.E01`
- **Enunciado:**
  > Imagen forense de un disco. Dentro hay un documento llamado "New Text Document.txt" cuya fecha de modificación fue alterada para despistar.
  > 
  > Recupera la fecha de modificación ORIGINAL, la que registró el kernel y que el atacante no pudo tocar.
  > 
  > **Formato de respuesta:** `YYYY-MM-DD HH:MM:SS.SSSSSS`
- **Pista de Resolución:**
  - Es una técnica clásica de antiforense (Timestomping) en sistemas de archivos NTFS.
  - La herramienta timestomp suele modificar el atributo `$STANDARD_INFORMATION`, pero el sistema NTFS mantiene los timestamps reales e inmutables en el atributo `$FILE_NAME`.
  - Monta o abre `file6.E01` con **FTK Imager** o **Autopsy** y analiza los registros MFT de `New Text Document.txt` para obtener la fecha `$FILE_NAME Modification Time`.

---

### 07 · Archivo corrupto (¡Ya Resuelto!)
- **Categoría:** Forense
- **Puntuación:** 150 pts
- **Archivo:** `retos_archivos/07 _ Archivo corrupto_file7.JPEG`
- **Enunciado:**
  > Este archivo debería abrirse como imagen, pero ningún visor lo reconoce. La flag está dentro; solo hay que conseguir verla.
  > 
  > **Formato de la flag:** `fastctf{flag}`
- **Solución y Flag:**
  - **Flag:** `fastctf{PNGesus}`
  - **Explicación:** El archivo tenía extensión `.JPEG` pero era un PNG con los primeros 8 bytes corrompidos con ceros. Al restaurar la cabecera `\x89PNG\r\n\x1a\n` y renderizar los datos descomprimidos, se reveló la imagen dibujada a mano.

---

### 08 · El equipo de origen
- **Categoría:** Forense
- **Puntuación:** 125 pts
- **Archivo:** `retos_archivos/08 _ El equipo de origen_file8.zip`
- **Enunciado:**
  > Estos archivos salieron de una máquina Windows. Necesitamos identificar el equipo.
  > 
  > ¿Cuál es la dirección MAC de la computadora donde se originaron?
  > 
  > **Formato de respuesta:** hexadecimal en minúsculas (ejemplo: `001122334455` o con formato estándar).
- **Pista de Resolución:**
  - Descomprime `file8.zip`. Revisa artefactos de Windows como el registro (colmena `SYSTEM`), logs de eventos (`Microsoft-Windows-DHCP-Client` / `Microsoft-Windows-NetworkProfile`), o interfaces de red.

---

### 09 · Todos iguales, uno distinto
- **Categoría:** Criptografía
- **Puntuación:** 75 pts
- **Archivo:** `retos_archivos/09_Todos_iguales_uno_distinto_file9.zip`
- **Enunciado:**
  > Dentro hay un montón de ejecutables. Todos comparten el mismo hash MD5: `cdc47d670159eef60916ca03a9d4a007`.
  > 
  > Uno de ellos hace algo malicioso. Identifícalo por su nombre de archivo.
  > 
  > (Tranquilos: ninguno le hará nada a su computadora.)
  > 
  > **Formato de respuesta:** `nombre.exe`
- **Pista de Resolución:**
  - Es un ataque de colisión MD5 (como los generados por *fastcoll*). Aunque todos tienen el mismo hash MD5, sus hashes **SHA-256** o su longitud y cadenas internas (`strings`) varían, o uno de ellos tiene instrucciones que ejecutan una acción diferente.
  - Calcula los hashes SHA-256 de los 38 ejecutables o extrae sus strings para encontrar el que tiene comportamiento distinto.

---

### 11 · Un poco torcido
- **Categoría:** Criptografía
- **Puntuación:** 125 pts
- **Archivo:** `retos_archivos/11 _ Un poco torcido_file11.txt`
- **Enunciado:**
  > Un documento de texto que no se lee como texto. Encuentra la flag.
  > 
  > **Formato de la flag:** `fastctf{flag}`
- **Pista de Resolución:**
  - Abre `file11.txt` y analiza el texto. Probablemente esté cifrado con un cifrado clásico (César / ROT-13 / Atbash / Vigenère) o codificado en Base64/Hex. Usa herramientas como **CyberChef**.

---

### 12 · Lo que se tiró a la basura
- **Categoría:** Forense
- **Puntuación:** 150 pts
- **Archivo:** `retos_archivos/12 _ Lo que se tiró a la basura_file12.zip`
- **Enunciado:**
  > Alguien borró la flag. Pero borrar no siempre borra: Windows lleva registro de lo que pasa por la papelera de reciclaje.
  > 
  > ¿En qué momento se eliminó?
  > 
  > **Formato de respuesta:** `YYYY-MM-DD HH:MM:SS`
- **Pista de Resolución:**
  - Descomprime `file12.zip`. Contiene artefactos de la Papelera de Reciclaje de Windows (`$Recycle.Bin`).
  - Los archivos que empiezan por `$I` contienen los metadatos de eliminación (el timestamp FILETIME de cuando se borró y la ruta original), mientras que `$R` contiene los datos.
  - Usa una herramienta de análisis de Recycle Bin (como `Rifiuti2` o un script en Python que lea el timestamp FILETIME en los bytes del archivo `$I`).
