## Dados numéricos 
1. Dados numéricos (inteiros e floats)
%pip install pandas
%pip install numpy
%pip install scikit-learn 
%pip install matplotlib

2. Importar as bibliotecas
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.pipeline import Pipeline 
from matplotlib.pyplot as plt

3. 
np.random.seed(42)

# Gerar dataset com 15 linhas e 3 colunas
df_numeric = pd.DataFrame({
    'inteiros': np.random.randint(low=0, high=100, size=15),
    'float': np.random.randn(15) * 10 + 50,
    'faltantes': [np.nan if i%4 == 0 else np.random.randn()*5 for i in range(15)]
})

# Gerar informações
print('Dataframe original: ')
df_numeric.head(15)

df_numeric.describe()


# Imputação dos dados na coluna de faltantes
df_numeric['faltantes'] = df_numeric['faltantes'].fillna(df_numeric['faltantes'].mean())

print('Dataframe após imputação: ')
df_numeric.head(5)

# Padronizar os dados
scaler = StandardScaler()

# Padronizar os dados
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns)

print('Dataframe após padronização: ')
df_scaled.head(5)

# 2. DADOS CATEGÓRICOS
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
categorias = pd.DataFrame({
    'cor': ['vermelho', 'amarelo', 'azul', 'verde'], 
    'tamanho': ['p', 'M', 'G', 'P', 'M']
})

print('Dados categoricos')
categorias.head(5)

ohe = OneHotEncoder(sparse_output=False)
categorias_ohe = pd.DataFrame(ohe.fit_transform(categorias), columns=ohe.get_feature_names_out())
print('Dados categorias apos OneHotEnconder: ')
categorias_ohe.head(5)

# Preparação dos dados para ML
from sklearn.compose import ColumnTransformer 

# Combinar os dataframes
df_full = pd.concat([df_numeric.reset_index(drop=True),
                     categorias.reset_index(drop=True)], axis=1
                     )

# Dados originais sem pre-processamento
df_full.head(5)

preprocessor = ColumnTransformer(
    [
        ('num', StandardScaler(), ['inteiros', 'floats', 'faltantes']),
        ('cat', OneHotEncoder(sparse_output=False), ['cor', 'tamanho'])
    ]
)


# 3. DADOS DE IMAGENS
from PIL import Image, ImageDraw
img = Image.new('RGB', (200, 200), color='white')
draw = ImageDraw.Draw(img)
draw.rectangle((50, 50, 150, 150), fill='blue')
draw.ellipse((75, 75, 125, 125), fill='red')


# Redimensionar essa imagem 
img_resized = img.resize((64, 64))
img_array = np,array(img_resized) / 255


plt.figure(figsize=(8,3))
plt.subplot(1,3,1)
plt.imshow(img)
plt.title('Imagem Original')
plt.subplot(1,3,2)
plt.imshow(img_resized)
plt.title('Imagem Redimensionada')
plt.show()
plt.subplot(1,3,3)
plt.imshow(img_array)
plt.title('Array da imagem')
plt.show()

# O que ela está fazendo aqui? 

hist_r = np.histogram(img_array[:,:,0], bins=16, range=(0,1))[0]
hist_g = np.histogram(img_array[:,:,1], bins=16, range=(0,1))[0]
hist_b = np.histogram(img_array[:,:,2], bins=16, range=(0,1))[0]

color_features = np.concatenate([hist_r, hist_g, hist_b])
print(f"Features extraídas: {len(color_features)} dimensões")
print("Exemplo de features: ")
print(color_features[:5])

img_flat = img.array.flatten()
print(f"Features extraídas: {len(img_flat)} dimensões")
print("Exemplo de features: ")
print(img_flat[:5])

# salvar os dados
features_df = pd.DataFrame({
   [color_features]
})

features_df.to_csv('dados_estruturados.csv', index=False)

## 4. Dados de aúdio
%pip install librosa

import librosa
from scipy.io.wavfile import write 

