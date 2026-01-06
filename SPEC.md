## Karaoke AI Backing – MVP (IA refaz instrumentos)

### Versão
v0.1 – MVP técnico (sem vídeo)

### Plataforma alvo
- macOS (ambiente local de desenvolvimento)

---

## 1. Visão Geral

Este projeto tem como objetivo criar um **pipeline automatizado** que, a partir de um **arquivo de áudio licenciado/autoral**, gera um **backing track instrumental** utilizando técnicas de **análise musical + IA**.

O processo **não reutiliza o áudio original** como backing.  
Os instrumentos são **recriados** a partir de:
- detecção de BPM / beats
- extração de acordes
- extração de linha de baixo
- geração de MIDI
- renderização de áudio via SoundFont

O MVP **não inclui** vídeo, karaokê visual ou upload para plataformas.

---

## 2. Escopo do MVP

### Incluído
- CLI para rodar pipeline por música
- Padronização e normalização de áudio
- Análise musical (tempo, beats, acordes, baixo)
- Geração de MIDI (drums, bass, chords, arrangement)
- Renderização MIDI → WAV (FluidSynth + SoundFont)
- Mix e master simples
- Exportação de artefatos
- Relatório técnico (`report.json`)

### Fora do escopo
- Geração de vídeo
- Letras sincronizadas (.srt / .ass)
- Upload para YouTube
- Interface gráfica / web
- Autorização/licenciamento automático de músicas

---

## 3. Requisitos Técnicos

### Sistema
- macOS
- Python 3.11+

### Dependências nativas
- `ffmpeg`
- `fluidsynth`

### Bibliotecas Python (sugestão mínima)
- typer (CLI)
- pydantic (validação de schema)
- rich (logs)
- numpy
- scipy
- librosa (BPM, beats, chroma)
- pretty_midi ou mido (MIDI)
- basic-pitch ou crepe (pitch tracking)

---

## 4. Estrutura de Pastas (Obrigatória)

```text
karaoke-ai-backing/
  README.md
  SPEC.md
  pyproject.toml
  .gitignore

  input/
    songs/
      <song_id>/
        audio.mp3
        meta.json
        lyrics.txt            # opcional
        assets/
          background.png      # opcional

  work/
    songs/
      <song_id>/
        00_original/
          audio.wav
        01_analysis/
          bpm.json
          beats.json
          chroma.npy
          chords.json
          bass_pitch.json
        02_midi/
          drums.mid
          bass.mid
          chords.mid
          arrangement.mid
        03_render/
          drums.wav
          bass.wav
          chords.wav
          backing.wav
        04_mix/
          backing_final.wav

  output/
    songs/
      <song_id>/
        backing.wav
        midi/
          drums.mid
          bass.mid
          chords.mid
          arrangement.mid
        report.json

  assets/
    soundfonts/
      GeneralUser_GS.sf2

  src/
    karaoke/
      cli.py
      pipeline.py
      schemas.py
      config.py
      utils/
        paths.py
        proc.py
        log.py
        audio.py
        midi.py
      steps/
        s00_validate.py
        s01_prepare_audio.py
        s02_analyze_tempo_beats.py
        s03_extract_chords.py
        s04_extract_bass_pitch.py
        s05_build_midi.py
        s06_render_midi.py
        s07_mix_master.py
        s08_export.py
```
