"""Gera os notebooks do curso em notebooks/*.ipynb.

Com SOLUCOES=1, preenche os exercícios com as soluções (para testar a correção).
Com OUT=<pasta>, grava em outra pasta.
"""

import os
import re
from pathlib import Path

import nbformat as nbf

from comum import (
    CT_TORAX,
    FOTO_CANTEIRO,
    FOTO_ENFERMARIA,
    FOTO_OPERARIOS,
    HELPERS,
    INSTALL,
    RM_CABECA,
    VIDEO_OBRA,
    badge,
    novo_notebook,
)
from exercicios import EXERCICIOS, celulas_exercicios, id_exercicio

OUT = Path(os.environ.get("OUT", Path(__file__).parent / "notebooks"))
SOLUCOES = os.environ.get("SOLUCOES") == "1"


def notebook(nome, celulas):
    somente = os.environ.get("SOMENTE")
    if somente and nome not in somente.split(","):
        return
    nb = novo_notebook()
    if nome in EXERCICIOS:
        celulas = celulas[:-1] + celulas_exercicios(EXERCICIOS[nome], SOLUCOES) + celulas[-1:]
    out = []
    for tipo, texto in celulas:
        texto = texto.strip("\n")
        texto = texto.replace("{BADGE}", badge(f"notebooks/{nome}"))
        texto = texto.replace("{CT_TORAX}", CT_TORAX).replace("{RM_CABECA}", RM_CABECA)
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
## Um quadro, parado

O vídeo passa rápido. Este é o primeiro quadro, com a máscara já pintada. A caixa vem junto: o modelo devolve as duas coisas.
"""),
    ("code", '''import matplotlib.pyplot as plt

cap = cv2.VideoCapture(video)
ok, frame = cap.read()
cap.release()
quadro = model(frame, verbose=False)[0]
plt.figure(figsize=(8, 4.5))
plt.imshow(quadro.plot()[:, :, ::-1])
plt.axis("off")
plt.show()'''),
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

INSTALL_EXAME = "!pip install -q pynrrd"

# ---------------------------------------------------------------- 05
notebook("05-tomografia.ipynb", [
    ("md", """
{BADGE}

# 5. Tomografia

Uma tomografia não é uma foto de quarto. É uma pilha de cortes. Em cada corte, o número do pixel é densidade: osso claro, ar escuro, músculo no meio. A unidade usual é Hounsfield. Água fica perto de zero. Pulmão, bem abaixo. Osso, bem acima.

A máscara daqui não vem das 80 classes. Ela sai da densidade. O ar de fora do corpo não entra. Entra o ar que está dentro do tórax.

O volume é o CTChest, amostra pública do 3D Slicer. Tem uns 40 MB.

> No Colab: **Ambiente de execução → Executar tudo**. CPU chega.
"""),
    ("code", INSTALL_EXAME),
    ("code", HELPERS),
    ("code", '''import nrrd
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

arquivo = baixar("{CT_TORAX}", "ct-torax.nrrd")
volume, _cabecalho = nrrd.read(arquivo)
volume = volume.astype(np.float32)
print(f"{volume.shape[0]} x {volume.shape[1]} x {volume.shape[2]} cortes")
print(f"densidade de {volume.min():.0f} a {volume.max():.0f}")
assert volume.ndim == 3'''),
    ("md", """
## O corte com mais pulmão

Pulmão, neste número, é o que fica entre −950 e −400. O corte que mais tem desses pixels é o que a gente olha primeiro.
"""),
    ("code", '''def pixels_de_pulmao(fatia):
    return int(((fatia > -950) & (fatia < -400)).sum())

areas = [pixels_de_pulmao(volume[:, :, z]) for z in range(volume.shape[2])]
z = int(np.argmax(areas))
fatia = volume[:, :, z]
print(f"corte {z}, {areas[z]} pixels na faixa do pulmão")'''),
    ("md", """
## A janela

O olho não lê −1000 e 3000 ao mesmo tempo. A janela de pulmão espalha os cinzas em volta de −600. Osso estoura no branco. Ar de fora fica preto.
"""),
    ("code", '''def janela(img, centro, largura):
    baixo = centro - largura / 2
    alto = centro + largura / 2
    return np.clip((img - baixo) / (alto - baixo), 0, 1)

plt.figure(figsize=(6, 6))
plt.imshow(janela(fatia, -600, 1500), cmap="gray")
plt.axis("off")
plt.show()'''),
    ("md", """
