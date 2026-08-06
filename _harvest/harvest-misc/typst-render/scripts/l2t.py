import re
def _grab(s,j):
    while j<len(s) and s[j]==' ': j+=1
    if j>=len(s) or s[j]!='{': return '',j
    depth=0; start=j
    while j<len(s):
        if s[j]=='{': depth+=1
        elif s[j]=='}':
            depth-=1
            if depth==0: return s[start+1:j], j+1
        j+=1
    return s[start+1:], j
def _fracs(s):
    out=[]; i=0
    while i<len(s):
        m=re.match(r'\\[dt]?frac', s[i:])
        if m:
            j=i+m.end(); a,j=_grab(s,j); b,j=_grab(s,j)
            out.append('frac(%s, %s)'%(_fracs(a), _fracs(b))); i=j
        else: out.append(s[i]); i+=1
    return ''.join(out)

_SKIP=set("frac product sum integral sqrt ln log exp min max times div dot op approx infinity dots plus minus arrow double left right cdot sin cos tan lim alpha beta gamma delta epsilon sigma mu rho theta lambda tau omega phi varphi pi Sigma Delta Omega Pi h c r".split())
def _wrapmulti(s):
    parts=re.split(r'("[^"]*")', s); out=[]
    for i,p in enumerate(parts):
        if i%2==1: out.append(p); continue
        def rp(m):
            w=m.group(0)
            return w if w in _SKIP or w.lower() in _SKIP else '"%s"'%w
        out.append(re.sub(r'[A-Za-z]{2,}', rp, p))
    return ''.join(out)

def latex_to_typst(s):
    s=s.strip()
    s=s.replace(r'\left[','[').replace(r'\right]',']').replace(r'\left(','(').replace(r'\right)',')').replace(r'\left|','|').replace(r'\right|','|').replace(r'\left.','').replace(r'\right.','')
    s=s.replace(r'\,',' ').replace(r'\;',' ').replace(r'\!','').replace(r'\quad','  ').replace(r'\ ',' ')
    s=_fracs(s)                                   # balanced frac FIRST
    s=re.sub(r'\\mathrm\{([^{}]*)\}', r'"\1"', s)
    s=re.sub(r'\\text(?:rm|bf|it)?\{([^{}]*)\}', r'"\1"', s)
    s=re.sub(r'\\operatorname\{([^{}]*)\}', r'"\1"', s)
    s=re.sub(r'\\sqrt\s*\{([^{}]*)\}', r'sqrt(\1)', s)
    s=s.replace(r'\prod','product').replace(r'\sum','sum').replace(r'\int','integral').replace(r'\cdots','dots.h.c').replace(r'\ldots','dots').replace(r'\dots','dots')
    for a,b in {r'\times':'times',r'\cdot':'dot.op',r'\div':'div',r'\pm':'plus.minus',r'\approx':'approx',r'\geq':'>=',r'\leq':'<=',r'\neq':'!=',r'\ne':'!=',r'\infty':'infinity',r'\ln':'ln ',r'\log':'log ',r'\exp':'exp ',r'\min':'min ',r'\max':'max ',r'\Rightarrow':'arrow.r.double',r'\rightarrow':'->',r'\to':'->'}.items(): s=s.replace(a,b)
    for g in ['alpha','beta','gamma','delta','epsilon','sigma','mu','rho','theta','lambda','tau','omega','phi','varphi','pi','Sigma','Delta','Omega','Pi']:
        s=re.sub(r'\\'+g+r'\b', g, s)
    for _ in range(5):
        n=re.sub(r'\^\{([^{}]*)\}', r'^(\1)', s); n=re.sub(r'_\{([^{}]*)\}', r'_(\1)', n)
        if n==s: break
        s=n
    s=s.replace('{','(').replace('}',')')
    s=re.sub(r'\\([A-Za-z]+)', r'\1', s); s=s.replace('\\','')
    s=_wrapmulti(s)
    return s
if __name__=='__main__':
    import sys; print(latex_to_typst(sys.argv[1]))
