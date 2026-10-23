# Segmentação na prática, no Colab

A caixa em volta do ônibus leva o céu junto. A máscara fica só no objeto. Quatro notebooks curtos mostram isso com YOLOv8-seg, da primeira foto até um treino com polígono. Cada um abre direto no Google Colab.

| Aula | Abrir |
|---|---|
| 1. Segmentação em imagem | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/01-segmentacao-em-imagem.ipynb) |
| 2. Segmentação em vídeo | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/02-segmentacao-em-video.ipynb) |
| 3. Medir a máscara | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/03-medir-a-mascara.ipynb) |
| 4. Treinar segmentação | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/notebooks/04-treinar-segmentacao.ipynb) |

No Colab, use **Ambiente de execução → Executar tudo**. As aulas 1 a 3 rodam em CPU. Na aula 4, uma GPU T4 ajuda.

## Os 24 exercícios, um notebook cada

Cada exercício também existe como notebook próprio: prepara os dados, deixa uma célula para você tentar e mostra uma solução conferida.

| Aula | Exercício | Abrir |
|---|---|---|
| 1 | 1. Quantas máscaras | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio1-quantas-mascaras.ipynb) |
| 1 | 2. Classes com máscara | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio2-classes-com-mascara.ipynb) |
| 1 | 3. A máscara mais segura | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio3-a-mascara-mais-segura.ipynb) |
| 1 | 4. Área da maior máscara | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio4-area-da-maior-mascara.ipynb) |
| 1 | 5. Só pessoas | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio5-so-pessoas.ipynb) |
| 1 | 6. O ônibus na foto | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula1-exercicio6-o-onibus-na-foto.ipynb) |
| 2 | 1. Duração do vídeo | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio1-duracao-do-video.ipynb) |
| 2 | 2. Quem ocupa mais pixels | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio2-quem-ocupa-mais-pixels.ipynb) |
| 2 | 3. Quadros com pessoa | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio3-quadros-com-pessoa.ipynb) |
| 2 | 4. Pular quadros | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio4-pular-quadros.ipynb) |
| 2 | 5. Média de máscaras | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio5-media-de-mascaras.ipynb) |
| 2 | 6. Vídeo só com plantas | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula2-exercicio6-video-so-com-plantas.ipynb) |
| 3 | 1. Quanto da caixa é objeto | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio1-quanto-da-caixa-e-objeto.ipynb) |
| 3 | 2. Porcentagem da foto | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio2-porcentagem-da-foto.ipynb) |
| 3 | 3. Recorte do ônibus | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio3-recorte-do-onibus.ipynb) |
| 3 | 4. Centro da pessoa | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio4-centro-da-pessoa.ipynb) |
| 3 | 5. IoU com a caixa | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio5-iou-com-a-caixa.ipynb) |
| 3 | 6. Máscaras que se tocam | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula3-exercicio6-mascaras-que-se-tocam.ipynb) |
| 4 | 1. Tamanho do treino | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio1-tamanho-do-treino.ipynb) |
| 4 | 2. Objetos rotulados | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio2-objetos-rotulados.ipynb) |
| 4 | 3. Classe mais rotulada | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio3-classe-mais-rotulada.ipynb) |
| 4 | 4. Pontos do polígono | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio4-pontos-do-poligono.ipynb) |
| 4 | 5. A menor perda | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio5-a-menor-perda.ipynb) |
| 4 | 6. mAP da máscara | [Colab](https://colab.research.google.com/github/naubergois/curso-segmentacao-colab/blob/main/exercicios/aula4-exercicio6-map-da-mascara.ipynb) |

## Vídeos e fotos

- `bus.jpg`, da [Ultralytics](https://ultralytics.com/images/bus.jpg)
- `home-objects-compressed.mp4`, dos [assets da Ultralytics](https://github.com/ultralytics/assets/releases/tag/v0.0.0)

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
