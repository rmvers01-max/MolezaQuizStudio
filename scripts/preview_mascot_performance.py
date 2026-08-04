from __future__ import annotations
import argparse, json, sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument('--projeto',default='.'); p.add_argument('--cena',default='question'); args=p.parse_args()
    root=Path(args.projeto).resolve(); sys.path.insert(0,str(root/'src'))
    from core.video.mascot_actor import MascotPerformanceDirector, MascotActorReportWriter
    perf=MascotPerformanceDirector().create_performance(scene_kind=args.cena,question_number=1,duration=4,difficulty=70,surprise=args.cena=='reveal',correct_reveal=args.cena=='reveal')
    out=root/'videos'/'relatorios'/'mascot_actor_report.json'; MascotActorReportWriter().save(perf,out)
    print(json.dumps(perf.to_dict(),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
