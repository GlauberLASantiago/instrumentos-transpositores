# Comportamento recuperado estaticamente do APK

Fonte: classes.dex e classes2.dex do pacote extraído pelo REA, sem execução do APK. `dex_static.py` lê tabelas e instruções Dalvik; `dex-evidence.json` guarda referências, offsets de código e limites das instruções. `annotate.py` associa constantes de Screen1 ao inicializador estático. `annotated-methods.txt` permite conferir cada conclusão.

## Aplicativo próprio

Só existe uma tela própria `appinventor.ai_glauberglauberglauber.InstrumentosTranspositores.Screen1` e sua classe auxiliar Kawa `$frame`. As demais classes do pacote são recursos R; não foram identificadas outras telas próprias em classes2.dex. O aplicativo foi compilado pelo MIT App Inventor, com código YAIL/Kawa. Caminho YAIL embutido contém timestamp 1619368448241, indício de compilação em abril de 2021, não prova de criação nessa data.

## Inicialização e navegação

`run` registra `g$instrumento` via `lambda3`, que retorna Lit4=1. `Screen1$Initialize` chama `p$Efetua`; `lambda4`/`lambda6` atribuem `DadosDosInstrumentos.Picture` ao índice global concatenado com `.jpg`. A tela inicial, portanto, é a ficha 1.jpg. Não há controle de capa no código identificado.

`Vai$Click` soma 1 ao índice; se o resultado é >=43, atribui 1; depois atualiza a imagem. Esse limite original pula a ficha 43 ao avançar da 42. `Volta$Click` soma -1; se resultado <=0 atribui 43; depois atualiza. A ficha 43 continua acessível voltando da primeira e por comando de voz. A versão web pode corrigir o limite de avanço para >43 e documentar essa correção.

## Controles e apresentação

Componentes visíveis: imagem `DadosDosInstrumentos` e organização em tabela de três colunas com os botões `Volta`, `Fala`, `Vai`. Textos dos botões: seta esquerda, `Falar!`, seta direita. Botões têm FontSize=20. A imagem usa `ScalePictureToFit=true`, Height/Width=-2 (preencher pai). A tela tem título `Instrumentos Transpositores`, tamanho Responsive, orientação sensor, fundo e ícone `PianoFundo.jpeg`. Não foi encontrada lista de seleção original; a busca digitada e seletor de fichas são melhorias web.

## Voz

`Fala$Click` chama `ReconhecedorDeVoz1.GetText`. `ReconhecedorDeVoz1$AfterGettingText` compara o resultado com nomes/aliases de instrumentos, atribui índice e termina chamando `p$Efetua`. `voice-aliases.json` contém os aliases exatos do APK em UTF-8; é a fonte para a seleção por voz. Não foi identificada normalização explícita de caixa/acentos no código próprio. Alguns aliases são erros ou aproximações históricos, como `shallow` para violoncelo, `glocknspiel`, `clarineta contralto` e `clarinete alto` mapeados a 13. Não substituir silenciosamente esses registros na documentação.

## Escopo e limites

Não há handlers próprios de quiz, pontuação, áudio sintetizado ou cálculo de transposição: a função é consultar as 43 fichas visuais preservadas. Essa conclusão se refere aos métodos da aplicação própria extraída, e não a uma execução dinâmica em Android. O parser foi feito para recuperar referências e constantes necessárias; não substitui uma decompilação integral de todo o framework App Inventor. A migração web da voz depende de suporte SpeechRecognition/webkitSpeechRecognition no navegador.
