"""Gera um notebook por exercício em exercicios/*.ipynb.

Cada notebook roda sozinho: instala, refaz o trecho da aula de que o exercício
precisa, mostra o enunciado, deixa uma célula para tentar e executa a solução
com a correção automática.
"""

import os
import re
import unicodedata
from pathlib import Path

import nbformat as nbf

from comum import HELPERS, INSTALL, badge, colab_url, novo_notebook
from exercicios import CONFERIR, EXERCICIOS

OUT = Path(os.environ.get("OUT", Path(__file__).parent / "exercicios"))

AULAS = {
    "01-segmentacao-em-imagem.ipynb": {
        "nome": "Segmentação em imagem",
        "install": INSTALL,
        "contexto": "A preparação carrega o YOLOv8 de segmentação e roda na foto do ônibus, como na aula 1. Ficam prontos `resultado` e `mascaras`.",
        "setup": '''import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

model = YOLO("yolov8n-seg.pt")
imagem = baixar("https://ultralytics.com/images/bus.jpg", "bus.jpg")
resultado = model(imagem, verbose=False)[0]
mascaras = mascaras_originais(resultado)

plt.figure(figsize=(6, 8))
plt.imshow(resultado.plot()[:, :, ::-1])
plt.axis("off")
plt.show()
print(len(mascaras), "máscaras")''',
    },
    "02-segmentacao-em-video.ipynb": {
        "nome": "Segmentação em vídeo",
        "install": INSTALL,
        "contexto": "A preparação baixa o vídeo da sala e segmenta os primeiros 80 quadros, como na aula 2. Ficam prontos `pixels`, `classes_por_quadro` e `mascaras_por_quadro`.",
        "setup": '''from collections import Counter

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")
video = baixar(
    "https://github.com/ultralytics/assets/releases/download/v0.0.0/home-objects-compressed.mp4",
    "sala.mp4",
)

MAX_QUADROS = 80
cap = cv2.VideoCapture(video)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
pixels = Counter()
classes_por_quadro = []
mascaras_por_quadro = []
quadros = 0
while quadros < MAX_QUADROS:
    ok, frame = cap.read()
    if not ok:
        break
    r = model(frame, verbose=False)[0]
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

print(f"{largura}x{altura} a {fps} FPS, {quadros} quadros")
print(pixels.most_common(3))''',
    },
    "03-medir-a-mascara.ipynb": {
        "nome": "Medir a máscara",
        "install": INSTALL,
        "contexto": "A preparação segmenta a foto do ônibus, como na aula 3. Ficam prontos `resultado` e `mascaras`, no tamanho da foto.",
        "setup": '''import numpy as np
import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt

model = YOLO("yolov8n-seg.pt")
imagem = baixar("https://ultralytics.com/images/bus.jpg", "bus.jpg")
resultado = model(imagem, verbose=False)[0]
mascaras = mascaras_originais(resultado)

plt.figure(figsize=(6, 8))
plt.imshow(resultado.plot()[:, :, ::-1])
plt.axis("off")
plt.show()
print(len(mascaras), "máscaras")''',
    },
    "04-treinar-segmentacao.ipynb": {
        "nome": "Treinar segmentação",
        "install": INSTALL,
        "contexto": "A preparação treina o YOLOv8-seg por três épocas no `coco8-seg`, como na aula 4. Ficam prontos o `df`, com as métricas de cada época, e o `melhor`, que é o modelo treinado.",
        "setup": '''from pathlib import Path

import pandas as pd
from ultralytics import YOLO
from ultralytics.utils import DATASETS_DIR

model = YOLO("yolov8n-seg.pt")
treino = model.train(
    data="coco8-seg.yaml", epochs=3, imgsz=320, batch=4,
    project="runs", name="coco8seg", exist_ok=True, plots=False, verbose=False,
)
pasta = Path(treino.save_dir)
df = pd.read_csv(pasta / "results.csv")
df.columns = df.columns.str.strip()
melhor = YOLO(pasta / "weights" / "best.pt")

print(df[["epoch", "train/box_loss", "train/seg_loss", "metrics/mAP50(M)"]].to_string(index=False))''',
    },
}


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


def lista_exercicios():
    """[(aula_nb, numero_aula, n, exercicio, nome_arquivo)] na ordem do curso."""
    saida = []
    for aula_nb, aula in EXERCICIOS.items():
        k = int(aula_nb[:2])
        for n, ex in enumerate(aula["lista"], start=1):
            saida.append((aula_nb, k, n, ex, f"aula{k}-exercicio{n}-{slug(ex['titulo'])}.ipynb"))
    return saida


def gerar():
    todos = lista_exercicios()
    OUT.mkdir(exist_ok=True)
    for i, (aula_nb, k, n, ex, arquivo) in enumerate(todos):
        info = AULAS[aula_nb]
        proximo = todos[i + 1] if i + 1 < len(todos) else None
        aula_url = colab_url(f"notebooks/{aula_nb}")

        if proximo:
            fecho = (f"Próximo: [Aula {proximo[1]}, exercício {proximo[2]}: {proximo[3]['titulo']}]"
                     f"({colab_url('exercicios/' + proximo[4])}).")
        else:
            fecho = "Esse foi o último dos 24. Agora é trocar a foto do ônibus por uma foto sua, com o contorno marcado."

        celulas = [
            ("md", f"""{badge('exercicios/' + arquivo)}

# Aula {k}, exercício {n}: {ex['titulo']}

{ex['enunciado'].strip()}

O exercício é da aula [{k}. {info['nome']}]({aula_url}), e este notebook roda sozinho. Use **Ambiente de execução → Executar tudo**: ele prepara os dados, deixa uma célula para você tentar e, no fim, mostra uma solução já conferida."""),
            ("code", info["install"]),
            ("code", HELPERS),
            ("md", f"## Preparação\n\n{info['contexto']}"),
            ("code", info["setup"]),
            ("form", "# @title Correção automática (rode, não precisa ler)\n"
                     + EXERCICIOS[aula_nb]["preparo"].strip("\n") + "\n" + CONFERIR),
            ("md", f"## Sua vez\n\n{ex['enunciado'].strip()}\n\n*Dica:* {ex['dica']}\n\n"
                   "Troque o `None` pela sua resposta e rode a célula."),
            ("code", f"{ex.get('inicio', '')}resposta = None\n\nconferir({n}, resposta)"),
            ("md", "## Uma solução\n\nCompare com o que você fez. Existem outros caminhos certos: o que vale é a `conferir` aprovar."),
            ("code", f"{ex['solucao'].strip()}\n\nconferir({n}, resposta)"),
            ("md", f"## O que fica\n\n{fecho}"),
        ]

        nb = novo_notebook()
        for tipo, texto in celulas:
            if tipo == "md":
                nb.cells.append(nbf.v4.new_markdown_cell(texto.strip("\n")))
            else:
                cel = nbf.v4.new_code_cell(texto.strip("\n"))
                if tipo == "form":
                    cel.metadata["cellView"] = "form"
                nb.cells.append(cel)
        nbf.write(nb, OUT / arquivo)
    print(f"{len(todos)} notebooks em {OUT}")


if __name__ == "__main__":
    gerar()
