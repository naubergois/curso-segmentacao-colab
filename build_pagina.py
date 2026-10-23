"""Gera a página estática do curso, no mesmo formato de /curso-yolo/."""

import html
import re
from pathlib import Path

from build_exercicios import lista_exercicios
from comum import colab_url

PORTAL = Path("/Volumes/NAUBER/portal-nauber/public/curso-segmentacao")
REPO = "https://github.com/naubergois/curso-segmentacao-colab"

ROTULO = {1: "Imagem", 2: "Vídeo", 3: "Medida", 4: "Treino"}
CAPA = {1: "enfermaria-seg.jpg", 2: "obra-seg.jpg", 3: "operarios-seg.jpg", 4: "canteiro-seg.jpg"}


def inline(texto):
    texto = html.escape(texto)
    texto = re.sub(r"`([^`]+)`", r"<code>\1</code>", texto)
    texto = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", texto)
    return texto


def cartao(i, aula, n, ex, arquivo):
    capa = CAPA[aula]
    return f'''    <article class="ex">
      <div class="ex-capa"><img src="assets/{capa}" alt="Máscara de segmentação, sem caixa" loading="lazy"></div>
      <div class="ex-topo"><span class="ex-num">{i:02d}</span><span class="ex-aula">Aula {aula} · {ROTULO[aula]} · exercício {n}</span></div>
      <h3>{html.escape(ex["titulo"])}</h3>
      <p>{inline(ex["enunciado"].strip())}</p>
      <a class="botao" href="{colab_url("exercicios/" + arquivo)}" target="_blank" rel="noopener">Abrir no Colab</a>
    </article>'''


