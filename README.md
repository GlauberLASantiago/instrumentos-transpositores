# Instrumentos Transpositores — edição web

Consulta musical recuperada do APK fornecido por Glauber Santiago. A aplicação preserva as 43 fichas originais: cada imagem informa se o instrumento é transpositor, sua tonalidade, intervalo de transposição, escrita da partitura, clave e leitura em um instrumento não transpositor.

## Usar

O aplicativo abre na primeira ficha, como o original. Use **Anterior** e **Próximo**, escolha um nome na lista ou faça uma busca digitada. **Falar!** procura um instrumento pela fala quando o navegador oferece reconhecimento de voz e o usuário autoriza o microfone. Esse recurso pode utilizar o serviço de reconhecimento do navegador; a busca digitada funciona sem ele. **Ampliar** abre a ficha em tela cheia.

A capa original está disponível na página Início. A lista, a busca digitada, os links diretos para fichas e a ampliação são adaptações para a web.

## Tecnologias e recuperação

O APK foi criado com **MIT App Inventor**, com lógica YAIL/Kawa compilada para DEX Android. Esta versão usa HTML, CSS e JavaScript nativo, sem depender do Android nem de um player Flash.

O REA inspecionou e extraiu o pacote sem executá-lo. SHA-256 do APK: `0fab126e0cb6e45dd2e33a8877d76cd74dc080520d46e2e4026798685981d681`. Os 44 arquivos de imagem (43 fichas e capa) permanecem byte a byte idênticos ao APK; hashes e IDs das evidências estão em `docs/extracted-assets.json`.

O provedor Android do REA não estava disponível por falta do JADX MCP JAR. A lógica foi recuperada por análise estática direta do DEX, com foco na classe Screen1. Essa análise identificou os botões Volta, Vai e Fala, atualização do arquivo de imagem pelo índice e os aliases da busca por voz. Não foi executado o APK, portanto não há uma comparação visual com o Android em execução.

A edição web mantém a sequência de 1 a 43. Corrige o limite de avanço do original, que retornava à primeira ficha ao alcançar 43; assim, a ficha de Guitarra também é acessível ao avançar. Os textos e as informações musicais das fichas não foram corrigidos ou reescritos.

## Desenvolvimento e validação

Requer Node.js:
```sh
npm start
npm test
```

Abra `http://127.0.0.1:4192/`. O teste verifica a integridade dos 44 recursos, os limites de navegação e o mapeamento dos aliases originais da fala. O reconhecimento real pelo microfone depende do navegador e não foi testado com áudio nesta recuperação.

GitHub Pages pode servir a raiz da branch main, sem compilação. O conteúdo original mantém sua autoria.