## A máscara do pulmão

Primeiro o corpo: tudo mais denso que −300, com os buracos preenchidos. O pulmão é o buraco que voltou a ser ar, dentro desse corpo. O que encosta na borda da imagem é ar de fora, e sai.
"""),
    ("code", '''def mascara_pulmao(fatia):
    corpo = ndimage.binary_fill_holes(fatia > -300)
    pulmao = corpo & (fatia > -950) & (fatia < -400)
    pulmao = ndimage.binary_opening(pulmao, iterations=1)
    rotulo, n = ndimage.label(pulmao)
    borda = set(rotulo[0, :]) | set(rotulo[-1, :]) | set(rotulo[:, 0]) | set(rotulo[:, -1])
    borda.discard(0)
    for pedaco in borda:
        pulmao[rotulo == pedaco] = False
    return pulmao

pulmao = mascara_pulmao(fatia)
cor = plt.cm.gray(janela(fatia, -600, 1500))[..., :3]
cor[pulmao] = 0.55 * cor[pulmao] + 0.45 * np.array([0.2, 0.85, 0.35])
plt.figure(figsize=(6, 6))
plt.imshow(cor)
plt.axis("off")
plt.show()
print(f"o pulmão cobre {pulmao.mean() * 100:.1f}% deste corte")'''),
    ("md", """
## O osso no mesmo corte

Osso é o que passa de 300. A máscara é fina: vértebra, costela, escápula. Vaso e brônquio continuam de fora das duas máscaras, porque não são ar nem osso.
"""),
    ("code", '''osso = fatia > 300
cor = plt.cm.gray(janela(fatia, -600, 1500))[..., :3]
cor[osso] = 0.55 * cor[osso] + 0.45 * np.array([0.25, 0.65, 1.0])
plt.figure(figsize=(6, 6))
plt.imshow(cor)
plt.axis("off")
plt.show()
print(f"osso: {int(osso.sum())} pixels")'''),
    ("md", """
## Três alturas

O pulmão não tem o mesmo tamanho no alto e na base. Três cortes, com a mesma máscara, mostram a mudança.
"""),
    ("code", '''escolhidos = [z for z in (z - 20, z, z + 12) if 0 <= z < volume.shape[2]]
fig, eixos = plt.subplots(1, len(escolhidos), figsize=(12, 4))
for eixo, indice in zip(eixos, escolhidos):
    f = volume[:, :, indice]
    m = mascara_pulmao(f)
    img = plt.cm.gray(janela(f, -600, 1500))[..., :3]
    img[m] = 0.55 * img[m] + 0.45 * np.array([0.2, 0.85, 0.35])
    eixo.imshow(img)
    eixo.set_title(f"corte {indice}")
    eixo.axis("off")
plt.tight_layout()
plt.show()'''),
    ("md", """
## O que fica

A máscara do pulmão é uma conta de densidade. Vaso dentro do pulmão fica de fora, porque é tecido. Isso ainda não é um laudo, e não marca nódulo: um nódulo tem densidade de tecido e some no meio da máscara, ou nem entra nela.

O modelo das aulas 1 a 4 não lê este arquivo. Ele não tem classe para pulmão.
"""),
])

# ---------------------------------------------------------------- 06
notebook("06-ressonancia.ipynb", [
    ("md", """
{BADGE}

# 6. Ressonância

A ressonância também é uma pilha de cortes, mas o número não é densidade. É sinal. No mesmo cérebro, gordura, água e osso trocam de claro e escuro conforme o peso do exame. Aqui o crânio fica escuro e o cérebro, cinza.

A máscara é o maior bloco acima de um corte de intensidade. No corte de lado, esse bloco é o cérebro, e o rosto fica de fora. Não é substância branca contra cinzenta. É o tecido contra o fundo.

O volume é o MRHead, doado ao 3D Slicer para uso sem restrição. Tem uns 7 MB.

> No Colab: **Ambiente de execução → Executar tudo**. CPU chega.
"""),
    ("code", INSTALL_EXAME),
    ("code", HELPERS),
    ("code", '''import nrrd
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

arquivo = baixar("{RM_CABECA}", "rm-cabeca.nrrd")
volume, _cabecalho = nrrd.read(arquivo)
volume = volume.astype(np.float32)
print(f"{volume.shape[0]} x {volume.shape[1]} x {volume.shape[2]}")
print(f"sinal de {volume.min():.0f} a {volume.max():.0f}")
assert volume.ndim == 3'''),
    ("md", """