def pagina():
    cards = "\n".join(
        cartao(i, aula, n, ex, arquivo)
        for i, (_nb, aula, n, ex, arquivo) in enumerate(lista_exercicios(), start=1)
    )
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Segmentação na prática: a forma, não só a caixa | Nauber Gois</title>
<meta name="description" content="Segmentação com YOLOv8 no Colab, em foto de enfermaria e em obra: máscara, vídeo, medida da área e treino com polígono.">
<meta property="og:title" content="Segmentação na prática, direto no Colab">
<meta property="og:description" content="A caixa do leito leva o chão junto. A máscara fica no objeto. Enfermaria e canteiro de obras, no Colab.">
<meta property="og:image" content="https://naubergois.com/curso-segmentacao/assets/enfermaria-seg.jpg">
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --line: #30363d;
    --text: #e6edf3; --muted: #9da7b3; --accent: #f7c948; --link: #58a6ff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--bg); color: var(--text);
    font: 17px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }}
  main {{ max-width: 1040px; margin: 0 auto; padding: 56px 20px 80px; }}
  header h1 {{ font-size: clamp(2rem, 5vw, 3rem); line-height: 1.15; margin: 0 0 16px; }}
  header h1 span {{ color: var(--accent); }}
  .lead {{ color: var(--muted); max-width: 720px; font-size: 1.1rem; margin: 0 0 12px; }}
  .hero {{ margin: 32px 0 48px; border-radius: 12px; overflow: hidden; border: 1px solid var(--line); }}
  .hero img, .hero video {{ display: block; width: 100%; }}
  h2 {{ font-size: 1.4rem; margin: 48px 0 16px; }}
  .aulas {{ display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(min(100%, 420px), 1fr)); }}
  .aula {{
    background: var(--card); border: 1px solid var(--line); border-radius: 12px;
    overflow: hidden; display: flex; flex-direction: column;
  }}
  .aula .midia {{ aspect-ratio: 16 / 10; background: #000; overflow: hidden; }}
  .aula .midia img, .aula .midia video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .aula .midia pre {{
    margin: 0; height: 100%; padding: 20px; overflow: hidden; color: #c9d1d9;
    font: 14px/1.6 ui-monospace, SFMono-Regular, Menlo, monospace;
    background: linear-gradient(160deg, #1b2230, #0d1117);
  }}
  .aula .midia pre b {{ color: var(--accent); font-weight: 600; }}
  .aula .corpo {{ padding: 18px 20px 22px; display: flex; flex-direction: column; flex: 1; }}
  .num {{ color: var(--accent); font-weight: 700; font-size: .85rem; letter-spacing: .08em; }}
  .aula h3 {{ margin: 4px 0 8px; font-size: 1.2rem; }}
  .aula p {{ margin: 0 0 16px; color: var(--muted); font-size: .97rem; flex: 1; }}
  .meta {{ font-size: .85rem; color: var(--muted); margin-bottom: 14px; }}
  .botao {{
    display: inline-flex; align-items: center; gap: 10px; align-self: flex-start;
    background: var(--accent); color: #111; font-weight: 700; text-decoration: none;
    padding: 10px 16px; border-radius: 8px;
  }}
  .botao:hover {{ filter: brightness(1.08); }}
  .passos {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 8px 24px; }}
  .passos li {{ margin: 10px 0; }}
  code {{ background: #262c36; padding: 1px 6px; border-radius: 4px; font-size: .92em; }}
  a {{ color: var(--link); }}
  .exercicios {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); }}
  .ex {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 0 20px 18px; display: flex; flex-direction: column; overflow: hidden; }}
  .ex-capa {{ margin: 0 -20px 14px; aspect-ratio: 16 / 10; background: #000; overflow: hidden; }}
  .ex-capa img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .ex-topo {{ display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }}
  .ex-num {{ background: var(--accent); color: #111; font-weight: 800; border-radius: 6px; padding: 2px 8px; font-size: .9rem; }}
  .ex-aula {{ color: var(--muted); font-size: .8rem; letter-spacing: .02em; }}
  .ex h3 {{ margin: 4px 0 6px; font-size: 1.08rem; }}
  .ex p {{ margin: 0 0 14px; color: var(--muted); font-size: .92rem; flex: 1; }}
  .ex .botao {{ padding: 8px 14px; font-size: .92rem; }}
  footer {{ margin-top: 56px; color: var(--muted); font-size: .9rem; border-top: 1px solid var(--line); padding-top: 20px; }}
</style>
</head>
<body>
<main>
  <header>
    <h1>Segmentação na prática: <span>a forma, não só a caixa</span></h1>
    <p class="lead">O retângulo em volta do leito leva junto o chão, a cortina e um pedaço da parede. Na obra, a caixa do operário leva a picareta, a lama e um pedaço do céu. A segmentação devolve o contorno: uma máscara só com os pixels do objeto.</p>
    <p class="lead">Enfermaria e canteiro passam pelo modelo das 80 classes. Tomografia e ressonância são outro exame: o corte é uma grade de densidade ou de sinal, e a máscara sai dessa grade. Isso ainda não é um laudo.</p>
    <p class="lead">Cada notebook abre no Google Colab. Você escreve a resposta, roda a célula e ele diz na hora se acertou. <a href="#exercicios">Ver os 24 exercícios</a>.</p>
  </header>

  <div class="hero">
    <img src="assets/enfermaria-seg.jpg" alt="Máscaras coloridas sobre os leitos e as cadeiras da enfermaria, sem retângulo">
  </div>

  <h2>As aulas</h2>
  <div class="aulas">

    <article class="aula">
      <div class="midia"><img src="assets/enfermaria-seg.jpg" alt="Máscaras sobre os leitos e as cadeiras, sem caixa" loading="lazy"></div>
      <div class="corpo">
        <span class="num">AULA 1</span>
        <h3>Segmentação em imagem</h3>
        <p>O quarto de hospital volta com uma máscara por leito e por cadeira. Cada máscara é uma grade de verdadeiro ou falso, e somar os pixels verdadeiros dá a área do objeto.</p>
        <div class="meta">CPU · cerca de 1 minuto · 6 exercícios</div>
        <a class="botao" href="{colab_url("notebooks/01-segmentacao-em-imagem.ipynb")}" target="_blank" rel="noopener">Abrir no Colab</a>
      </div>
    </article>

    <article class="aula">
      <div class="midia"><img src="assets/obra-seg.jpg" alt="Operários e máquinas na obra de rodovia, pintados pela máscara, sem retângulo" loading="lazy"></div>
      <div class="corpo">
        <span class="num">AULA 2</span>
        <h3>Segmentação em vídeo</h3>
        <p>O clipe é uma obra de rodovia. O laço lê o quadro, segmenta e grava. A escavadeira não tem classe própria: o nome que volta costuma ser trem ou caminhão. A conta que importa é a área.</p>
        <div class="meta">CPU · cerca de 2 minutos · 6 exercícios</div>
        <a class="botao" href="{colab_url("notebooks/02-segmentacao-em-video.ipynb")}" target="_blank" rel="noopener">Abrir no Colab</a>
      </div>
    </article>

    <article class="aula">
      <div class="midia"><img src="assets/operarios-seg.jpg" alt="Operários na obra com o centro da máscara marcado, sem retângulo" loading="lazy"></div>
      <div class="corpo">
        <span class="num">AULA 3</span>
        <h3>Medir a máscara</h3>
        <p>A máscara do operário vira número: a porcentagem da foto, o centro do corpo, o quanto a caixa sobra e se as duas pessoas se encostam.</p>
        <div class="meta">CPU · cerca de 1 minuto · 6 exercícios</div>
        <a class="botao" href="{colab_url("notebooks/03-medir-a-mascara.ipynb")}" target="_blank" rel="noopener">Abrir no Colab</a>
      </div>
    </article>

    <article class="aula">
      <div class="midia"><img src="assets/canteiro-seg.jpg" alt="Caminhões no canteiro pintados pela máscara, sem retângulo" loading="lazy"></div>
      <div class="corpo">
        <span class="num">AULA 4</span>
        <h3>Treinar segmentação</h3>
        <p>O rótulo deixa de ser um retângulo e vira um polígono. Quatro fotos mostram o caminho. No canteiro, o modelo ainda pinta o caminhão. A trinca no solo continua sem máscara.</p>
        <div class="meta">GPU T4 recomendada · cerca de 3 minutos · 6 exercícios</div>
        <a class="botao" href="{colab_url("notebooks/04-treinar-segmentacao.ipynb")}" target="_blank" rel="noopener">Abrir no Colab</a>
      </div>
    </article>

    <article class="aula">
      <div class="midia"><img src="assets/tomografia-seg.jpg" alt="Tomografia de tórax com o pulmão pintado pela máscara" loading="lazy"></div>
      <div class="corpo">
        <span class="num">AULA 5</span>
        <h3>Tomografia</h3>
        <p>O corte do tórax é densidade. Osso estoura no branco, ar fica preto. A máscara do pulmão é o ar que está dentro do corpo, não o ar de fora.</p>
        <div class="meta">CPU · cerca de 1 minuto · volume de 40 MB</div>
        <a class="botao" href="{colab_url("notebooks/05-tomografia.ipynb")}" target="_blank" rel="noopener">Abrir no Colab</a>
      </div>
    </article>

    <article class="aula">
      <div class="midia"><img src="assets/ressonancia-seg.jpg" alt="Ressonância da cabeça com o cérebro pintado pela máscara" loading="lazy"></div>
      <div class="corpo">
        <span class="num">AULA 6</span>
        <h3>Ressonância</h3>
        <p>O mesmo volume, dois cortes: um pelos olhos, outro de lado. A máscara é o maior bloco de sinal. O crânio fica de fora. Lesão ainda não tem classe.</p>
        <div class="meta">CPU · cerca de 1 minuto · volume de 7 MB</div>
        <a class="botao" href="{colab_url("notebooks/06-ressonancia.ipynb")}" target="_blank" rel="noopener">Abrir no Colab</a>
      </div>
    </article>

  </div>

  <h2 id="exercicios">Os 24 exercícios</h2>
  <p class="lead">Cada exercício tem um notebook só dele. Ele prepara os dados da aula, deixa uma célula para você tentar e mostra uma solução conferida. É só clicar em <strong>Abrir no Colab</strong>.</p>
  <div class="exercicios">
{cards}
  </div>

  <h2>Como rodar</h2>
  <ol class="passos">
    <li>Clique em <strong>Abrir no Colab</strong> e entre com sua conta Google.</li>
    <li>Menu <strong>Ambiente de execução → Executar tudo</strong>. Na aula 4, antes, troque o tipo de ambiente para <strong>T4 GPU</strong>.</li>
    <li>Se o Colab avisar que o notebook não é do Google, confirme em <strong>Executar mesmo assim</strong>.</li>
    <li>Nos exercícios, troque <code>resposta = None</code> pela sua resposta e rode a célula. A solução conferida vem na célula de baixo.</li>
    <li>Para guardar suas alterações, use <strong>Arquivo → Salvar uma cópia no Drive</strong>.</li>
  </ol>

  <footer>
    O código está em <a href="{REPO}">github.com/naubergois/curso-segmentacao-colab</a>.
    A detecção com caixas está em <a href="https://naubergois.com/curso-yolo/">YOLO na prática</a>.
    Enfermaria: Tomasz Sienicki, domínio público. Operários: Justine Belson, U.S. Fish and Wildlife Service, domínio público.
    Canteiro: Neb, CC BY-SA 4.0. Vídeo da obra da D8: Juandev, CC BY-SA 3.0. Tudo via Wikimedia Commons.
    Tomografia: CTChest, amostra do <a href="https://www.slicer.org/">3D Slicer</a>.
    Ressonância: MRHead, doada ao 3D Slicer para uso sem restrição.
    <br>Nauber Gois · <a href="https://naubergois.com">naubergois.com</a>
  </footer>
</main>
</body>
</html>
'''


def main():
    destino = PORTAL / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    (PORTAL / "assets").mkdir(exist_ok=True)
    destino.write_text(pagina(), encoding="utf-8")
    print("ok", destino)


if __name__ == "__main__":
    main()
