from __future__ import annotations
from .models import EndingDirection

class AAAEndingDirector:
    CATEGORY_CLOSERS = {
        'flags_geography': 'Cada bandeira conta uma parte da história de um país!',
        'animals': 'O mundo animal ainda guarda muitas surpresas!',
        'food': 'Comida também é cultura, história e diversão!',
        'sports': 'Cada desafio é uma nova chance de superar seu resultado!',
        'characters': 'Sempre existe outro personagem esperando para ser descoberto!',
        'preference': 'Não existe escolha certa: a melhor é a que combina com você!',
        'general_knowledge': 'Quanto mais você joga, mais coisas incríveis descobre!',
    }

    def choose(self, *, category: str, quiz_type: str, duration: float = 5.4,
               production_mode: str = '', finale_message: str = '') -> EndingDirection:
        category = category or ('preference' if quiz_type == 'preferencia' else 'general_knowledge')
        is_preference = quiz_type == 'preferencia' or category == 'preference'
        if is_preference:
            headline = 'SUAS ESCOLHAS FORAM DEMAIS!'
            supporting = finale_message or 'Conte nos comentários qual escolha foi a mais difícil!'
            primary = 'COMENTE SUAS ESCOLHAS!'
            secondary = 'VEJA SE SEUS AMIGOS ESCOLHERIAM O MESMO!'
            show_score = False
            show_comment = True
            celebration = 'choice_confetti'
            sequence = ('happy', 'point_left', 'wave')
        else:
            headline = 'VOCÊ COMPLETOU O QUIZ!'
            supporting = finale_message or 'Mandou muito bem! Quantas você conseguiu acertar?'
            primary = 'CONTE SUA PONTUAÇÃO NOS COMENTÁRIOS!'
            secondary = 'DESAFIE UM AMIGO A SUPERAR VOCÊ!'
            show_score = True
            show_comment = True
            celebration = 'golden_confetti'
            sequence = ('celebrate', 'point_right', 'wave')

        if production_mode == 'compact_high_energy':
            duration = min(float(duration), 5.0)
        else:
            duration = max(float(duration), 5.0)

        return EndingDirection(
            category=category,
            quiz_type=quiz_type,
            duration=round(min(duration, 6.5), 2),
            headline=headline,
            supporting_text=supporting,
            primary_cta=primary,
            secondary_cta=secondary,
            mascot_sequence=sequence,
            celebration_style=celebration,
            transition_style='logo_glow_fade',
            show_score_prompt=show_score,
            show_comment_prompt=show_comment,
            show_next_video_slot=True,
            show_subscribe_slot=True,
            curiosity_closer=self.CATEGORY_CLOSERS.get(category, self.CATEGORY_CLOSERS['general_knowledge']),
            metadata={'ending_version': '2.0', 'production_mode': production_mode},
        )
