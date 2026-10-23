"""Exercícios com correção automática, seis por aula.

Cada exercício tem enunciado, dica, solução e uma verificação que calcula a
resposta esperada a partir dos dados do próprio notebook.
"""

CONFERIR = '''
_acertos = {}


def conferir(n, resposta):
    if resposta is None:
        print(f"Exercício {n}: ainda sem resposta.")
        return
    try:
        certo = bool(VERIFICAR[n](resposta))
    except Exception as erro:
        certo = False
        print(f"  (a verificação deu erro: {erro})")
    _acertos[n] = certo
    print(f"Exercício {n}: " + ("✅ certo!" if certo else "❌ ainda não. Releia o enunciado e tente de novo."))


def placar():
    print(f"{sum(_acertos.values())} de {len(VERIFICAR)} exercícios certos.")
'''


def id_exercicio(notebook, n):
    """Id da célula do enunciado, usado nos links #scrollTo= do Colab."""
    return f"exercicio-{notebook[:2]}-{n}"


def celulas_exercicios(aula, solucoes=False):
    celulas = [
        ("md", """
## Exercícios

Seis perguntas sobre o que acabou de rodar. Escreva a resposta na variável `resposta` e rode a célula: a função `conferir` diz na hora se está certo. Se travar, abra **Ver solução**.

Rode antes a célula de preparação abaixo. Ela só carrega as verificações.
"""),
        ("form", "# @title Preparação dos exercícios (rode, não precisa ler)\n" + aula["preparo"].strip("\n") + "\n" + CONFERIR),
    ]
    for n, ex in enumerate(aula["lista"], start=1):
        solucao = ex["solucao"].strip("\n")
        celulas.append(("md", f"""
### Exercício {n}. {ex["titulo"]}

{ex["enunciado"].strip()}

<details>
<summary>Ver solução</summary>

```python
{solucao}
```

</details>
"""))
        corpo = solucao if solucoes else f"# Dica: {ex['dica']}\n{ex.get('inicio', '')}resposta = None"
        celulas.append(("code", f"{corpo}\n\nconferir({n}, resposta)"))
    celulas.append(("code", "placar()"))
    return celulas


AULA1 = {
    "preparo": '''
import numpy as np

_cls = resultado.boxes.cls.int().tolist()
_conf = resultado.boxes.conf.tolist()
_xyxy = resultado.boxes.xyxy.tolist()


def _indices(nome):
    return [i for i, c in enumerate(_cls) if model.names[c] == nome]


def _i_onibus():
    return max(_indices("bus"), key=lambda i: (_xyxy[i][2] - _xyxy[i][0]) * (_xyxy[i][3] - _xyxy[i][1]))


def _fracao_onibus():
    uniao = np.any(mascaras[_indices("bus")], axis=0)
    return float(uniao.mean())


VERIFICAR = {
    1: lambda r: int(r) == len(mascaras),
    2: lambda r: set(r) == {model.names[c] for c in _cls},
    3: lambda r: abs(float(r) - max(_conf)) < 1e-3,
    4: lambda r: int(r) == int(mascaras.sum(axis=(1, 2)).max()),
    5: lambda r: int(r) == len(model(imagem, classes=[0], verbose=False)[0].masks),
    6: lambda r: abs(float(r) - _fracao_onibus()) < 1e-3,
}
''',
    "lista": [
        {
            "titulo": "Quantas máscaras",
            "enunciado": "Quantas máscaras o modelo devolveu em `mascaras`?",
            "dica": "len(mascaras) é o número de objetos segmentados.",
            "solucao": "resposta = len(mascaras)",
        },
        {
            "titulo": "Classes com máscara",
            "enunciado": "Monte um conjunto (`set`) com os **nomes** das classes que ganharam máscara.",
            "dica": "model.names traduz o índice que está em resultado.boxes.cls.",
            "solucao": "resposta = {model.names[int(c)] for c in resultado.boxes.cls}",
        },
        {
            "titulo": "A máscara mais segura",
            "enunciado": "Qual é a maior confiança entre as máscaras? Responda com um número entre 0 e 1.",
            "dica": "A confiança fica em resultado.boxes.conf, na mesma ordem das máscaras.",
            "solucao": "resposta = float(resultado.boxes.conf.max())",
        },
        {
            "titulo": "Área da maior máscara",
            "enunciado": "Quantos pixels tem a maior máscara? Cada `True` em `mascaras` é um pixel do objeto.",
            "dica": "mascaras.sum(axis=(1, 2)) soma a área de cada objeto.",
            "solucao": "resposta = int(mascaras.sum(axis=(1, 2)).max())",
        },
        {
            "titulo": "Só pessoas",
            "enunciado": "Rode o modelo de novo na mesma foto, pedindo só pessoas com `classes=[0]`. Quantas máscaras vieram?",
            "dica": "model(imagem, classes=[0], verbose=False)[0].masks",
            "solucao": "resposta = len(model(imagem, classes=[0], verbose=False)[0].masks)",
        },
        {
            "titulo": "O ônibus na foto",
            "enunciado": "Que fração da foto a máscara do ônibus cobre? Se houver mais de um ônibus, una as máscaras. Responda com um número entre 0 e 1.",
            "dica": "np.any junta máscaras, e .mean() num array booleano é a fração de True.",
            "solucao": '''idx = [i for i, c in enumerate(resultado.boxes.cls) if model.names[int(c)] == "bus"]
resposta = float(np.any(mascaras[idx], axis=0).mean())''',
        },
    ],
}

