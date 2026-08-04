from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import math
import struct
import wave

from moviepy import AudioFileClip


@dataclass(frozen=True, slots=True)
class AudioCue:
    cue_type: str
    start: float
    volume: float
    path: Path
    experience_code: str = "discovery_01"
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "cue_type": self.cue_type,
            "start": self.start,
            "volume": self.volume,
            "path": str(self.path),
            "experience_code": self.experience_code,
            "metadata": dict(self.metadata),
        }


class ProceduralSfxSynthesizer:
    """Cria efeitos WAV leves quando o projeto ainda não possui SFX próprios."""

    SAMPLE_RATE = 44100

    def ensure(self, root: Path, cue_type: str) -> Path | None:
        folder = root / "cache" / "audio_experience"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{cue_type}.wav"
        if path.exists():
            return path
        builders = {
            "discovery_in": self._discovery,
            "suspense_tick": self._tick,
            "competition_whoosh": self._whoosh,
            "victory_hit": self._victory,
            "calm_release": self._calm,
            "reveal_soft": self._reveal,
        }
        builder = builders.get(cue_type)
        if builder is None:
            return None
        samples = builder()
        self._write(path, samples)
        return path

    def _write(self, path: Path, samples):
        with wave.open(str(path), "w") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(self.SAMPLE_RATE)
            frames = bytearray()
            for value in samples:
                value = max(min(float(value), 1.0), -1.0)
                frames.extend(struct.pack("<h", int(value * 32767)))
            handle.writeframes(bytes(frames))

    def _tone(self, duration, start_freq, end_freq=None, volume=.4, decay=2.2):
        end_freq = start_freq if end_freq is None else end_freq
        total = int(self.SAMPLE_RATE * duration)
        phase = 0.0
        out=[]
        for i in range(total):
            p=i/max(total-1,1)
            freq=start_freq+(end_freq-start_freq)*p
            phase += 2*math.pi*freq/self.SAMPLE_RATE
            env=(1-p)**decay
            attack=min(p/0.04,1.0)
            out.append(math.sin(phase)*volume*env*attack)
        return out

    def _mix(self,*tracks):
        n=max(len(t) for t in tracks)
        out=[0.0]*n
        for track in tracks:
            for i,v in enumerate(track): out[i]+=v
        peak=max(max(abs(v) for v in out),1.0)
        return [v/peak for v in out]

    def _discovery(self): return self._mix(self._tone(.38,420,820,.34,1.7), self._tone(.42,630,980,.20,2.2))
    def _tick(self): return self._tone(.10,1250,920,.34,4.0)
    def _whoosh(self): return self._tone(.46,180,1250,.30,1.15)
    def _victory(self): return self._mix(self._tone(.62,520,780,.34,1.6), self._tone(.72,780,1180,.26,1.8), self._tone(.28,120,85,.26,2.4))
    def _calm(self): return self._mix(self._tone(.55,520,420,.18,1.5), self._tone(.60,660,540,.12,1.7))
    def _reveal(self): return self._mix(self._tone(.35,480,760,.28,1.8), self._tone(.40,720,1040,.17,2.1))


class AudioExperienceDirector:
    def choose(self, *, scene_kind, difficulty, surprise, pattern_break, emotional_tone, final_zone=False):
        tone=str(emotional_tone or '').lower()
        if scene_kind=='reveal' and (surprise or final_zone or tone=='victory'):
            return {'experience_code':'victory_01','cue_type':'victory_hit','volume':.34,'music_duck':.18}
        if scene_kind=='countdown' or difficulty>=72 or tone=='suspense':
            return {'experience_code':'suspense_01','cue_type':'suspense_tick','volume':.18,'music_duck':.06}
        if pattern_break or tone in {'challenge','competition'}:
            return {'experience_code':'competition_01','cue_type':'competition_whoosh','volume':.28,'music_duck':.10}
        if tone in {'relief','calm'}:
            return {'experience_code':'calm_01','cue_type':'calm_release','volume':.16,'music_duck':.04}
        return {'experience_code':'discovery_01','cue_type':'discovery_in','volume':.20,'music_duck':.05}


