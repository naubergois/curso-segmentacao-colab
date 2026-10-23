"""Gera os notebooks do curso em notebooks/*.ipynb.

Com SOLUCOES=1, preenche os exercícios com as soluções (para testar a correção).
Com OUT=<pasta>, grava em outra pasta.
"""

import os
import re
from pathlib import Path

import nbformat as nbf

from comum import (
    FOTO_CANTEIRO,
    FOTO_ENFERMARIA,
    FOTO_OPERARIOS,
    HELPERS,
    INSTALL,
    VIDEO_OBRA,
    badge,
    novo_notebook,
)
from exercicios import EXERCICIOS, celulas_exercicios, id_exercicio

OUT = Path(os.environ.get("OUT", Path(__file__).parent / "notebooks"))
SOLUCOES = os.environ.get("SOLUCOES") == "1"


def notebook(nome, celulas):
    nb = novo_notebook()
    if nome in EXERCICIOS:
        celulas = celulas[:-1] + celulas_exercicios(EXERCICIOS[nome], SOLUCOES) + celulas[-1:]
    out = []
    for tipo, texto in celulas:
        texto = texto.strip("\n")
        texto = texto.replace("{BADGE}", badge(f"notebooks/{nome}"))
        if tipo == "md":
            cel = nbf.v4.new_markdown_cell(texto)
            ex = re.match(r"### Exercício (\d+)\.", texto)
            if ex:
                cel.metadata["id"] = id_exercicio(nome, int(ex.group(1)))
            out.append(cel)
        else:
            cel = nbf.v4.new_code_cell(texto)
            if tipo == "form":
                cel.metadata["cellView"] = "form"
            out.append(cel)
    nb.cells = out
    OUT.mkdir(exist_ok=True)
    nbf.write(nb, OUT / nome)
    print("ok", nome)


# ---------------------------------------------------------------- 01
notebook("01-segmentacao-em-imagem.ipynb", [
    ("md", """
{BADGE}

# 1. Segmentação em uma imagem

Uma caixa diz onde o objeto está, mais ou menos. Num quarto de hospital, o retângulo do leito leva junto o chão, a cortina e um pedaço da parede. A segmentação devolve a forma: uma máscara com os pixels que são o leito.

O modelo é o `yolov8n-seg`, a versão nano de segmentação. Tem uns 7 MB, roda sem GPU e conhece as 80 classes do COCO. Leito e cadeira estão nessa lista. Uma lesão, um órgão ou uma trinca no concreto, não. A caixa continua vindo. Junto com ela, vem a máscara.

> No Colab: **Ambiente de execução → Executar tudo**. GPU é opcional aqui.
"""),
    ("code", INSTALL),
    ("code", HELPERS),
    ("md", """
## Carregar o modelo e a foto

Na primeira chamada, `YOLO("yolov8n-seg.pt")` baixa os pesos. A foto é um quarto de hospital, com dois leitos e cadeiras.
"""),
    ("code", f'''import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

model = YOLO("yolov8n-seg.pt")
imagem = baixar("{FOTO_ENFERMARIA}", "enfermaria.jpg")'''),
    ("md", """
## Rodar a segmentação

`model(imagem)` devolve um resultado por foto. `plot()` desenha a caixa e pinta a máscara. `mascaras_originais` estica cada máscara de volta ao tamanho da foto, porque a rede responde numa grade menor.
"""),
    ("code", '''resultado = model(imagem, verbose=False)[0]
mascaras = mascaras_originais(resultado)

plt.figure(figsize=(8, 10))
plt.imshow(resultado.plot()[:, :, ::-1])  # BGR -> RGB
plt.axis("off")
plt.show()
print(f"{len(mascaras)} máscaras, foto {mascaras.shape[1]}x{mascaras.shape[2]}")
assert len(mascaras) > 0'''),
    ("md", """
## Ler a máscara como dado

Cada máscara é uma grade de verdadeiro ou falso, na mesma ordem das caixas. Somar os `True` dá a área em pixels. A confiança continua na caixa.
"""),
    ("code", '''areas = mascaras.sum(axis=(1, 2))
for i, caixa in enumerate(resultado.boxes):
    classe = model.names[int(caixa.cls)]
    conf = float(caixa.conf)
    print(f"{classe:10s} {conf:5.0%}  {int(areas[i]):7d} pixels")'''),
    ("md", """
## A caixa é maior que o objeto

A área da máscara dividida pela área da caixa mostra quanto do retângulo é objeto de verdade. No leito, uma parte da caixa é chão e cortina.
"""),
    ("code", '''for i, caixa in enumerate(resultado.boxes):
    x1, y1, x2, y2 = caixa.xyxy[0].tolist()
    area_caixa = (x2 - x1) * (y2 - y1)
    fracao = float(areas[i]) / area_caixa
    print(f"{model.names[int(caixa.cls)]:10s}  máscara/caixa = {fracao:.0%}")'''),
    ("md", """
## O que fica

A máscara é um array. Dá para contar pixel, recortar e medir. O que ela ainda não faz sozinha é lembrar do mesmo objeto no quadro seguinte: cada foto é uma conta nova.

Para experimentar com uma foto sua, troque a URL em `baixar(...)` ou suba o arquivo pelo painel lateral do Colab.
"""),
])

