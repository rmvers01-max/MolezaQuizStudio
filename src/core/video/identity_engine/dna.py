from .models import ChannelDNA

def moleza_quiz_dna():
    return ChannelDNA(
        channel_code="moleza_quiz",channel_name="Moleza Quiz",
        personality=("divertido","acolhedor","colorido","organizado","familia"),
        accent_color=(255,215,65),text_color=(55,35,95),
        maximum_motion=.92,maximum_vignette=.20,maximum_particles=.76,
        metadata={"dna_version":"1.0","principle":"Energia com clareza."},
    )
