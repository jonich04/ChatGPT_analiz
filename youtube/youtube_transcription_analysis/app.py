# from flask import Flask, request, render_template, jsonify
# from flask_cors import CORS
# from pytube import YouTube
# import whisper
# import os
# import openai
# import logging
# import yt_dlp as youtube_dl
# # Настройка логирования
# logging.basicConfig(level=logging.DEBUG)

# app = Flask(__name__)
# CORS(app)  # Для работы с CORS

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# openai.api_key = "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"

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/download', methods=['POST'])
# def download_video():
#     data = request.json
#     url = data.get("url")
#     if not url:
#         return jsonify({"error": "URL отсутствует"}), 400
#     try:
#         ydl_opts = {
#             'format': 'bestaudio/best',  # Для загрузки только аудио
#             'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(id)s.%(ext)s'),
#             'quiet': False,
#         }
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=True)
#             file_path = ydl.prepare_filename(info_dict)
#             return jsonify({"message": "Видео успешно загружено", "path": file_path})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     data = request.json
#     file_path = data.get("file_path")
    
#     if not file_path or not os.path.exists(file_path):
#         return jsonify({"error": "Файл отсутствует"}), 400
    
#     try:
#         model = whisper.load_model("base")
#         result = model.transcribe(file_path)
#         return jsonify({"transcription": result['text']})
    
#     except Exception as e:
#         logging.error(f"Ошибка при транскрибации: {str(e)}")
#         return jsonify({"error": f"Ошибка транскрибации: {str(e)}"}), 500

# @app.route('/analyze', methods=['POST'])
# def analyze_text():
#     data = request.json
#     transcription = data.get("transcription")
    
#     if not transcription:
#         return jsonify({"error": "Текст для анализа отсутствует"}), 400
    
#     try:
#         response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=f"Анализ текста: {transcription}",
#             max_tokens=100
#         )
#         return jsonify({"analysis": response.choices[0].text.strip()})
    
#     except Exception as e:
#         logging.error(f"Ошибка при анализе текста: {str(e)}")
#         return jsonify({"error": f"Ошибка анализа текста: {str(e)}"}), 500

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)  # Создаем папку для загрузки файлов, если её нет
#     app.run(debug=True)
import os
import logging
import whisper
import yt_dlp as youtube_dl
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import openai
from pydub import AudioSegment
from pydub.utils import which

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Для работы с CORS

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Убедитесь, что у вас есть ключ API OpenAI, если вы планируете его использовать
openai.api_key = "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"

# Убедитесь, что ffmpeg доступен для pydub
AudioSegment.ffmpeg = which("ffmpeg")

@app.route('/')
def index():
    return render_template('index.html')

@app.routea('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL отсутствует"}), 400
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Для загрузки только аудио
            'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(id)s.%(ext)s'),
            'quiet': False,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            
            # Логируем путь к загруженному файлу
            logging.debug(f"Загруженный файл: {file_path}")
            
            # Проверяем, существует ли файл
            if not os.path.exists(file_path):
                logging.error(f"Файл не найден: {file_path}")
                return jsonify({"error": "Не удалось найти загруженный файл"}), 500
            
            return jsonify({"message": "Видео успешно загружено", "path": file_path})
    except Exception as e:
        logging.error(f"Ошибка при загрузке видео: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Функция для конвертации .webm или другого формата в .wav
def convert_to_wav(input_file_path):
    output_file_path = input_file_path.replace(".webm", ".wav").replace(".mp4", ".wav")
    try:
        audio = AudioSegment.from_file(input_file_path)
        audio.export(output_file_path, format="wav")
        logging.debug(f"Файл успешно конвертирован в WAV: {output_file_path}")
        return output_file_path
    except Exception as e:
        logging.error(f"Ошибка при конвертации: {str(e)}")
        return None

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.json
    file_path = data.get("file_path")

    if not file_path:
        logging.error("Не был передан путь к файлу.")
        return jsonify({"error": "Файл отсутствует"}), 400

    # Получаем полный путь
    full_file_path = os.path.join(os.getcwd(), file_path)

    # Логируем полный путь
    logging.debug(f"Файл для транскрибации: {full_file_path}")

    if not os.path.exists(full_file_path):
        logging.error(f"Файл не найден: {full_file_path}")
        return jsonify({"error": "Файл не найден"}), 400

    try:
        # Проверяем, нужно ли конвертировать файл
        if not full_file_path.endswith(".wav"):
            logging.debug(f"Конвертируем файл {full_file_path} в формат WAV")
            wav_file_path = convert_to_wav(full_file_path)
            if not wav_file_path:
                return jsonify({"error": "Ошибка при конвертации файла."}), 500
            full_file_path = wav_file_path  # Используем новый файл для транскрибации

        logging.debug(f"Транскрибация файла: {full_file_path}")
        model = whisper.load_model("base")
        result = model.transcribe(full_file_path)

        return jsonify({"transcription": result['text']})
    
    except Exception as e:
        logging.error(f"Ошибка при транскрибации: {str(e)}")
        return jsonify({"error": f"Ошибка транскрибации: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    transcription = data.get("transcription")
    
    if not transcription:
        return jsonify({"error": "Текст для анализа отсутствует"}), 400
    
    try:
        # Использование OpenAI API для анализа текста
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Анализ текста: {transcription}",
            max_tokens=100
        )
        return jsonify({"analysis": response.choices[0].text.strip()})
    
    except Exception as e:
        logging.error(f"Ошибка при анализе текста: {str(e)}")
        return jsonify({"error": f"Ошибка анализа текста: {str(e)}"}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Создаем папку для загрузки файлов, если её нет
    app.run(debug=True)


