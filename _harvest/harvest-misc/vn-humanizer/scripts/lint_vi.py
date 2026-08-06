#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_vi.py — lint AI-tells cho văn tiếng Việt (vn-humanizer).
Usage: python3 lint_vi.py <file.txt|.md> [--register R2] [--json]
Registers: R1a tin | R1b phân tích | R2 học thuật | R3 SEO | R4 social | R5 email | R6 báo cáo | R7 blog | R8 kỹ thuật
Nguyên tắc: đây là CÒI BÁO KHÓI — hit = chỗ cần NGƯỜI/model nhìn lại, không phải lỗi tự động."""
import re, sys, json, statistics, unicodedata

PATTERNS = {
 'opener_ai':   (r'(Trong bối cảnh|Trong thế giới|kỷ nguyên số|Hãy cùng (tìm hiểu|khám phá)|Chào mừng bạn|Dưới đây là)', {}),
 'parallel':    (r'(không chỉ[^.\n]{0,60}mà còn|không phải[^.\n]{0,40}mà là)', {}),
 'hedging_rong':(r'(Điều quan trọng cần lưu ý|có thể nói rằng|Đáng chú ý là|Điều đáng lưu ý)', {}),
 'ket_thua':    (r'(Tóm lại|Nhìn chung|Như vậy,? (ta|chúng ta) (thấy|có thể thấy))', {'R2':'ok','R1b':'ok'}),
 'connector':   (r'(Hơn nữa|Bên cạnh đó|Thêm vào đó|Ngoài ra)', {'density_per_1000': 1.0}),
 'editorial':   (r'(đóng vai trò (quan trọng|then chốt)|là minh chứng cho|đánh dấu bước ngoặt|nâng tầm|đi sâu vào|bức tranh toàn cảnh|mở ra kỷ nguyên|tạo (ra )?giá trị)', {}),
 'passive_boi': (r'được [^.\n]{0,30} bởi', {'R6':'ok'}),
 'mot_cach':    (r'một cách [a-zà-ỹ]+', {}),
 'dieu_ma':     (r', điều (mà|này)', {}),
 'self_qa':     (r'(\? Nó có nghĩa|\? Câu trả lời là|Vậy điều này có nghĩa|\? Nghĩa là)', {}),
 'enthusiasm':  (r'(Thật thú vị|đầy hấp dẫn|Câu hỏi rất hay)', {}),
 'chat_frame':  (r'(dựa trên thông tin bạn cung cấp|Để tôi phân tích|Hy vọng bài viết (này )?giúp)', {}),
 'kinh_gui_sai':(r'(Kính gửi|Trân trọng,)', {'R5':'ok','R6':'ok'}),
 'em_dash':     (r'—', {'density_per_1000': 1.5}),
 'ban_day_dac': (r'\bbạn\b', {'density_per_1000': 8.0, 'R4':'ok'}),
 'liet_ke_3':   (r'[^,.\n;:()]{3,40}, [^,.\n;:()]{3,40},? (và|hay|hoặc|lẫn) [^,.\n;:()]{3,40}', {'density_per_1000': 2.5}),
}

def bullet_ratio(text):
    lines=[l for l in text.splitlines() if l.strip()]
    if len(lines)<8: return None
    b=sum(1 for l in lines if l.lstrip()[:2] in ('- ','* ','• ') or __import__('re').match(r'\s*\d+[.)] ', l))
    return round(b/len(lines),2)

def sent_cv(text):
    sents=[s for s in re.split(r'[.!?…]\s', text) if 4<len(s.split())<80]
    if len(sents)<15: return None, len(sents)
    L=[len(s.split()) for s in sents]
    return round(statistics.pstdev(L)/statistics.mean(L),2), len(sents)

def para_cv(text):
    paras=[p for p in re.split(r'\n\s*\n', text) if len(p.split())>10]
    if len(paras)<4: return None
    L=[len(p.split()) for p in paras]
    return round(statistics.pstdev(L)/statistics.mean(L),2)

def top_ngrams(text, n=3, k=8):
    words=re.sub(r'[^\wà-ỹÀ-Ỹ ]',' ',text.lower()).split()
    from collections import Counter
    grams=Counter(tuple(words[i:i+n]) for i in range(len(words)-n))
    return [(" ".join(g),c) for g,c in grams.most_common(k) if c>=3]

def main():
    args=[a for a in sys.argv[1:] if not a.startswith('--')]
    reg=None
    for i,a in enumerate(sys.argv):
        if a=='--register' and i+1<len(sys.argv): reg=sys.argv[i+1]
    as_json='--json' in sys.argv
    text=unicodedata.normalize('NFC', open(args[0],encoding='utf-8',errors='replace').read())
    words=len(text.split())
    report={'file':args[0],'words':words,'register':reg,'hits':{},'notes':[]}
    for fam,(pat,meta) in PATTERNS.items():
        if reg and meta.get(reg)=='ok':
            continue  # hợp lệ ở register này
        found=re.findall(pat,text)
        c=len(found)
        if not c: continue
        dens=round(c*1000/max(words,1),2)
        thresh=meta.get('density_per_1000')
        flag = (dens>thresh) if thresh else True
        if flag: report['hits'][fam]={'count':c,'per_1000':dens}
    cv,ns=sent_cv(text)
    if cv is not None:
        report['sent_cv']=cv; report['n_sents']=ns
        if cv<0.35: report['notes'].append(f'NHỊP MÁY: sent_cv={cv} (<0.35; người thường 0.45-0.70)')
    pcv=para_cv(text)
    if pcv is not None:
        report['para_cv']=pcv
        if pcv<0.30: report['notes'].append(f'ĐOẠN ĐỀU TĂM TẮP: para_cv={pcv}')
    br=bullet_ratio(text)
    if br is not None and br>0.30 and reg not in ('R8',):
        report['notes'].append(f'LIST-ITIS: {int(br*100)}% dòng là bullet/đánh số (prose là mặc định; R8 kỹ thuật được miễn)')
    if 'liet_ke_3' in report['hits']:
        report['notes'].append('RULE-OF-3: mật độ liệt kê "X, Y và Z" cao — đổi số item 1/2/4, làm vế lệch độ dài (Tier 2)')
    tg=top_ngrams(text)
    if tg: report['repeated_3grams']=tg[:5]
    if as_json: print(json.dumps(report,ensure_ascii=False,indent=1))
    else:
        print(f"== lint_vi: {args[0]} | {words} từ | register={reg or 'chưa khai (verdict có thể sai!)'}")
        for fam,v in report['hits'].items(): print(f"  {fam:<14} {v['count']:>3} hits  ({v['per_1000']}/1000w)")
        if 'sent_cv' in report: print(f"  sent_cv={report['sent_cv']} ({report['n_sents']} câu)  para_cv={report.get('para_cv')}")
        for n in report['notes']: print("  ⚠", n)
        if report.get('repeated_3grams'):
            print("  3-gram lặp (ứng viên tic):", ", ".join(f"'{g}'×{c}" for g,c in report['repeated_3grams']))
        print("  Nhắc: hit = chỗ cần nhìn lại theo REGISTER_MAP, không phải lỗi tự động.")
if __name__=='__main__': main()
