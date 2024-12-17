import requests

# URL do endpoint Django
url = "http://127.0.0.1:8000/upload-file/"

# Caminho do arquivo a ser enviado
file_path = "vcg_signal.txt"

# Abrindo o arquivo e enviando para o servidor
with open(file_path, 'rb') as file:
    files = {'file': file}  # Nome do campo deve coincidir com o esperado pelo servidor
    response = requests.post(url, files=files)

# Exibindo a resposta do servidor
print("Status Code:", response.status_code)
try:
    print("Resposta JSON:", response.json())
except Exception as e:
    print("Resposta Texto:", response.text)