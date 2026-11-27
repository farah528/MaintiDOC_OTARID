from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root=Path(__file__).parents[1]; name='L2_MaintiDoc_OTARID'; archive=root/f'{name}.zip'
files=['L2_MaintiDoc_OTARID_Rapport.pdf','L2_MaintiDoc_OTARID_Veille.pdf','L2_MaintiDoc_OTARID_LienGitHub.txt','README.md']
files += [str(p.relative_to(root)).replace('\\','/') for p in (root/'resultats').rglob('*') if p.is_file()]
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
    for rel in files: z.write(root/rel, f'{name}/{rel}')
with ZipFile(archive) as z:
    names=z.namelist(); assert all(n.startswith(name+'/') for n in names); assert any(n.endswith('README.md') for n in names); print(f'{archive} verified: {len(names)} files')
