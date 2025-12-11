Coloque aqui as imagens (figurinha) que serão usadas no site.

Instruções:
- Nomeie as imagens como `sticker1.png`, `sticker2.png`, etc.
- Preferível: arquivos PNG com fundo transparente (exportar do seu editor ou usar remove.bg ou similar).
- Se não remover o fundo, o site aplicará efeitos visuais, mas o resultado fica melhor com PNG transparante.

Ferramentas online para remover fundo rapidamente:
- https://www.remove.bg/
- https://photoscissors.com/

Depois de colocar as imagens, atualize o site (recarregue a página/servidor local).

Processamento automático (script):
- Você pode usar o script `tools/process_stickers.py` para remover o fundo e separar várias figurinhas
	de uma única imagem (por exemplo uma imagem com várias figurinhas juntas).
- Como usar:
	1. Instale dependências: `pip install -r tools/requirements.txt` (recomendado dentro de um virtualenv).
	2. Coloque sua imagem com várias figurinhas em `site_halloktty/images/source.png`.
	3. Rode: `python tools/process_stickers.py site_halloktty/images/source.png`.
	4. O script irá gerar `sticker1.png`, `sticker2.png`, ... na mesma pasta `images/`.

Observações:
- Para melhores resultados utilize imagens em alta resolução. O script usa a biblioteca `rembg` para
	remoção automática de fundo; ela é bastante eficaz em imagens com contraste entre figura e fundo.