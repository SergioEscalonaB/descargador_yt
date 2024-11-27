import os
import yt_dlp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ruta principal (opcional para verificar que la app está funcionando)
@app.route('/')
def hello_world():
    return "¡La aplicación está funcionando!"

# Ruta para manejar la descarga de YouTube a MP3
@app.route('/download', methods=['GET'])
def download():
    # Obtener el parámetro 'url' de la solicitud GET
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Opciones para yt-dlp (conversión a mp3)
        ydl_opts = {
            'format': 'bestaudio/best',  # Selecciona el mejor formato de audio
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Calidad 192 kbps
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Ruta de salida de los archivos
        }

        # Iniciar la descarga usando yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Descargar el video

        return jsonify({"success": "Download started"}), 200  # Respuesta de éxito

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # En caso de error, devolver mensaje de error

# Asegúrate de que Flask escuche en el puerto proporcionado por Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Obtén el puerto de la variable de entorno
    app.run(host="0.0.0.0", port=port)  # Ejecuta la aplicación en 0.0.0.0 para permitir conexiones externas



