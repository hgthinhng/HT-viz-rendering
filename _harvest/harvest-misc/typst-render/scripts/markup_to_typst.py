#!/usr/bin/env python3
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from l2t import latex_to_typst
TPL_IMPORT='#import "cfa_warm.typ": *\n#show: conf.with(level: "%s")\n\n'
def esc(t):
    for a,b in [('\\','\\\\'),('#','\\#'),('$','\\$'),('@','\\@'),('*','\\*'),('_','\\_'),('<','\\<'),('>','\\>'),('`','\\`')]:
        t=t.replace(a,b)
    return t
def inline(t):
    terms=[]
    def g(m): terms.append((m.group(1).strip(), m.group(2).strip())); return '\x00%d\x00'%(len(terms)-1)
    t=re.sub(r'\[T:\s*([^|\]]+)\|\s*([^\]]+)\]', g, t)
    t=esc(t)
    for i,(a,b) in enumerate(terms):
        t=t.replace('\x00%d\x00'%i, '#term[%s][%s]'%(a.replace(']','').replace('#','\\#'), b.replace(']','').replace('#','\\#')))
    return t
BOX={'BOX_EXAMPLE':'example','BOX_KEY':'key','BOX_WARN':'warn','BOX_NOTE':'note','INTUITION':'note','CHECK':'note'}
def emit(src, base):
    lines=src.split('\n'); out=[]; i=0; n=len(lines); first_sec=True
    def grab(close, st):
        buf=[]; j=st
        while j<n and not lines[j].strip().startswith(close): buf.append(lines[j]); j+=1
        return buf, j
    while i<n:
        s=lines[i].strip()
        if not s: i+=1; continue
        if s.startswith('[COVER:'):
            inn=s[7:].rstrip(']'); parts=[p.strip() for p in inn.split('|')]
            subj=parts[0] if parts else ''; mod=parts[1] if len(parts)>1 else ''; vi=parts[2] if len(parts)>2 else ''
            out.append('#cover(subject: [%s], module: [%s], vi: [%s], level: "I")'%(esc(subj),esc(mod),esc(vi))); i+=1; continue
        if s.startswith('[SECTION:'):
            inn=s[9:].rstrip(']'); parts=[p.strip() for p in inn.split('|')]
            en=parts[0]; vi=parts[1] if len(parts)>1 else ''
            if not first_sec: out.append('#pagebreak()')
            first_sec=False
            out.append('= %s'%esc(en))
            if vi: out.append('#gloss[%s]'%esc(vi))
            i+=1; continue
        if s.startswith('[SECTION_OPEN]'):
            buf,j=grab('[/SECTION_OPEN]', i+1); why=prev=''
            for b in buf:
                bs=b.strip()
                if bs.startswith('why_now:'): why=bs[8:].strip()
                elif bs.startswith('preview:'): prev=bs[8:].strip()
            i=j+1; continue  # SECTION_OPEN removed (AI-cringe); skip
        if s.startswith('[SUBSECTION:'):
            inn=s[12:].rstrip(']'); parts=inn.split('|'); en=parts[0].strip()
            vi=''
            if len(parts)>1:
                vi=parts[1].strip()
                if vi.lower().startswith('vi:'): vi=vi[3:].strip()
            out.append('== %s'%esc(en))
            if vi: out.append('#gloss[%s]'%esc(vi))
            i+=1; continue
        if s.startswith('[BODY]'):
            buf,j=grab('[/BODY]', i+1); txt=' '.join(b.strip() for b in buf if b.strip())
            out.append(inline(txt)); i=j+1; continue
        if s.startswith('[FORMULA'):
            buf,j=grab('[/FORMULA]', i+1); eqs=[]; leg=[]; inw=False
            for b in buf:
                bs=b.strip()
                if not bs: continue
                if bs.lower().startswith('where'): inw=True; continue
                if inw: leg.append(bs)
                elif not bs.startswith('@'): eqs.append(bs)
            for e in eqs:
                out.append('#align(center)[$ %s $]'%latex_to_typst(e))
            if leg:
                parts=[]
                for lg in leg:
                    if '=' in lg:
                        sym,desc=lg.split('=',1); desc=desc.split('|')[0].strip()
                        parts.append('#text(fill: teal, weight:"bold")[%s] = %s'%(esc(sym.strip()), esc(desc)))
                out.append('#text(9pt, fill: mute)[%s]'%('  ·  '.join(parts)))
            i=j+1; continue
        boxtag=None
        for tg in BOX:
            if s.startswith('['+tg): boxtag=tg; break
        if boxtag:
            buf,j=grab('[/'+boxtag+']', i+1); kind=BOX[boxtag]
            content=' #linebreak() '.join(inline(b.strip()) for b in buf if b.strip())
            out.append('#callout(kind: "%s")[%s]'%(kind, content)); i=j+1; continue
        if s.startswith('[RECAP_HANDOFF]'):
            buf,j=grab('[/RECAP_HANDOFF]', i+1); rc=hd=''
            for b in buf:
                bs=b.strip()
                if bs.startswith('recap:'): rc=bs[6:].strip()
                elif bs.startswith('handoff:'): hd=bs[8:].strip()
            body='*Tóm lại.* %s'%inline(rc)
            if hd: body+=' #linebreak() #linebreak() *Tiếp theo.* %s'%inline(hd)
            out.append('#callout(kind: "key")[%s]'%body); i=j+1; continue
        if s.startswith('[TABLE'):
            cap=''; m=re.match(r'\[TABLE:\s*(.*?)\]', s)
            if m: cap=m.group(1).strip()
            buf,j=grab('[/TABLE]', i+1); hdr=[]; rows=[]
            for b in buf:
                bs=b.strip()
                if bs.startswith('header:'): hdr=[c.strip() for c in bs[7:].split('|')]
                elif bs.startswith('row:'): rows.append([c.strip() for c in bs[4:].split('|')])
            if hdr:
                hs='('+', '.join('[%s]'%esc(h) for h in hdr)+',)'
                rs='('+', '.join('('+', '.join('[%s]'%esc(c) for c in r)+',)' for r in rows)+',)'
                out.append('#cfatable(%s, %s, caption: [%s])'%(hs, rs, esc(cap)))
            i=j+1; continue
        if s.startswith('[FIGURE:'):
            inn=s[8:].rstrip(']'); parts=inn.split('|'); path=parts[0].strip(); cap=parts[1].strip() if len(parts)>1 else ''
            ap=os.path.join(base, path)
            if os.path.exists(ap): out.append('#figure(image("%s", width: 80%%), caption: [%s])'%(ap, esc(cap)))
            else: out.append('#callout(kind:"note")[FIGURE (chèn ảnh): %s]'%esc(cap))
            i+=1; continue
        i+=1
    return '\n\n'.join(out)
if __name__=='__main__':
    src_path=sys.argv[1]; base=os.path.dirname(os.path.abspath(src_path))
    body=emit(open(src_path,encoding='utf-8').read(), base)
    open(sys.argv[2],'w',encoding='utf-8').write(TPL_IMPORT%'I'+body)
    print("wrote", sys.argv[2])