AULA2 = {
    "preparo": '''
from functools import lru_cache
from pathlib import Path

_cap = cv2.VideoCapture(video)
_total = int(_cap.get(cv2.CAP_PROP_FRAME_COUNT))
_fps_arquivo = _cap.get(cv2.CAP_PROP_FPS)
_cap.release()


@lru_cache(None)
def _pixels_cadeira_pulando():
    cap = cv2.VideoCapture(video)
    total = 0
    for i in range(40):
        ok, frame = cap.read()
        if not ok:
            break
        if i % 5:
            continue
        r = model(frame, verbose=False)[0]
        if r.masks is None:
            continue
        for c, m in zip(r.boxes.cls.int().tolist(), mascaras_originais(r)):
            if model.names[c] == "chair":
                total += int(m.sum())
    cap.release()
    return total


VERIFICAR = {
    1: lambda r: abs(float(r) - _total / _fps_arquivo) < 0.05,
    2: lambda r: r in {nome for nome, n in pixels.items() if n == max(pixels.values())},
    3: lambda r: int(r) == sum("person" in nomes for nomes in classes_por_quadro[:40]),
    4: lambda r: int(r) == _pixels_cadeira_pulando(),
    5: lambda r: abs(float(r) - (sum(mascaras_por_quadro) / len(mascaras_por_quadro))) < 1e-3,
    6: lambda r: Path(str(r)).name == "sala_plantas.mp4" and Path(str(r)).stat().st_size > 1000,
}
''',
    "lista": [
        {
            "titulo": "Duração do vídeo",
            "enunciado": "Quantos segundos tem o vídeo inteiro? Use o total de quadros e o FPS do arquivo, não só os quadros que a aula processou.",
            "dica": "cv2.CAP_PROP_FRAME_COUNT e cv2.CAP_PROP_FPS.",
            "solucao": '''cap = cv2.VideoCapture(video)
resposta = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
cap.release()''',
        },
        {
            "titulo": "Quem ocupa mais pixels",
            "enunciado": "Qual classe somou mais pixels de máscara no vídeo processado? Responda com o nome.",
            "dica": "pixels é um Counter: pixels.most_common(1) devolve o par (nome, total).",
            "solucao": "resposta = pixels.most_common(1)[0][0]",
        },
        {
            "titulo": "Quadros com pessoa",
            "enunciado": "Em quantos dos primeiros 40 quadros processados aparece pelo menos uma pessoa?",
            "dica": "classes_por_quadro[i] é a lista de nomes daquele quadro.",
            "solucao": 'resposta = sum("person" in nomes for nomes in classes_por_quadro[:40])',
        },
        {
            "titulo": "Pular quadros",
            "enunciado": "Nos primeiros 40 quadros, rode o modelo só em 1 a cada 5 (quadros 0, 5, 10...) e some os pixels das máscaras de `chair`.",
            "dica": "if i % 5: continue pula o quadro. mascaras_originais(r) devolve as máscaras no tamanho da foto.",
            "solucao": '''cap = cv2.VideoCapture(video)
total = 0
for i in range(40):
    ok, frame = cap.read()
    if not ok:
        break
    if i % 5:
        continue
    r = model(frame, verbose=False)[0]
    if r.masks is None:
        continue
    for c, m in zip(r.boxes.cls.int().tolist(), mascaras_originais(r)):
        if model.names[c] == "chair":
            total += int(m.sum())
cap.release()
resposta = total''',
        },
        {
            "titulo": "Média de máscaras",
            "enunciado": "Em média, quantas máscaras o modelo desenhou por quadro no vídeo processado?",
            "dica": "mascaras_por_quadro guarda a contagem de cada quadro.",
            "solucao": "resposta = sum(mascaras_por_quadro) / len(mascaras_por_quadro)",
        },
        {
            "titulo": "Vídeo só com plantas",
            "enunciado": "Grave um vídeo novo com os primeiros 40 quadros, desenhando só `potted plant`. A resposta é o caminho `sala_plantas.mp4`. O índice da classe está em `model.names`.",
            "dica": "Passe classes=[indice] na chamada do modelo e grave com r.plot().",
            "solucao": '''indice = [i for i, nome in model.names.items() if nome == "potted plant"][0]
cap = cv2.VideoCapture(video)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter("sala_plantas.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (largura, altura))
for _ in range(40):
    ok, frame = cap.read()
    if not ok:
        break
    r = model(frame, classes=[indice], verbose=False)[0]
    out.write(r.plot())
cap.release()
out.release()
resposta = "sala_plantas.mp4"''',
        },
    ],
}

