from core.video import VideoGenerator
generator=VideoGenerator()
report=generator.core_engine.validate()
print("healthy:",report["healthy"])
print("score:",report["score"])
print("services:")
for name in report["registered_services"]: print("-",name)
print("pipeline:")
for name in generator.core_engine.pipeline.stages(): print("-",name)
assert report["healthy"] is True
print("AAA CORE ENGINE OK")
