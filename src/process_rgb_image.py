import os
from PIL import Image
import numpy as np

# Caminhos de origem e destino
source_dir = 'Results_Cycles_normalized'
dest_dir = source_dir + '_RGB_black'
count_errors = 0
splits = ['training', 'val']
# Certifique-se de que o diretório de destino exista
os.makedirs(dest_dir, exist_ok=True)

# Percorre as pastas de 'training' e 'val'

for label in ['0', '1']:
    label_dir = os.path.join(dataset_dir, label)
    
    # Percorre cada paciente (pastas como 00412_hr)
    for patient in os.listdir(label_dir):
        patient_dir = os.path.join(label_dir, patient)
        
        # Percorre cada ciclo dentro do paciente (pastas numeradas)
        for cycle in os.listdir(patient_dir):
            cycle_dir = os.path.join(patient_dir, cycle)
            try:
                # Caminhos das imagens R, G e B
                img_r_path = os.path.join(cycle_dir, 'RPS_x_tau001s.png')
                img_g_path = os.path.join(cycle_dir, 'RPS_y_tau001s.png')
                img_b_path = os.path.join(cycle_dir, 'RPS_z_tau001s.png')
                
                # Carrega as imagens em escala de cinza
                img_r = Image.open(img_r_path).convert('L')  # L -> grayscale (um canal)
                img_g = Image.open(img_g_path).convert('L')
                img_b = Image.open(img_b_path).convert('L')
                
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
                
                # Converter de volta para imagem PIL
                new_img = Image.fromarray(new_img_array)

                # Cria o caminho de saída para o ciclo
                output_dir = os.path.join(dest_dir, dataset_type, label, patient, cycle)
                os.makedirs(output_dir, exist_ok=True)
                
                # Salva a imagem combinada com fundo preto
                output_path = os.path.join(output_dir, 'RPS_combined.png')
                new_img.save(output_path)
                
            except Exception as e:
                print(f"Erro ao processar {dataset_type}/{label}/{patient}/{cycle_dir}: {e}")
                count_errors += 1

print("Imagens combinadas e salvas com sucesso!")
print(f"Erros: {count_errors}")