AULA3 = {
    "preparo": '''
import numpy as np

_cls = resultado.boxes.cls.int().tolist()
_xyxy = resultado.boxes.xyxy.tolist()


def _indices(nome):
    return [i for i, c in enumerate(_cls) if model.names[c] == nome]


def _i_onibus():
    return max(_indices("bus"), key=lambda i: (_xyxy[i][2] - _xyxy[i][0]) * (_xyxy[i][3] - _xyxy[i][1]))


def _i_pessoa():
    return max(_indices("person"), key=lambda i: int(mascaras[i].sum()))


def _razao_caixa(i):
    x1, y1, x2, y2 = _xyxy[i]
    return float(mascaras[i].sum()) / ((x2 - x1) * (y2 - y1))


def _centro(i):
    ys, xs = np.where(mascaras[i])
    return (int(round(xs.mean())), int(round(ys.mean())))


def _iou_caixa(i):
    caixa = np.zeros(mascaras.shape[1:], dtype=bool)
    x1, y1, x2, y2 = map(int, _xyxy[i])
    caixa[y1:y2, x1:x2] = True
    inter = np.logical_and(mascaras[i], caixa).sum()
    uniao = np.logical_or(mascaras[i], caixa).sum()
    return float(inter / uniao)


def _pares():
    n = len(mascaras)
    return sum(
        bool(np.any(mascaras[i] & mascaras[j]))
        for i in range(n) for j in range(i + 1, n)
    )


def _recorte():
    i = _i_onibus()
    ys, xs = np.where(mascaras[i])
    return (int(ys.max() - ys.min() + 1), int(xs.max() - xs.min() + 1))


VERIFICAR = {
    1: lambda r: abs(float(r) - _razao_caixa(_i_onibus())) < 1e-3,
    2: lambda r: abs(float(r) - float(mascaras[_i_onibus()].mean()) * 100) < 0.1,
    3: lambda r: tuple(getattr(r, "shape", r)[:2]) == _recorte(),
    4: lambda r: all(abs(int(a) - b) <= 1 for a, b in zip(r, _centro(_i_pessoa()))),
    5: lambda r: abs(float(r) - _iou_caixa(_i_onibus())) < 1e-3,
    6: lambda r: int(r) == _pares(),
}
''',
    "lista": [
        {
            "titulo": "Quanto da caixa é objeto",
            "enunciado": "Divida a área da máscara do ônibus pela área da caixa dele. Se houver mais de um ônibus, use o da maior caixa. O resultado fica entre 0 e 1: é a parte da caixa que é ônibus de verdade.",
            "dica": "Área da caixa: (x2 - x1) * (y2 - y1), com os cantos em resultado.boxes.xyxy.",
            "solucao": '''def _area_caixa(k):
    x1, y1, x2, y2 = resultado.boxes.xyxy[k].tolist()
    return (x2 - x1) * (y2 - y1)

i = max(
    (k for k, c in enumerate(resultado.boxes.cls) if model.names[int(c)] == "bus"),
    key=_area_caixa,
)
x1, y1, x2, y2 = resultado.boxes.xyxy[i].tolist()
resposta = float(mascaras[i].sum()) / ((x2 - x1) * (y2 - y1))''',
        },
        {
            "titulo": "Porcentagem da foto",
            "enunciado": "Quantos por cento da foto a máscara desse ônibus cobre? Responda com um número de 0 a 100.",
            "dica": "A média de uma máscara booleana, vezes 100, é a porcentagem.",
            "solucao": '''i = max(
    (k for k, c in enumerate(resultado.boxes.cls) if model.names[int(c)] == "bus"),
    key=lambda k: float((resultado.boxes.xyxy[k][2] - resultado.boxes.xyxy[k][0]) * (resultado.boxes.xyxy[k][3] - resultado.boxes.xyxy[k][1])),
)
resposta = float(mascaras[i].mean()) * 100''',
        },
        {
            "titulo": "Recorte do ônibus",
            "enunciado": "Recorte a foto no retângulo justo da máscara do ônibus (o menor retângulo que ainda contém todos os pixels `True`). A resposta é o recorte.",
            "dica": "np.where devolve as linhas e as colunas. O recorte é img[y_min:y_max+1, x_min:x_max+1].",
            "solucao": '''i = max(
    (k for k, c in enumerate(resultado.boxes.cls) if model.names[int(c)] == "bus"),
    key=lambda k: float((resultado.boxes.xyxy[k][2] - resultado.boxes.xyxy[k][0]) * (resultado.boxes.xyxy[k][3] - resultado.boxes.xyxy[k][1])),
)
img = cv2.imread(imagem)
ys, xs = np.where(mascaras[i])
resposta = img[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

plt.imshow(resposta[:, :, ::-1])
plt.axis("off")
plt.show()''',
        },
        {
            "titulo": "Centro da pessoa",
            "enunciado": "Ache o centro da maior pessoa (a de máscara com mais pixels). Responda com `(x, y)` em pixels, x na horizontal.",
            "dica": "np.where(mascara) devolve (linhas, colunas). A média das colunas é o x.",
            "solucao": '''i = max(
    (k for k, c in enumerate(resultado.boxes.cls) if model.names[int(c)] == "person"),
    key=lambda k: int(mascaras[k].sum()),
)
ys, xs = np.where(mascaras[i])
resposta = (int(round(xs.mean())), int(round(ys.mean())))''',
        },
        {
            "titulo": "IoU com a caixa",
            "enunciado": "Calcule o IoU entre a máscara do ônibus e o retângulo da caixa dele. IoU é a interseção dividida pela união. Use o ônibus da maior caixa.",
            "dica": "Pinte um array booleano só dentro da caixa e compare com a máscara usando & e |.",
            "solucao": '''i = max(
    (k for k, c in enumerate(resultado.boxes.cls) if model.names[int(c)] == "bus"),
    key=lambda k: float((resultado.boxes.xyxy[k][2] - resultado.boxes.xyxy[k][0]) * (resultado.boxes.xyxy[k][3] - resultado.boxes.xyxy[k][1])),
)
caixa = np.zeros(mascaras.shape[1:], dtype=bool)
x1, y1, x2, y2 = map(int, resultado.boxes.xyxy[i].tolist())
caixa[y1:y2, x1:x2] = True
inter = np.logical_and(mascaras[i], caixa).sum()
uniao = np.logical_or(mascaras[i], caixa).sum()
resposta = float(inter / uniao)''',
        },
        {
            "titulo": "Máscaras que se tocam",
            "enunciado": "Quantos pares de máscaras têm pelo menos um pixel em comum?",
            "dica": "Para cada par i < j, np.any(mascaras[i] & mascaras[j]) diz se elas se encostam.",
            "solucao": '''pares = 0
n = len(mascaras)
for i in range(n):
    for j in range(i + 1, n):
        if np.any(mascaras[i] & mascaras[j]):
            pares += 1
resposta = pares''',
        },
    ],
}

