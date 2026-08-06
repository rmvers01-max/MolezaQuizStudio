from __future__ import annotations

from .models import DuckingWindow


class AudioDuckingPlanner:
    """
    Cria janelas de ducking usando os tempos dos clips de primeiro plano.

    As janelas sobrepostas são combinadas para evitar dezenas de cortes
    desnecessários na música.
    """

    def create_windows(
        self,
        clips,
        *,
        duration: float,
        gain: float,
        attack: float,
        release: float,
    ) -> tuple[DuckingWindow, ...]:
        raw = []

        for clip in clips:
            start = self._number(
                getattr(
                    clip,
                    "start",
                    0.0,
                ),
                0.0,
            )

            clip_duration = self._number(
                getattr(
                    clip,
                    "duration",
                    0.0,
                ),
                0.0,
            )

            end_value = getattr(
                clip,
                "end",
                None,
            )

            end = (
                self._number(
                    end_value,
                    start + clip_duration,
                )
                if end_value is not None
                else start + clip_duration
            )

            if end <= start:
                continue

            raw.append(
                (
                    max(
                        start - float(attack),
                        0.0,
                    ),
                    min(
                        end + float(release),
                        float(duration),
                    ),
                )
            )

        if not raw:
            return ()

        raw.sort(
            key=lambda item: (
                item[0],
                item[1],
            )
        )

        merged = [
            list(raw[0])
        ]

        for start, end in raw[1:]:
            previous = merged[-1]

            if start <= previous[1] + 0.04:
                previous[1] = max(
                    previous[1],
                    end,
                )
            else:
                merged.append(
                    [start, end]
                )

        return tuple(
            DuckingWindow(
                start=round(start, 4),
                end=round(end, 4),
                gain=float(gain),
                reason="foreground_audio",
            )
            for start, end in merged
            if end > start
        )

    def _number(
        self,
        value,
        default,
    ) -> float:
        try:
            return float(value)
        except (
            TypeError,
            ValueError,
        ):
            return float(default)
