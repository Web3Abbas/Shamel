#!/bin/bash
# Generate + render the scope PDF, increasing per-section height factors until no page overflows.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
PDF="$(dirname "$HERE")"
OUT="${1:-$HERE/scope-test.pdf}"
SHOTS="${2:-}"
[ -f "$HERE/fit.json" ] || echo '{}' > "$HERE/fit.json"
for i in 1 2 3 4 5 6 7 8; do
  python3 "$HERE/gen.py"
  if [ -n "$SHOTS" ]; then R=$(cd "$PDF" && node render-overview.mjs "$HERE/scope.html" "$OUT" --title "Shamel Pro API — Capabilities & Scope" --shots "$SHOTS"); else R=$(cd "$PDF" && node render-overview.mjs "$HERE/scope.html" "$OUT" --title "Shamel Pro API — Capabilities & Scope"); fi
  echo "$R" | python3 -c "
import json,sys
r=json.loads(sys.stdin.read())
fit=json.load(open('$HERE/fit.json'))
over=r['overflow']
print('round $i pages', r['pages'], 'overflow', [(o['id'],o['over_px']) for o in over], 'errors', r['errors'][:3])
changed=False
for o in over:
    sec=o['id'].rsplit('-',1)[0] if '-' in o['id'] else o['id']
    if sec in ('glance','how','map','matrix','writes','bawaba','apC',''):
        continue
    fit[sec]=round(fit.get(sec,1.0)*1.07,3); changed=True
json.dump(fit,open('$HERE/fit.json','w'))
sys.exit(0 if (not over or not changed) else 3)
" && break || true
done
