from pathlib import Path


def _source():
    path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "core"
        / "video"
        / "legacy_generator.py"
    )
    return path.read_text(
        encoding="utf-8"
    )


def test_export_does_not_use_legacy_audio_list():
    source = _source()

    assert (
        "audio=bool(fontes_audio)"
        not in source
    )


def test_export_checks_audio_on_final_clip():
    source = _source()

    assert (
        "audio_final_presente"
        in source
    )
    assert (
        'getattr(\n'
        '                    video_para_exportar,\n'
        '                    "audio",'
        in source
    )
    assert (
        "audio=audio_final_presente"
        in source
    )


def test_mixed_audio_is_validated_after_attachment():
    source = _source()

    assert (
        "A mixagem foi criada, mas o áudio "
        in source
    )
