# CTF_FORENCE

Plataforma offline de retos forenses digitales, esteganografía y criptografía basada en CTFd.

## 🚀 Despliegue Rápido

### Opción 1: Servidor Local (Recomendado)
Ejecutar el archivo batch:
```cmd
INICIAR_CTF.bat
```
O mediante consola de comandos:
```bash
python server.py
```
Acceder en el navegador a: `http://localhost:8100/challenges`

### Opción 2: Visualizador Directo sin servidor
Abrir en el navegador el archivo:
```text
visualizador_offline.html
```

---

## 📁 Estructura del Repositorio

- `retos_archivos/`: Archivos forenses de cada reto con nombres legibles.
- `files/`: Archivos organizados con hashes para descargas desde el servidor local.
- `themes/`: Interfaz, estilos CSS, JavaScript, fuentes y sonidos originales.
- `challenges.json`: Metadatos completos de los 10 retos (enunciados, categorías, puntos).
- `server.py`: Servidor backend local en Python compatible con la API de CTFd.
- `INICIAR_CTF.bat`: Lanzador en un clic para Windows.
- `visualizador_offline.html`: Visor estático independiente.
- `GUIA_Y_ENUNCIADOS.md`: Guía detallada con enunciados, pistas forenses y formatos de respuesta.

---

## 🎯 Retos Incluidos

1. **01 · Transmisión en el Pokégear** (Esteganografía - 175 pts)
2. **02 · Una foto cualquiera** (Forense - 70 pts)
3. **03 · El logo que no era solo un logo** (Esteganografía - 250 pts)
4. **04 · Te juro que está ahí dentro** (Criptografía - 225 pts)
5. **06 · Alguien tocó el reloj** (Forense - 200 pts)
6. **07 · Archivo corrupto** (Forense - 150 pts)
7. **08 · El equipo de origen** (Forense - 125 pts)
8. **09 · Todos iguales, uno distinto** (Criptografía - 75 pts)
9. **11 · Un poco torcido** (Criptografía - 125 pts)
10. **12 · Lo que se tiró a la basura** (Forense - 150 pts)
