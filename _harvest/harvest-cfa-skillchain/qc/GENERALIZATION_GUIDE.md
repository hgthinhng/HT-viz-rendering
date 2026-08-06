# Generalization Guide — note-pipeline-audit

When an audit finding is one-off vs systemic, and how to elevate to skill rules.

## Decision tree

For each finding from Phase B audit:

```
Finding appears in:
├── 1 location → Single instance
│   └── Note in report; do NOT generalize
├── 2 locations → Borderline
│   └── Note + recommend agent prompt update (not validator)
└── 3+ locations → SYSTEMIC
    └── Propose ONE of:
        ├── New validator rule (E## or W## code)
        ├── Agent prompt update for Phase 1.3 / 1.4
        └── Render engine patch
```

## When to add validator rule

Add E (error, blocks render) when:
- Pattern is unambiguously wrong (e.g., foreign-language word, broken tag pair)
- Auto-detection regex is reliable (low false positive)
- Fix is purely mechanical (can't merge BODY semantically via script)

Add W (warning, advisory) when:
- Pattern is suboptimal but not always wrong (e.g., 4+ consecutive BODY)
- Heuristic-based (some false positives expected)
- Author judgment required to fix

## When to update agent prompt

Update Phase 1.3 (teaching script writer) prompt when:
- Issue is content-quality (not structural)
- Examples: voice warmth, sentence variety, narrative flow, example density
- Phase 1.3 agent has full context of section being written

Update Phase 1.4 (markup conversion) prompt when:
- Issue is markup-structural (which tag to use)
- Examples: when to RUNIN vs BODY, when (i)(ii)(iii) → TABLE
- Phase 1.4 agent has prose ready and decides format

## When to patch render engine

Patch render_engine.py when:
- Visual rendering of valid markup is suboptimal
- Examples: spacing, page break, tab, color, font size
- Markup convention works but visual output needs adjustment

## Examples from EQ_M1 audit

### Foreign-language word leak ("memiliki")
- Appeared in 1 section but maker missed
- Validator rule **E18**: catches Indonesian/Malay/Tagalog regex
- Decision: **VALIDATOR** (high confidence, mechanical)

### 4+ consecutive [BODY] blocks
- Appeared 16x across module
- Auto-fixing with DIVIDER injection caused noise
- Decision: **WARNING + agent prompt** (W08 + Phase 1.4 rule "merge or use INTUITION/BOX, NEVER auto-DIVIDER")

### Subsection format inconsistency
- Half use `vi:` prefix, half don't
- Decision: **RENDER ENGINE PATCH** (parser accepts both formats — done) + **AGENT PROMPT** (use consistent format)

### RUNIN missing for sequential listings (Bước, Lực, etc.)
- Appeared 13+ times across module
- Decision: **WARNING W16** (advisory, agent should convert) + **AGENT PROMPT** (Phase 1.4 must convert sequential listings to RUNIN)

### Inline (i)(ii)(iii) listing
- Appeared 3+ times
- Decision: **WARNING W15** (suggest TABLE extraction) + **AGENT PROMPT**

### BOX_PURPLE without Layout/Elements/Relationships
- Appeared 2x in older versions
- Decision: **WARNING** (structure compliance check) + **TEMPLATE in skill reference** (BOX_GUIDE.md)

## Anti-patterns (do NOT do)

1. **Don't add validator rule for one-off finding** — too noisy, low signal
2. **Don't update agent prompt for mechanical issue** — validator catches it more reliably
3. **Don't patch render engine for content issue** — engine should be content-agnostic
4. **Don't propose new skill for single category fix** — only propose new skill if 3+ categories need new tooling

## Output format for skill update proposals

In `_skill_updates.md`:

```markdown
## Proposed validator rules

### E19 (or W17) — {Description}
**Detection**: {regex or heuristic}
**Severity**: Error / Warning
**Trigger location**: in {block type}
**Example**: {sample finding}

## Proposed agent prompt updates

### Phase 1.3 (teaching script writer)
Add to prompt: "{exact instruction}"
**Reason**: {why}
**Examples to give agent**: {good vs bad}

### Phase 1.4 (markup conversion)
Add to prompt: "{exact instruction}"
**Reason**: {why}

## Proposed render engine patches

### Patch 1: {description}
**File**: render_engine.py
**Function**: {name}
**Change**: {description}
**Reason**: {why}
```

User reads `_skill_updates.md` and decides which to apply.