# ---------------------------------------------------------------- 02
notebook("02-segmentacao-em-video.ipynb", [
    ("md", """
{BADGE}

# 2. Segmentação quadro a quadro

Vídeo é uma sequência de fotos. O laço lê o quadro, roda o modelo, desenha e grava. A diferença é o que se conta. Um operário que atravessa a obra gera uma detecção por quadro, mas a pergunta melhor é quantos pixels a pessoa ocupa.

O clipe é uma obra de rodovia: gente de colete e máquinas no aterro. Dura uns 24 segundos. Aqui são 80 quadros, para caber em CPU.

A escavadeira não está nas 80 classes. O nome que volta costuma ser `train` ou `truck`. A conta de pixels continua valendo, com o nome que o modelo conhece.

> GPU deixa bem mais rápido: **Ambiente de execução → Alterar o tipo de ambiente → T4 GPU**.
"""),
    ("code", INSTALL),
    ("code", HELPERS),
    ("code", f'''from collections import Counter

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")
video = baixar(
    "{VIDEO_OBRA}",
    "obra.mp4",
)'''),
    ("md", """
## Ler, segmentar, gravar

`r.plot()` já pinta as máscaras. Em paralelo, somamos os pixels de cada classe e guardamos os nomes que apareceram em cada quadro.
"""),
    ("code", '''MAX_QUADROS = 80

cap = cv2.VideoCapture(video)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"{largura}x{altura} a {fps} FPS")

out = cv2.VideoWriter("obra_segmentada.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (largura, altura))
pixels = Counter()
classes_por_quadro = []
mascaras_por_quadro = []
quadros = 0

while quadros < MAX_QUADROS:
    ok, frame = cap.read()
    if not ok:
        break
    r = model(frame, verbose=False)[0]
    out.write(r.plot())
    nomes = []
    if r.masks is not None:
        for c, m in zip(r.boxes.cls.int().tolist(), mascaras_originais(r)):
            nome = model.names[c]
            nomes.append(nome)
            pixels[nome] += int(m.sum())
    classes_por_quadro.append(nomes)
    mascaras_por_quadro.append(len(nomes))
    quadros += 1

cap.release()
out.release()
print(f"{quadros} quadros processados")
assert quadros > 0'''),
    ("md", """
## Assistir o resultado
"""),
    ("code", 'web = mostrar_video("obra_segmentada.mp4")'),
    ("md", """
## Quem ocupa a imagem

O número de detecções trata um operário pequeno e uma máquina enorme como iguais. A soma de pixels não.
"""),
    ("code", '''for classe, n in pixels.most_common():
    print(f"{classe:16s} {n:8d} pixels")'''),
    ("md", """
## Baixar o vídeo
"""),
    ("code", "baixar_para_maquina(web)"),
    ("md", """
## O que fica

Segmentar vídeo é o mesmo laço da detecção, com uma conta a mais: a área. Para desenhar só uma classe, passe `classes=[indice]` na chamada do modelo. O índice está em `model.names`.
"""),
])

