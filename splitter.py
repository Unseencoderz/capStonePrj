# Run this in the same directory where you've saved the canvas content file.
# If you copied the canvas content into 'actionable_meeting_agent_files.py', run the splitter below.

content = open('actionable_meeting_agent_files.py','r',encoding='utf-8').read()
parts = content.split('\\n# === FILE:')
for p in parts:
    if p.strip()=='':
        continue
    # the first part may be header; skip if no filename marker
    if p.startswith(' agents.py') or p.startswith(' agents.py') or p.startswith(' agents.py') or 'FILE:' in p:
        # ensure robust parsing
        pass

# Simpler robust splitter:
import re
blocks = re.split(r\"\\n# === FILE: (.+?) ===\\n\", content)
# blocks: [preheader, filename1, body1, filename2, body2, ...]
for i in range(1, len(blocks), 2):
    fname = blocks[i].strip()
    body = blocks[i+1]
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(body)
    print('Wrote', fname)
