#!/usr/bin/env python3
"""Compile Pages CMS JSON entries into a static manifest for Netlify."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
items=[]
for file in sorted((root/'content/projects').glob('*.json')):
    try:
        obj=json.loads(file.read_text(encoding='utf-8'))
        if not isinstance(obj,dict): continue
        image=str(obj.get('image','')).strip()
        # Pages CMS normally stores absolute public URLs such as /images/a.jpg.
        if image.startswith('images/'): image='/'+image
        if not image.startswith('/images/') or '..' in image.split('/'):
            print(f'Skipping {file.name}: unsafe or missing image path')
            continue
        items.append({
            'title':str(obj.get('title','Project'))[:160],
            'category':str(obj.get('category','Interior')),
            'image':image,
            'description':str(obj.get('description',''))[:500],
            'status':str(obj.get('status','Finished')),
        })
    except (ValueError,OSError) as exc:
        print(f'Skipping {file.name}: {exc}')
(root/'gallery-data.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Wrote {len(items)} projects')