# ---------------------------------------------------------------- 03
notebook("03-medir-a-mascara.ipynb", [
    ("md", """
{BADGE}

# 3. Medir a máscara

A máscara pintada na foto é boa de olhar. Para usar num sistema, ela precisa virar número: que fração da imagem o objeto cobre, onde fica o centro, o quanto a caixa sobra, se duas máscaras se encostam.

Tudo isso é conta de array. A foto é de dois operários na obra, de capacete e picareta. A caixa do operário da frente leva a ferramenta, a lama e um pedaço do céu. A máscara acompanha o corpo.
"""),
    ("code", INSTALL),
    ("code", HELPERS),
    ("code", f'''import numpy as np
import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt

model = YOLO("yolov8n-seg.pt")
imagem = baixar("{FOTO_OPERARIOS}", "operarios.jpg")
resultado = model(imagem, verbose=False)[0]
mascaras = mascaras_originais(resultado)
print(f"{{len(mascaras)}} máscaras")'''),
    ("md", """
## Porcentagem da foto

A média de uma máscara booleana é a fração de pixels `True`. Vezes 100, vira porcentagem.
"""),
    ("code", '''for i, caixa in enumerate(resultado.boxes):
    pct = float(mascaras[i].mean()) * 100
    print(f"{model.names[int(caixa.cls)]:10s} cobre {pct:5.1f}% da foto")'''),
    ("md", """
## O centro

O centro da máscara é a média das posições onde ela é `True`. `np.where` devolve as linhas e as colunas. A coluna é o x.
"""),
    ("code", '''foto = cv2.imread(imagem)
for i, caixa in enumerate(resultado.boxes):
    ys, xs = np.where(mascaras[i])
    cx, cy = int(round(xs.mean())), int(round(ys.mean()))
    cv2.circle(foto, (cx, cy), 8, (0, 255, 255), -1)
    print(f"{model.names[int(caixa.cls)]:10s} centro ({cx}, {cy})")

plt.figure(figsize=(8, 10))
plt.imshow(foto[:, :, ::-1])
plt.axis("off")
plt.show()'''),
    ("md", """
## IoU entre máscara e caixa

O IoU é a interseção dividida pela união. Aqui um dos lados é a máscara e o outro é o retângulo da caixa, pintado num array do mesmo tamanho. Se o IoU fica longe de 1, a caixa inclui bastante fundo.
"""),
    ("code", '''for i, caixa in enumerate(resultado.boxes):
    caixa_cheia = np.zeros(mascaras.shape[1:], dtype=bool)
    x1, y1, x2, y2 = map(int, caixa.xyxy[0].tolist())
    caixa_cheia[y1:y2, x1:x2] = True
    inter = np.logical_and(mascaras[i], caixa_cheia).sum()
    uniao = np.logical_or(mascaras[i], caixa_cheia).sum()
    print(f"{model.names[int(caixa.cls)]:10s} IoU máscara/caixa = {float(inter / uniao):.2f}")'''),
    ("md", """
## Quem encosta em quem

Dois objetos se tocam quando algum pixel é `True` nas duas máscaras. Na foto dos operários, a conta diz se os corpos se encontram.
"""),
    ("code", '''n = len(mascaras)
for i in range(n):
    for j in range(i + 1, n):
        if np.any(mascaras[i] & mascaras[j]):
            a = model.names[int(resultado.boxes.cls[i])]
            b = model.names[int(resultado.boxes.cls[j])]
            print(f"{a} encosta em {b}")'''),
    ("md", """
## O que fica

Área, centro, IoU e sobreposição saem da mesma grade de verdadeiro ou falso. Isso ainda não desenha uma classe sua: o modelo só conhece as 80 classes do COCO. Uma classe nova pede fotos com o contorno marcado.
"""),
])

