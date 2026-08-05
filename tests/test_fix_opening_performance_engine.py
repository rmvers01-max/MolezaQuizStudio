from pathlib import Path

def test_opening_performance_engine_patch():
    p=Path(__file__).resolve().parents[1]/"src/core/video/opening/opening_studio.py"
    s=p.read_text(encoding="utf-8")
    assert "from ..performance_engine import AAAPerformanceEngine" in s
    assert "def _get_performance_engine(self):" in s
    assert "self.performance_engine = (" in s
