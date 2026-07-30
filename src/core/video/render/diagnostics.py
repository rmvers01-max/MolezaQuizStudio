from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RenderDiagnostics:
    cenas_renderizadas: int = 0
    quadros_renderizados: int = 0
    avisos: list[str] = field(
        default_factory=list
    )

    def registrar_cena(
        self,
        quadros: int,
    ):
        self.cenas_renderizadas += 1
        self.quadros_renderizados += int(
            quadros
        )

    def avisar(
        self,
        mensagem: str,
    ):
        self.avisos.append(
            str(mensagem)
        )

    def resumo(self) -> dict:
        return {
            "cenas_renderizadas": (
                self.cenas_renderizadas
            ),
            "quadros_renderizados": (
                self.quadros_renderizados
            ),
            "avisos": list(
                self.avisos
            ),
            "status": (
                "concluido"
                if not self.avisos
                else "concluido_com_avisos"
            ),
        }
