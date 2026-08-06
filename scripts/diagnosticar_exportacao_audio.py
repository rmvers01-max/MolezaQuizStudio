from __future__ import annotations

from pathlib import Path


path = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "core"
    / "video"
    / "legacy_generator.py"
)

source = path.read_text(
    encoding="utf-8"
)

checks = {
    "sem verificação legada": (
        "audio=bool(fontes_audio)"
        not in source
    ),
    "verifica áudio do clip final": (
        "audio_final_presente"
        in source
    ),
    "exporta áudio real": (
        "audio=audio_final_presente"
        in source
    ),
    "valida mixagem anexada": (
        "A mixagem foi criada, mas o áudio"
        in source
    ),
}

for name, result in checks.items():
    print(
        f"{name}:",
        result,
    )

assert all(
    checks.values()
)

print("\nEXPORTAÇÃO DE ÁUDIO OK")
