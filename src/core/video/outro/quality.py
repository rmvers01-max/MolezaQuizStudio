from __future__ import annotations

class EndingQualityAnalyzer:
    def analyze(self, direction) -> dict:
        data = direction.to_dict() if hasattr(direction, 'to_dict') else dict(direction)
        score, findings = 100, []
        duration = float(data.get('duration', 5.2))
        if duration < 4.5: score -= 15; findings.append('Encerramento curto para CTA e despedida.')
        if duration > 6.5: score -= 12; findings.append('Encerramento longo demais.')
        if not data.get('headline'): score -= 25; findings.append('Headline ausente.')
        if not data.get('primary_cta'): score -= 18; findings.append('CTA principal ausente.')
        if data.get('quiz_type') == 'preferencia' and data.get('show_score_prompt'):
            score -= 35; findings.append('Preferência não pode exibir pontuação por acerto.')
        return {'score': max(score, 0), 'status': 'aaa_ready' if score >= 92 else 'approved' if score >= 80 else 'needs_revision', 'findings': findings}
