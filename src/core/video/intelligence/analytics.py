from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any


class PerformanceAnalyticsEngine:
    def analyze(
        self,
        metrics: list[dict[str, Any]],
    ) -> dict[str, Any]:
        valid = [
            item
            for item in metrics
            if isinstance(item, dict)
        ]

        if not valid:
            return {
                "sample_size": 0,
                "averages": {},
                "by_quiz_type": {},
                "by_theme_pack": {},
                "best_videos": [],
            }

        return {
            "sample_size": len(valid),
            "averages": self._averages(
                valid
            ),
            "by_quiz_type": self._group(
                valid,
                "quiz_type",
            ),
            "by_theme_pack": self._group(
                valid,
                "theme_pack",
            ),
            "best_videos": self._best_videos(
                valid
            ),
        }

    def _averages(
        self,
        items,
    ):
        fields = (
            "ctr_percent",
            "average_percentage_viewed",
            "first_30_seconds_retention",
            "likes",
            "comments",
            "subscribers_gained",
            "views",
        )

        result = {}

        for field in fields:
            values = [
                float(item[field])
                for item in items
                if item.get(field)
                is not None
            ]

            if values:
                result[field] = round(
                    mean(values),
                    3,
                )

        return result

    def _group(
        self,
        items,
        field,
    ):
        groups = defaultdict(list)

        for item in items:
            key = str(
                item.get(field)
                or "não informado"
            )

            groups[key].append(item)

        return {
            key: {
                "count": len(values),
                "averages": self._averages(
                    values
                ),
            }
            for key, values
            in groups.items()
        }

    def _best_videos(
        self,
        items,
    ):
        scored = []

        for item in items:
            retention = float(
                item.get(
                    "average_percentage_viewed"
                )
                or 0
            )

            ctr = float(
                item.get(
                    "ctr_percent"
                )
                or 0
            )

            subscribers = float(
                item.get(
                    "subscribers_gained"
                )
                or 0
            )

            views = max(
                float(
                    item.get(
                        "views"
                    )
                    or 0
                ),
                1.0,
            )

            subscriber_rate = (
                subscribers
                / views
                * 1000
            )

            score = (
                retention * 0.52
                + ctr * 2.4
                + subscriber_rate * 0.18
            )

            scored.append(
                {
                    "video_id": item.get(
                        "video_id"
                    ),
                    "title": item.get(
                        "title"
                    ),
                    "score": round(
                        score,
                        3,
                    ),
                    "quiz_type": item.get(
                        "quiz_type"
                    ),
                    "theme_pack": item.get(
                        "theme_pack"
                    ),
                }
            )

        return sorted(
            scored,
            key=lambda item: item["score"],
            reverse=True,
        )[:10]
