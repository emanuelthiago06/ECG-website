import numpy as np
import pandas as pd
import os
from PIL import Image

from src.signal.Read import Read
from src.signal.Signal import VCG
from src.filter.Filter import Filter
from src.processing.Convert import Convert
from src.processing.SignalProcess import SignalProcess
from src.display.Display import Display
from keras.utils import custom_object_scope
from tensorflow_addons.metrics import F1Score
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model

from tensorflow.keras.losses import BinaryCrossentropy

# Definir a função de perda
loss_fn = BinaryCrossentropy()


def make_vcg_signal(v1, v2, v3):
    if len(v1) != len(v2) or len(v1) != len(v3):
        raise ValueError("Os sinais v1, v2 e v3 devem ter o mesmo comprimento.")
    
    # Empilhar os sinais como colunas
    vcg_signal = np.column_stack((v1, v2, v3))
    return vcg_signal

def make_vcg_from_signal(arr):
    header = {'fs': 500}
    vcg = VCG(arr, 'paciente', header, 'kors')
    return vcg


def processVCG(vcg, n_samples_to_delay):
    try:

        # PRO CASO DE USAR APENAS UMA PARTE DE UM CICLO
        # inferior_slice_lim = 50
        # superior_slice_lim = 300

        # PRO CASO DE USAR APENAS UMA PARTE DE UM CICLO
        # if signalOfCycle.shape[0] != superior_slice_lim - inferior_slice_lim:
        #     return
        variables = {
            0: "x",
            1: "y",
            2: "z"
        }
        count = 0
        errors_list_position = []
        tau = 1
        vcg_leads_reconstructed = []
        vcgLeadsOfCycleRPS = np.zeros(
        (vcg.signal.shape[0] - n_samples_to_delay*tau, 2))
        for vcg_lead in range(vcg.signal.shape[1]):
            vcgLeadsOfCycleRPS[:, :] = SignalProcess.reconstructPhaseSpace(vcg.signal[:, vcg_lead], n_samples_to_delay*tau)
            Display(vcgLeadsOfCycleRPS, (2.24, 2.24), [-1, 2, -1, 2]).save_RPS_image(f'vcg_img_{variables[vcg_lead]}.png', 'off')
    except:
        errors_list_position.append(count)

def generate_image_from_vcg(v1,v2,v3):
    vcg_signal = make_vcg_signal(v1, v2, v3)
    vcg = make_vcg_from_signal(vcg_signal)

    FIGSIZE = (2.24, 2.24)
    PLOT_LIMS = [-1, 2, -1, 2]  # 0.15 antes

    HOME = HOME = os.path.expanduser('~')
    #Normalize the VCG
    max_value = np.max(np.abs(vcg.signal))
    vcg.signal = vcg.signal / max_value

    time_delay_seconds = 0.01
    n_samples_to_delay = int(time_delay_seconds*vcg.samplingFreq)

    processVCG(vcg, n_samples_to_delay)
    
    # Carrega as imagens em escala de cinza
    img_r = Image.open("vcg_img_x.png").convert('L')  # L -> grayscale (um canal)
    img_g = Image.open("vcg_img_y.png").convert('L')
    img_b = Image.open("vcg_img_z.png").convert('L')
    
    # Converter as imagens para arrays numpy
    r, g, b = np.array(img_r), np.array(img_g), np.array(img_b)

    r[r == 0] = 19
    r[r >= 247] = 0
    r[r != 0] = 255

    g[g == 0] = 19
    g[g >= 247] = 0
    g[g != 0] = 255

    b[b == 0] = 19
    b[b >= 247] = 0
    b[b != 0] = 255

    # Criar uma nova imagem RGB com fundo preto
    new_img_array = np.zeros((r.shape[0], r.shape[1], 3), dtype=np.uint8)
    
    
    # Aplicar os canais de cor às imagens de entrada
    new_img_array[:, :, 0] = r   # Canal vermelho
    new_img_array[:, :, 1] = g   # Canal verde
    new_img_array[:, :, 2] = b   # Canal azul
    
    return new_img_array

data = np.loadtxt('vcg_signal.txt', delimiter='\t', skiprows=1)  # Ignora a linha do cabeçalho

# Separando cada coluna
v1 = data[:, 0]  # Primeira coluna
v2 = data[:, 1]  # Segunda coluna
v3 = data[:, 2]  # Terceira coluna

new_img_array = generate_image_from_vcg(v1, v2, v3)


def classify_img(img):

    # Carregar o modelo treinado
    with custom_object_scope({'Addons>F1Score': F1Score}):
        model = load_model('/home/emanuel/Documents/ECG-website/src/modelo_treinado.h5')

    # Converter a matriz para um formato de imagem, se necessário
    image = Image.fromarray(img)

    # Redimensionar a imagem para o tamanho que o modelo espera (exemplo: 224x224)
    image = image.resize((224, 224))  # Substitua por (tamanho_x, tamanho_y) esperado pelo modelo

    # Converter para array NumPy e normalizar
    image_array = np.array(image) / 255.0  # Normalizar para valores entre 0 e 1

    # Adicionar uma dimensão para representar o batch (o modelo espera entrada com formato [batch, altura, largura, canais])
    image_array = np.expand_dims(image_array, axis=0)

    # Fazer a previsão
    prediction = model.predict(image_array)

    # Exibir o resultado
    print("Previsão do modelo:", prediction)
    return prediction