Pasta do site separada do bot

Este diretório contém a landing page simples com links para Instagram (@halloktty) e para o bot do Telegram.

Arquivos:
- `index.html` — página principal
- `styles.css` — estilos

Para testar localmente:
1. Abra PowerShell e navegue até esta pasta:
   ```powershell
   cd "C:\Users\richa\Projetos\site_halloktty"
   ```
2. Rode um servidor local:
   ```powershell
   py -m http.server 8000
   ```
3. Abra http://localhost:8000 no navegador.

Para publicar, faça deploy em Netlify ou GitHub Pages (arrastar a pasta ou publicar a pasta `site_halloktty`).
