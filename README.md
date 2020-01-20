# Pod.py: A Alternativa Preguiçosa para Podcasters

Script para compilar um podcast com música de fundo e transição entre capítulos

## Introdução

Digamos que você quer fazer um podcast, mas tem preguiça de editar. Então você é que nem eu: uma pessoa ~~preguiçosa~~ que quer falar do que gosta ao mesmo tempo que foca somente no importante; o conteúdo. Sendo assim, PodPy é feito para você!

**AVISO**: O script ainda está incompleto! Siga passo a passo o setup para que ele funcione corretamente enquanto eu conserto tudo.

## Setup

1. Clone o repositório e entre na pasta

```bash
git clone https://github.com/dandeeccastro/podpy
cd podpy
```
2. Crie a pasta que você vai botar os arquivos do seu podcast. Ela tem que conter certas pastas para funcionar direito. Uma delas é a `assets`. Ela deverá ter a seguinte estrutura: 

```bash
├── assets
│   ├── 1
│   │   └── 1.m4a
│   │   └── 2.mp3
│   │   └── 3.m4a
│   ├── 2
│   │   └── 1.m4a
│   │   └── 2.mp3
│   └── 3
│       └── 1.m4a

```

Cada pasta dentro dela representará os *capítulos* do seu podcast, e cada capítulo tem os seus áudios. Enumere eles para que o programa saiba qual vem primeiro

A outra pasta é a `music`, que vai conter suas músicas de fundo. Pode botar quantas músicas quiser, o programa vai fazer um *mix aleatório* delas como música de fundo!

3. Rode o código e seja feliz!
```bash
python3 main.py
```