# ---------------------------------------------------------------- 04
notebook("04-treinar-segmentacao.ipynb", [
    ("md", """
{BADGE}

# 4. Treinar a segmentação

O modelo pronto desenha pessoa, leito, cadeira e caminhão. Para desenhar uma trinca no concreto ou o contorno de uma estrutura numa foto clínica, o treino precisa de fotos em que o contorno já foi marcado.

O rótulo deixa de ser um retângulo. Cada objeto vira um polígono: a classe, e depois os pontos do contorno, todos entre 0 e 1.

O dataset pequeno é o `coco8-seg`: quatro fotos de treino e quatro de validação, já no formato certo. Serve para ver o processo. Ele não é um conjunto de hospital nem de canteiro. Um modelo bom pede centenas de contornos por classe.

> Aqui a GPU faz diferença: **Ambiente de execução → Alterar o tipo de ambiente → T4 GPU**.
"""),
    ("code", INSTALL),
    ("code", HELPERS),
    ("md", """
## Como é um rótulo de segmentação

Uma linha por objeto. O primeiro número é a classe. O resto são pares `x y` do polígono. Uma caixa teria cinco números no total. Um contorno tem bem mais.
"""),
    ("code", '''from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from ultralytics import YOLO
from ultralytics.utils import DATASETS_DIR

model = YOLO("yolov8n-seg.pt")'''),
    ("md", """
## Treinar

A chamada é a mesma do treino de detecção. Muda o peso inicial (`yolov8n-seg.pt`) e o yaml (`coco8-seg.yaml`). Três épocas com imagens de 320 px bastam para aparecer um `results.csv`. Não bastam para um modelo bom.
"""),
    ("code", '''treino = model.train(
    data="coco8-seg.yaml",
    epochs=3,
    imgsz=320,
    batch=4,
    project="runs",
    name="coco8seg",
    exist_ok=True,
    plots=False,
    verbose=False,
)
pasta = Path(treino.save_dir)
print("Resultados em", pasta)'''),
    ("md", """
## O que o arquivo de rótulos tem
"""),
    ("code", '''rotulo = sorted((DATASETS_DIR / "coco8-seg" / "labels" / "train").glob("*.txt"))[0]
linha = rotulo.read_text().splitlines()[0].split()
print(rotulo.name)
print(f"classe {linha[0]}, { (len(linha) - 1) // 2 } pontos no polígono")
print(" ".join(linha[:13]), "...")'''),
    ("md", """
## A perda da máscara

Além da perda da caixa e da classe, o treino de segmentação tem `train/seg_loss`: o quanto o contorno previsto errou o contorno marcado. Com quatro fotos, a curva oscila. O que importa é saber em qual coluna ela mora.
"""),
    ("code", '''df = pd.read_csv(pasta / "results.csv")
df.columns = df.columns.str.strip()
colunas = ["epoch", "train/box_loss", "train/seg_loss", "train/cls_loss", "metrics/mAP50(M)"]
print(df[colunas].to_string(index=False))

plt.figure(figsize=(8, 3))
plt.plot(df["epoch"], df["train/seg_loss"], label="seg_loss")
plt.plot(df["epoch"], df["train/box_loss"], label="box_loss")
plt.xlabel("época")
plt.legend()
plt.grid(True)
plt.show()'''),
    ("md", """
## Usar o modelo treinado

O melhor peso fica em `weights/best.pt`. Ele carrega igual ao modelo original e devolve máscara do mesmo jeito.
"""),
    ("code", f'''melhor = YOLO(pasta / "weights" / "best.pt")
r = melhor("{FOTO_CANTEIRO}", verbose=False)[0]
plt.figure(figsize=(6, 8))
plt.imshow(r.plot()[:, :, ::-1])
plt.axis("off")
plt.show()
print(0 if r.masks is None else len(r.masks), "máscaras")'''),
    ("md", """
## Para treinar com as suas fotos

1. Marque o contorno no [Roboflow](https://roboflow.com) ou no [CVAT](https://www.cvat.ai) e exporte em **YOLOv8 Segmentation**.
2. Suba o `.zip` no Colab e descompacte.
3. Troque `data="coco8-seg.yaml"` pelo `data.yaml` do seu dataset e suba `epochs` para 50 ou mais.

O processo é o mesmo. Mudam o tamanho do dataset e o tempo de treino. Quatro fotos ensinam o caminho, e erram o contorno.
"""),
])