## Dois jeitos de cortar a mesma cabeça

Um corte atravessa os olhos. O outro mostra a cabeça de lado, com o cerebelo embaixo. Os dois saem do mesmo volume. Muda o eixo.
"""),
    ("code", '''def cinza(img):
    baixo, alto = np.percentile(img, [1, 99])
    return np.clip((img - baixo) / (alto - baixo + 1e-6), 0, 1)

axial = volume[:, volume.shape[1] // 2, :]
sagital = volume[:, :, volume.shape[2] // 2]

fig, eixos = plt.subplots(1, 2, figsize=(8, 5))
eixos[0].imshow(cinza(axial), cmap="gray")
eixos[0].set_title("pelos olhos")
eixos[1].imshow(cinza(sagital), cmap="gray")
eixos[1].set_title("de lado")
for eixo in eixos:
    eixo.axis("off")
plt.tight_layout()
plt.show()'''),
    ("md", """
## A máscara no corte de lado

O fundo é quase zero. O que passa de um patamar vira candidato. A abertura come a borda fininha. O maior pedaço que sobra é o cérebro. Olho e pele, quando se separam, ficam de fora.
"""),
    ("code", '''def mascara_tecido(fatia):
    vivos = fatia[fatia > 5]
    patamar = np.percentile(vivos, 40) if len(vivos) else 0
    mascara = fatia > patamar
    mascara = ndimage.binary_opening(mascara, iterations=2)
    mascara = ndimage.binary_fill_holes(mascara)
    rotulo, n = ndimage.label(mascara)
    if n == 0:
        return mascara
    tamanhos = ndimage.sum(np.ones_like(rotulo), rotulo, range(1, n + 1))
    return rotulo == (1 + int(np.argmax(tamanhos)))

cerebro = mascara_tecido(sagital)
cor = plt.cm.gray(cinza(sagital))[..., :3]
cor[cerebro] = 0.55 * cor[cerebro] + 0.45 * np.array([0.85, 0.65, 0.25])
plt.figure(figsize=(6, 6))
plt.imshow(cor)
plt.axis("off")
plt.show()
print(f"o maior bloco cobre {cerebro.mean() * 100:.1f}% do corte de lado")'''),
    ("md", """
## O corte dos olhos

A mesma conta, agora no corte que atravessa os olhos. O patamar sobe um pouco, para o cinza do cérebro não grudar na pele. O que a máscara pega aqui é o miolo da cabeça, não o crânio.
"""),
    ("code", '''def mascara_miolo(fatia):
    mascara = (fatia > 35) & (fatia < 120)
    mascara = ndimage.binary_opening(mascara, iterations=1)
    mascara = ndimage.binary_closing(mascara, iterations=2)
    mascara = ndimage.binary_fill_holes(mascara)
    rotulo, n = ndimage.label(mascara)
    borda = set(rotulo[0, :]) | set(rotulo[-1, :]) | set(rotulo[:, 0]) | set(rotulo[:, -1])
    borda.discard(0)
    for pedaco in borda:
        mascara[rotulo == pedaco] = False
    rotulo, n = ndimage.label(mascara)
    if n == 0:
        return mascara
    tamanhos = ndimage.sum(np.ones_like(rotulo), rotulo, range(1, n + 1))
    return rotulo == (1 + int(np.argmax(tamanhos)))

miolo = mascara_miolo(axial)
cor = plt.cm.gray(cinza(axial))[..., :3]
cor[miolo] = 0.55 * cor[miolo] + 0.45 * np.array([0.2, 0.75, 0.4])
plt.figure(figsize=(6, 6))
plt.imshow(cor)
plt.axis("off")
plt.show()
print(f"miolo: {miolo.mean() * 100:.1f}% do corte")'''),
    ("md", """
## O que fica

Tomografia separa pelo peso do pixel. Ressonância separa pelo sinal, e o número muda se o exame for outro peso. As duas máscaras são conta de limiar. Nenhuma das duas lê um laudo, e nenhuma separa lesão de tecido sadio.

Para uma lesão virar classe, alguém marca o contorno em muitos exames. Aí o treino da aula 4 passa a ter o que aprender.
"""),
])
