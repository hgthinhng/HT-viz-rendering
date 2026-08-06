// cfa_warm.typ — preamble "design ấm" cho CFA note (Typst). #import "cfa_warm.typ": *
#let ink   = rgb("#14213D")
#let teal  = rgb("#1C5D72")
#let gold  = rgb("#9A7B3F")
#let paper = rgb("#FAFAF7")
#let body  = rgb("#23262B")
#let mute  = rgb("#6B7078")

#let conf(title: "", subject: "", level: "I", doc) = {
  set page(paper: "a4", fill: paper, margin: (x: 2.2cm, top: 2cm, bottom: 1.8cm),
    footer: context [ #set text(8pt, fill: mute); #line(length: 100%, stroke: 0.4pt + gold); #v(2pt)
                      #align(center)[#counter(page).display()] ])
  set text(font: "Lato", size: 10.5pt, fill: body, lang: "vi")
  set par(justify: true, leading: 0.72em, spacing: 1.0em)
  show heading.where(level: 1): it => { set text(font: "Lora", fill: teal, size: 19pt); block(below: 6pt, it)
    place(dx: 0pt, dy: 2pt)[#line(length: 4.5cm, stroke: 1.4pt + gold)] ; v(8pt) }
  show heading.where(level: 2): set text(font: "Lora", fill: ink, size: 14pt)
  show heading.where(level: 3): set text(font: "Lato", fill: teal, size: 11.5pt, weight: "bold")
  doc
}
// callout box: #callout(kind:"example"|"key"|"warn"|"note")[ ... ]
#let callout(kind: "note", b) = {
  let bar = (example: teal, key: gold, warn: rgb("#C2762B"), note: rgb("#8A9098")).at(kind, default: teal)
  let bg  = (example: rgb("#EEF2F5"), key: rgb("#F4EFE3"), warn: rgb("#FBEEDD"), note: rgb("#EFF1F2")).at(kind, default: rgb("#EEF2F5"))
  let lab = (example: "EXAMPLE", key: "KEY IDEA", warn: "GHI CHÚ BỔ SUNG", note: "NOTE").at(kind, default: "NOTE")
  block(fill: bg, inset: 9pt, radius: 3pt, stroke: (left: 2.5pt + bar), width: 100%, breakable: false)[
    #text(7.5pt, weight: "bold", fill: gold, tracking: 0.6pt)[#lab] #linebreak() #b ]
}
// song ngữ term-first: #term[English][gloss Việt]
#let term(en, vi) = [#text(weight: "bold", fill: teal)[#en] (#vi)]
// cover đơn giản
#let cover(subject: "", module: "", vi: "", level: "I") = {
  v(5cm)
  text(font: "Lato", 11pt, weight: "bold", fill: gold, tracking: 2pt)[CFA PROGRAM · LEVEL #level]; v(10pt)
  text(font: "Lato", 13pt, weight: "bold", fill: teal, tracking: 1.5pt)[#upper(subject)]; v(2pt)
  line(length: 4cm, stroke: 1.4pt + gold); v(14pt)
  text(font: "Lora", 33pt, weight: "bold", fill: ink)[#module]; v(4pt)
  text(font: "Lora", 15pt, style: "italic", fill: teal)[#vi]
  pagebreak()
}

// bảng kiểu note: header teal, zebra, kẻ ngang mảnh
#let cfatable(headers, rows, caption: none) = block(width: 100%, breakable: true)[
  #if caption != none { text(9.5pt, weight: "bold", fill: teal, tracking: 0.4pt)[#upper(caption)]; v(3pt) }
  #table(
    columns: headers.len(),
    align: left + horizon,
    inset: 6pt,
    stroke: (x, y) => (top: if y == 0 { 1pt + ink } else { 0pt }, bottom: 0.5pt + rgb("#C9CDD3")),
    fill: (x, y) => if y == 0 { teal } else if calc.even(y) { rgb("#F2F5F7") } else { none },
    table.header(..headers.map(h => text(fill: white, weight: "bold", size: 9.5pt)[#h])),
    ..rows.flatten().map(c => text(size: 9.5pt, fill: body)[#c]),
  )
]
// gloss tiếng Việt dưới heading
#let gloss(t) = text(font: "Lora", style: "italic", size: 10pt, fill: mute)[#t]
// section opener
#let opener(why, preview) = block(fill: rgb("#EAF1F3"), inset: 9pt, radius: 3pt, stroke: (left: 2.5pt + teal), width: 100%)[
  #text(7.5pt, weight: "bold", fill: gold, tracking: 0.6pt)[VÌ SAO BÂY GIỜ] #linebreak() #why #linebreak() #linebreak()
  #text(7.5pt, weight: "bold", fill: gold, tracking: 0.6pt)[TRONG PHẦN NÀY] #linebreak() #preview ]
