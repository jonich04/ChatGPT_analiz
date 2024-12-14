#import openai
#import os
#import pandas as pd

# Настройка API ключа
#openai.api_key = "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"

# Пример запроса к API
#response = openai.ChatCompletion.create(
  #  model="gpt-3.5-turbo",  # Актуальная модель
  #  messages=[
   #     {"role": "system", "content": "You are a helpful assistant."},
   #     {"role": "user", "content": "Hello, how are you?"}
  #  ]
#)

#print(response['choices'][0]['message']['content'])

# Загрузка CSV файла для анализа
#data = pd.read_excel(r"D:\5 семестр\fx_table.xlsx", engine='openpyxl')
#print(data.head(100))
# import openai
# import os
# import pandas as pd
# import PyPDF2
# from docx import Document
# import sys

# # Настройка API ключа
# openai.api_key = "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"

# # Функция для обработки Excel файлов
# def process_excel(file_path):
#     try:
#         data = pd.read_excel(file_path, engine='openpyxl')
#         text_data = data.to_string()
#         return text_data
#     except Exception as e:
#         print(f"Error processing Excel file: {e}")
#         return None

# # Функция для обработки CSV файлов
# def process_csv(file_path):
#     try:
#         data = pd.read_csv(file_path)
#         text_data = data.to_string()
#         return text_data
#     except Exception as e:
#         print(f"Error processing CSV file: {e}")
#         return None

# # Функция для обработки PDF файлов
# def process_pdf(file_path):
#     try:
#         with open(file_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text_data = ""
#             for page in range(len(reader.pages)):
#                 text_data += reader.pages[page].extract_text()
#             return text_data
#     except Exception as e:
#         print(f"Error processing PDF file: {e}")
#         return None

# # Функция для обработки Word файлов (.docx)
# def process_word(file_path):
#     try:
#         doc = Document(file_path)
#         text_data = ""
#         for para in doc.paragraphs:
#             text_data += para.text + "\n"
#         return text_data
#     except Exception as e:
#         print(f"Error processing Word file: {e}")
#         return None

# # Функция для обработки текстовых файлов
# def process_text_file(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             text_data = file.read()
#         return text_data
#     except Exception as e:
#         print(f"Error processing text file: {e}")
#         return None

# # Функция для загрузки данных в OpenAI
# def upload_to_openai(text_data):
#     try:
#         with open('extracted_data.txt', 'w', encoding='utf-8') as f:
#             f.write(text_data)

#         # Загрузка текстового файла в OpenAI
#         file = openai.File.create(
#             file=open("extracted_data.txt"),  # Путь к файлу
#             purpose='user_data'  # Цель использования файла
#         )
#         file_id = file['id']
#         print(f"File uploaded successfully with ID: {file_id}")
#         return file_id
#     except Exception as e:
#         print(f"Error uploading file to OpenAI: {e}")
#         return None

# # Функция для выполнения запроса с использованием данных файла
# def analyze_file_with_data(text_data):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # Актуальная модель
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": f"Please analyze the following data: \n{text_data}"}
#             ]
#         )
#         # Печать ответа
#         print(response['choices'][0]['message']['content'])
#     except Exception as e:
#         print(f"Error analyzing data with OpenAI: {e}")

# # Основной процесс для разных типов файлов
# def process_file(file_path):
#     text_data = None
    
#     if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
#         text_data = process_excel(file_path)
#     elif file_path.endswith('.csv'):
#         text_data = process_csv(file_path)
#     elif file_path.endswith('.pdf'):
#         text_data = process_pdf(file_path)
#     elif file_path.endswith('.docx'):
#         text_data = process_word(file_path)
#     elif file_path.endswith('.txt'):
#         text_data = process_text_file(file_path)
#     else:
#         print("Unsupported file type.")
#         return

#     if text_data:
#         # Анализируем данные
#         analyze_file_with_data(text_data)

# # Проверка аргументов командной строки
# if len(sys.argv) != 2:
#     print("Usage: python script.py <file_path>")
# else:
#     file_path = sys.argv[1]  # Получаем путь к файлу из командной строки
#     process_file(file_path)*/


