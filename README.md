# Segmentação na prática, no Colab

A caixa em volta do leito leva o chão junto. Na obra, a caixa do operário leva a lama e o céu. A máscara fica só no objeto. Quatro notebooks curtos mostram isso com YOLOv8-seg, da enfermaria até um treino com polígono. Cada um abre direto no Google Colab.

| Aula | Abrir |
|---|---|
| 1. Segmentação em imagem | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/01-segmentacao-em-imagem.ipynb) |
| 2. Segmentação em vídeo | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/02-segmentacao-em-video.ipynb) |
| 3. Medir a máscara | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/03-medir-a-mascara.ipynb) |
| 4. Treinar segmentação | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/04-treinar-segmentacao.ipynb) |
| 5. Tomografia | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/05-tomografia.ipynb) |
| 6. Ressonância | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/06-ressonancia.ipynb) |

No Colab, use **Ambiente de execução → Executar tudo**. As aulas 1 a 3 rodam em CPU. Na aula 4, uma GPU T4 ajuda.

## Os 24 exercícios, um notebook cada

Cada exercício também existe como notebook próprio: prepara os dados, deixa uma célula para você tentar e mostra uma solução conferida.

| Aula | Exercício | Abrir |
|---|---|---|
| 1 | 1. Quantas máscaras | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio1-quantas-mascaras.ipynb) |
| 1 | 2. Classes com máscara | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio2-classes-com-mascara.ipynb) |
| 1 | 3. A máscara mais segura | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio3-a-mascara-mais-segura.ipynb) |
| 1 | 4. Área da maior máscara | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio4-area-da-maior-mascara.ipynb) |
| 1 | 5. Só os leitos | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio5-so-os-leitos.ipynb) |
| 1 | 6. Os leitos na foto | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio6-os-leitos-na-foto.ipynb) |
| 2 | 1. Duração do vídeo | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio1-duracao-do-video.ipynb) |
| 2 | 2. Quem ocupa mais pixels | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio2-quem-ocupa-mais-pixels.ipynb) |
| 2 | 3. Quadros com pessoa | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio3-quadros-com-pessoa.ipynb) |
| 2 | 4. Pular quadros | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio4-pular-quadros.ipynb) |
| 2 | 5. Média de máscaras | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio5-media-de-mascaras.ipynb) |
| 2 | 6. Vídeo só com pessoas | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio6-video-so-com-pessoas.ipynb) |
| 3 | 1. Quanto da caixa é o operário | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio1-quanto-da-caixa-e-o-operario.ipynb) |
| 3 | 2. Porcentagem da foto | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio2-porcentagem-da-foto.ipynb) |
| 3 | 3. Recorte do operário | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio3-recorte-do-operario.ipynb) |
| 3 | 4. Centro do operário | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio4-centro-do-operario.ipynb) |
| 3 | 5. IoU com a caixa | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio5-iou-com-a-caixa.ipynb) |
| 3 | 6. Máscaras que se tocam | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio6-mascaras-que-se-tocam.ipynb) |
| 4 | 1. Tamanho do treino | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio1-tamanho-do-treino.ipynb) |
| 4 | 2. Objetos rotulados | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio2-objetos-rotulados.ipynb) |
| 4 | 3. Classe mais rotulada | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio3-classe-mais-rotulada.ipynb) |
| 4 | 4. Pontos do polígono | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio4-pontos-do-poligono.ipynb) |
| 4 | 5. A menor perda | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio5-a-menor-perda.ipynb) |
| 4 | 6. mAP da máscara | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio6-map-da-mascara.ipynb) |

## Vídeos e fotos

Ficam em `midia/` e o Colab baixa do próprio repositório.

- `enfermaria.jpg`: quarto de hospital, Tomasz Sienicki, domínio público
- `obra.mp4`: obra da rodovia D8, Juandev, CC BY-SA 3.0
- `operarios.jpg`: Justine Belson, U.S. Fish and Wildlife Service, domínio público
- `canteiro.jpg`: Neb, CC BY-SA 4.0

Origem: Wikimedia Commons. O modelo segue nas 80 classes do COCO. Ele pinta leito, cadeira, pessoa e caminhão.

A tomografia e a ressonância não passam por esse modelo. Os volumes vêm do [3D Slicer](https://www.slicer.org/): CTChest e MRHead. A máscara sai da densidade, no tórax, e do sinal, na cabeça. Isso ainda não marca lesão.

## Exercícios

Cada aula termina com seis exercícios, 24 no total. Você escreve a resposta, roda a célula e a função `conferir` diz na hora se acertou. A solução fica em **Ver solução**, embaixo de cada enunciado.

Os exercícios ficam em `exercicios.py`. Os notebooks avulsos são gerados por `build_exercicios.py`.

## Editar

Os notebooks são gerados por `build_notebooks.py`. A página do site sai de `build_pagina.py`.

```bash
python build_notebooks.py
python build_exercicios.py
python build_pagina.py
```

A página fica em [naubergois.com/curso-segmentacao](https://naubergois.com/curso-segmentacao/).