# Criar dados sintéticos
sr = 20050
duration = 3 
t = np.linspace(0, duration, int(sr * duration))

# Sinal composto (44oHz + 880Hz )
audio_signal = 0.5 * np.sin(2 * np.pi*440*t) + 0.3 * np.sin(2 * np.pi*880*t)
audio_signal
audio_signal = (audio_signal * 32767).astype(np.int16)

# Salvar como WAV
write('audio_signal.wav', sr, audio_signal)
print(f"Áudio criado: {duration} s, {sr} Hz")


# Espectrograma

# Carregar o áudio
y, sr_loaded = librosa.load('audio_signal.wav')

plt.figure(figsize=(12,4))
plt.subplot(1,2,1)
librosa.display.waveshow(y, sr=sr_loaded)
plt.title('Sinal de áudio')

plt.subplot(1,2,2)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref = np.max)
librosa.display.specshow(D, sr=sr_loaded, x_axis='time', y_axis='hz')
plt.title('Espectrograma')
plt.tight_layout()
plt.show()

mfccs = librosa.feature.mfcc(y=y, sr=sr_loaded, n_mfcc=13)

# Calcular estatísticas
mfccs_mean = np.mean(mfccs, axis=1)
mfccs_std = np.std(mfccs, axis=1)
mfccs_features = np.concatenate([mfccs_mean, mfccs_std])

print(f"Features extraídas: {len(mfccs_features)} dimensões")

print("Exemplo de feature: ")
mfccs_features[:5]


## 5. Dados de vídeos 
%pip instal opencv-python

import cv2

# Criar vídeo sintético
fourcc = cv2.VideoWriter_fourcc(*'.mp4')
video_writer = cv2.VideoWriter('video_synthetic.mp4', fourcc, 10.0, (200, 200))

# criando
import cv2

# Criar vídeo sintético
fourcc = cv2.VideoWriter_fourcc(*'.mp4')
video_writer = cv2.VideoWriter('video_synthetic.mp4', fourcc, 10.0, (200, 200))

# Montar frames 
frames_data = []
for i in range(30):
  # Criar um frame colorido
  frame = np.zeros((200,200,3), dtype=np.uint8)

  # Círculo que se move 
  center_x = int(100+50 * np.sin(i*0.2))
  center_y = int(100+30 * np.cos(i*0.2))

  cv2.circle(frame, (center_x, center_y), 20, (0,255,255-i*8), -1)
  cv2.rectangle(frame, (50,50), (150,150), (255,0,i*8), 2)
  
  frames_data.append(frame.copy())
  video_writer.write(frame)

video_writer.release()
print('Vídeo criado com 30 frames e 10 FPS')

# Extrair alguns frames
plt.figure(figsize=(12,3))
for i, idx in enumerate([0, 10, 20]):
    plt.subplot(1,3, i+1)
    plt.imshow(cv2.cvtColor(frames_data[idx], cv2.COLOR_BGR2RGB))
    plt.title(f'Frame {idx}')
plt.show()

# Extrair features de cada frame
video_features = []
for frame in frames_data[::5]:
  hist = cv2.calcHist([frame], [0,1,2], None, [8,8,8], [0, 256, 0, 256, 0, 256])
  hist_normalized = hist.flatten() / hist.sum()
  video_features.append(hist_normalized)
video_features = np.array(video_features)
print(f"Features extraídas: {video_features.shape[1]} dimensões")  

# Média ao longo do tempo
temporal_mean = np.mean(video_features, axis=0)
temporal_std = np.std(video_features, axis=0)
temporal_features = np.concatenate([temporal_mean, temporal_std])
print(f"Features extraídas: {len(temporal_features)} dimensões")

# Salvar features
video_features_df = pd.DataFrame(video_features)
video_features_df.to_csv('dados_estruturados.csv', index=False)


1. um agente para procurar no banco de dados e trazer a resposta
2. trazer o texto em mql 
3. outro agente que vai procurar 