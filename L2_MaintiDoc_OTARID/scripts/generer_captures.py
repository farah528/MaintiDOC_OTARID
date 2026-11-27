from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv
root=Path(__file__).parents[1]; out=root/'resultats'/'captures'; out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((root/'resultats'/'resultats_evaluation.csv').open(encoding='utf-8')))
examples=[('recherche_texte.png','Q01','texte_seul'),('recherche_photo.png','Q11','texte_images'),('acces_refuse.png','Q18','texte_seul')]
for fn,q,cfg in examples:
    r=next(x for x in rows if x['question_id']==q and x['configuration']==cfg)
    im=Image.new('RGB',(1200,650),'white'); d=ImageDraw.Draw(im); d.text((40,30),f'MAINTiDOC - capture de test local - {q}',fill='navy'); d.text((40,80),f'Configuration: {cfg}',fill='black'); d.text((40,125),'Attendus: '+r['attendus'],fill='black'); d.text((40,180),'Résultats: '+r['resultats'],fill='black'); d.text((40,235),f"Hit@5: {r['hit_at_5']}   (fallback local, sans Qdrant/CLIP)",fill='darkgreen' if r['hit_at_5']=='1' else 'darkred'); im.save(out/fn)
