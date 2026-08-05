from core.video.opening.opening_studio import OpeningStudio
studio=OpeningStudio(largura=1280,altura=720,fps=24)
engine=studio._get_performance_engine()
print("_get_performance_engine:", hasattr(OpeningStudio,"_get_performance_engine"))
print("performance_engine:", engine is not None)
print("perfil:", engine.profile.code)
print("OPENING PERFORMANCE ENGINE OK")