class AudioSyncDirector:
    """Sincroniza efeitos existentes ou gera fallbacks procedurais."""

    CANDIDATES = {
        "question_in": ("assets/sfx/question_in.wav","assets/sfx/question_in.mp3","assets/sfx/card_in.wav","assets/sfx/card_in.mp3","assets/sounds/question_in.wav"),
        "tick": ("assets/sfx/tick.wav","assets/sfx/tick.mp3","assets/sounds/tick.wav"),
        "reveal": ("assets/sfx/reveal.wav","assets/sfx/reveal.mp3","assets/sfx/correct.wav","assets/sfx/correct.mp3","assets/sounds/reveal.wav"),
        "pattern_break": ("assets/sfx/pattern_break.wav","assets/sfx/pattern_break.mp3","assets/sfx/whoosh.wav","assets/sfx/whoosh.mp3"),
        "victory_hit": ("assets/sfx/victory_hit.wav","assets/sfx/victory.wav","assets/sfx/correct.wav"),
        "calm_release": ("assets/sfx/calm_release.wav","assets/sfx/soft_release.wav"),
    }

    def __init__(self):
        self.experience_director=AudioExperienceDirector()
        self.synth=ProceduralSfxSynthesizer()
        self.last_report=None

    def build_question_cues(self, *, project_root, question_number, total_questions, question_start, question_duration, response_time, reveal_duration, difficulty=50.0, surprise=False, emotional_tone='', force_pattern_break=False):
        root=Path(project_root)
        cues=[]
        interval=3 if total_questions<=10 else 4 if total_questions<=24 else 5
        pattern_break=bool(force_pattern_break or (question_number>1 and question_number%interval==0))
        final_zone=question_number>=max(total_questions-1,1)

        question_exp=self.experience_director.choose(scene_kind='question',difficulty=difficulty,surprise=surprise,pattern_break=pattern_break,emotional_tone=emotional_tone,final_zone=final_zone)
        qpath=self._find(root,'pattern_break' if pattern_break else 'question_in') or self.synth.ensure(root,question_exp['cue_type'])
        if qpath:
            cues.append(AudioCue(question_exp['cue_type'],float(question_start+.04),question_exp['volume'],qpath,question_exp['experience_code'],{'music_duck':question_exp['music_duck']}))

        countdown_start=question_start+question_duration
        tickpath=self._find(root,'tick') or self.synth.ensure(root,'suspense_tick')
        if tickpath:
            for offset in range(max(int(response_time),0)):
                intensity=.17 + .035*(offset/max(int(response_time)-1,1))
                cues.append(AudioCue('suspense_tick',float(countdown_start+offset),intensity,tickpath,'suspense_01',{'countdown_index':offset+1}))

        reveal_start=question_start+question_duration+response_time
        reveal_exp=self.experience_director.choose(scene_kind='reveal',difficulty=difficulty,surprise=surprise,pattern_break=False,emotional_tone=emotional_tone,final_zone=final_zone)
        rkey='victory_hit' if reveal_exp['experience_code']=='victory_01' else 'reveal'
        rpath=self._find(root,rkey) or self.synth.ensure(root,reveal_exp['cue_type'] if reveal_exp['cue_type']!='discovery_in' else 'reveal_soft')
        if rpath:
            cues.append(AudioCue(reveal_exp['cue_type'],float(reveal_start),reveal_exp['volume'],rpath,reveal_exp['experience_code'],{'music_duck':reveal_exp['music_duck']}))

        self.last_report={
            'audio_experience_version':'1.0',
            'question_number':question_number,
            'difficulty':difficulty,
            'surprise':surprise,
            'emotional_tone':emotional_tone,
            'pattern_break':pattern_break,
            'cues':[cue.to_dict() for cue in cues],
            'note':'Efeitos próprios têm prioridade; WAV procedurais são usados somente como fallback.',
        }
        return cues

    def create_clips(self,cues):
        clips=[]
        for cue in cues:
            try:
                clip=AudioFileClip(str(cue.path)).with_volume_scaled(cue.volume).with_start(cue.start)
            except Exception:
                continue
            clips.append(clip)
        return clips

    def save_report(self,path):
        if self.last_report is None: return None
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(self.last_report,ensure_ascii=False,indent=2),encoding='utf-8')
        return path

    def _find(self,project_root,cue_type):
        for relative in self.CANDIDATES.get(cue_type,()):
            for candidate in (Path(relative),project_root/relative):
                if candidate.exists(): return candidate
        return None
