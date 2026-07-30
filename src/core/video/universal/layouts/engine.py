from __future__ import annotations

from dataclasses import dataclass

from ..components import ComponentBox


@dataclass(frozen=True, slots=True)
class KnowledgeLayout:
    question: ComponentBox
    main_image: ComponentBox | None
    choices: tuple[ComponentBox, ...]
    timer: ComponentBox
    progress: ComponentBox
    answer: ComponentBox


class UniversalLayoutEngine:
    def __init__(
        self,
        width=1280,
        height=720,
    ):
        self.width = int(width)
        self.height = int(height)

    def knowledge(
        self,
        choice_count: int,
        has_image: bool,
    ) -> KnowledgeLayout:
        question = ComponentBox(
            x=100,
            y=76,
            width=self.width - 200,
            height=115,
        )

        progress = ComponentBox(
            x=995,
            y=22,
            width=190,
            height=48,
        )

        timer = ComponentBox(
            x=55,
            y=22,
            width=90,
            height=90,
        )

        if has_image:
            main_image = ComponentBox(
                x=100,
                y=210,
                width=460,
                height=340,
            )

            choice_area_x = 610
            choice_area_width = 560

        else:
            main_image = None
            choice_area_x = 150
            choice_area_width = 980

        count = max(
            min(
                int(choice_count),
                6
            ),
            1
        )

        columns = (
            2
            if count >= 4
            else 1
        )

        rows = (
            count + columns - 1
        ) // columns

        gap_x = 20
        gap_y = 18

        box_width = (
            choice_area_width
            - gap_x * (
                columns - 1
            )
        ) // columns

        available_height = 360
        box_height = min(
            86,
            (
                available_height
                - gap_y * (
                    rows - 1
                )
            ) // rows
        )

        choices = []

        for index in range(count):
            column = index % columns
            row = index // columns

            choices.append(
                ComponentBox(
                    x=(
                        choice_area_x
                        + column
                        * (
                            box_width
                            + gap_x
                        )
                    ),
                    y=(
                        225
                        + row
                        * (
                            box_height
                            + gap_y
                        )
                    ),
                    width=box_width,
                    height=box_height,
                )
            )

        answer = ComponentBox(
            x=270,
            y=500,
            width=740,
            height=135,
        )

        return KnowledgeLayout(
            question=question,
            main_image=main_image,
            choices=tuple(choices),
            timer=timer,
            progress=progress,
            answer=answer,
        )
