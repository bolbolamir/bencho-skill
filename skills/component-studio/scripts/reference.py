#!/usr/bin/env python3
"""Return only the Bencho reference entries relevant to a component request."""
import argparse
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('query', nargs='+')
parser.add_argument('--limit', type=int, default=5)
args = parser.parse_args()
terms = set(re.findall(r'[a-z0-9]+', ' '.join(args.query).lower()))
catalog = json.loads((Path(__file__).resolve().parents[1] / 'assets/bencho-catalog.json').read_text())
scored = []
for item in catalog['components']:
    name = set(re.findall(r'[a-z0-9]+', (item['name'] + ' ' + item['slug']).lower()))
    body = set(re.findall(r'[a-z0-9]+', (item['behavior_notes'] + ' ' + item['observed_control_summary']).lower()))
    score = 4 * len(terms & name) + len(terms & body)
    if score:
        scored.append((score, item))
scored.sort(key=lambda pair: (-pair[0], pair[1]['name']))
print(json.dumps({'source': catalog['source'], 'matches': [item for _, item in scored[:max(1, min(args.limit, 12))]]}, ensure_ascii=False, indent=2))