AULA4 = {
    "preparo": '''
from collections import Counter
from functools import lru_cache

_raiz = DATASETS_DIR / "coco8-seg"
_arquivos = sorted((_raiz / "labels" / "train").glob("*.txt"))
_linhas = [l.split() for f in _arquivos for l in f.read_text().splitlines() if l.strip()]
_por_classe = Counter(int(l[0]) for l in _linhas)


def _pontos():
    nums = _arquivos[0].read_text().splitlines()[0].split()
    return (len(nums) - 1) // 2


@lru_cache(None)
def _map50_mascara():
    return float(melhor.val(data="coco8-seg.yaml", imgsz=320, verbose=False, plots=False).seg.map50)


VERIFICAR = {
    1: lambda r: int(r) == len(list((_raiz / "images" / "train").glob("*.jpg"))),
    2: lambda r: int(r) == len(_linhas),
    3: lambda r: r in {model.names[c] for c, n in _por_classe.items() if n == max(_por_classe.values())},
    4: lambda r: int(r) == _pontos(),
    5: lambda r: int(r) == int(df.loc[df["train/seg_loss"].idxmin(), "epoch"]),
    6: lambda r: abs(float(r) - _map50_mascara()) < 1e-3,
}
''',
    "lista": [
        {
            "titulo": "Tamanho do treino",
            "enunciado": "Quantas imagens há na pasta de treino do `coco8-seg`?",
            "dica": "As imagens ficam em DATASETS_DIR / \"coco8-seg\" / \"images\" / \"train\".",
            "solucao": 'resposta = len(list((DATASETS_DIR / "coco8-seg" / "images" / "train").glob("*.jpg")))',
        },
        {
            "titulo": "Objetos rotulados",
            "enunciado": "Quantos objetos rotulados existem, somando todos os arquivos `.txt` do treino? Cada linha é um objeto.",
            "dica": "Some o número de linhas de cada arquivo em labels/train.",
            "solucao": '''rotulos = (DATASETS_DIR / "coco8-seg" / "labels" / "train").glob("*.txt")
resposta = sum(len(f.read_text().strip().splitlines()) for f in rotulos)''',
        },
        {
            "titulo": "Classe mais rotulada",
            "enunciado": "Qual classe mais aparece nos rótulos de treino? Responda com o nome, não com o número.",
            "dica": "O primeiro número de cada linha é a classe; model.names traduz para nome.",
            "solucao": '''cont = Counter()
for f in (DATASETS_DIR / "coco8-seg" / "labels" / "train").glob("*.txt"):
    cont.update(int(l.split()[0]) for l in f.read_text().strip().splitlines())
resposta = model.names[cont.most_common(1)[0][0]]''',
        },
        {
            "titulo": "Pontos do polígono",
            "enunciado": "Abra o primeiro `.txt` de treino, em ordem alfabética. Quantos pontos tem o polígono da primeira linha? A classe é o primeiro número; cada ponto usa dois números.",
            "dica": "(quantidade de números - 1) / 2.",
            "solucao": '''arquivo = sorted((DATASETS_DIR / "coco8-seg" / "labels" / "train").glob("*.txt"))[0]
nums = arquivo.read_text().splitlines()[0].split()
resposta = (len(nums) - 1) // 2''',
        },
        {
            "titulo": "A menor perda",
            "enunciado": "Em qual época a `train/seg_loss` foi a menor?",
            "dica": "df[\"coluna\"].idxmin() dá a linha do menor valor.",
            "solucao": 'resposta = int(df.loc[df["train/seg_loss"].idxmin(), "epoch"])',
        },
        {
            "titulo": "mAP da máscara",
            "enunciado": "Rode a validação do modelo treinado com `melhor.val(data=\"coco8-seg.yaml\", imgsz=320)` e responda com o mAP50 das máscaras.",
            "dica": "O retorno de val() tem .seg.map50.",
            "solucao": '''metricas = melhor.val(data="coco8-seg.yaml", imgsz=320, verbose=False, plots=False)
resposta = metricas.seg.map50''',
        },
    ],
}

EXERCICIOS = {
    "01-segmentacao-em-imagem.ipynb": AULA1,
    "02-segmentacao-em-video.ipynb": AULA2,
    "03-medir-a-mascara.ipynb": AULA3,
    "04-treinar-segmentacao.ipynb": AULA4,
}
