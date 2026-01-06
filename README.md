# Karaoke AI Backing

Pipeline inicial para gerar backing tracks instrumentais a partir de um arquivo MP3.

## Requisitos

- Python 3.11+
- `ffmpeg`
- `fluidsynth`

## Estrutura esperada

Coloque o áudio em `input/songs/<song_id>/audio.mp3`.

## Como usar

```bash
python -m karaoke.cli run <song_id>
```

Os artefatos serão gerados em `work/` e exportados para `output/`.

Consulte o arquivo `SPEC.md` para detalhes do MVP.
