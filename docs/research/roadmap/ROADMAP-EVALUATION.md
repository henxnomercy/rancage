# RANCAGE Roadmap Evaluation & Strategic Recommendations

**Document type:** Evaluation + Strategic Input  
**Date:** 17 November 2026  
**Status:** Draft for internal review  
**Based on:** Full language review + feature prioritization discussion

---

## 1. Executive Summary

RANCAGE currently sits at a solid early-stage foundation (v0.1 baseline + 0.2.0-alpha.1 packaging work). The documentation quality, honesty about current limitations, and hybrid architecture vision are genuine strengths.

However, the language is still too limited to be practically useful for real programs. The most urgent work is completing fundamental language features. Longer-term differentiation should focus on **security-by-design** and **true multi-target semantic guarantees** — two areas where almost no mainstream languages compete seriously.

---

## 2. Current State Assessment

### Strengths
- Excellent, transparent, and realistic documentation
- Clear hybrid compilation vision (stable frontend → RANCAGE-IR → multiple backends)
- Early security thinking (bounded VM, instruction budget, no ambient authority)
- Windows standalone packaging pipeline already started
- Hybrid licensing model already designed

### Critical Gaps
- No arrays / lists
- No structs / records
- No practical error handling
- Extremely weak module system
- Almost no standard library beyond `print`
- No strong, visible differentiator yet
- Bytecode still in readable JSON form

### Risk
Without rapid progress on basic usability features, the project risks remaining a well-documented prototype that few people try.

---

## 3. Recommended Feature Priority

### Priority High (Target: v0.2 – v0.3)

These features are required before the language can be considered useful for non-trivial programs:

1. **Dynamic arrays / lists**
2. **Structs / records**
3. **Error handling** (`Result[T, E]` style preferred, or simple `try`/`catch`)
4. **Proper module system** (import / export)
5. **Basic string methods** (length, slice, split, concat, format)
6. **`for` loops + range syntax**
7. **Significantly better diagnostics** (clear error messages + accurate source locations)

### Priority Medium (After high-priority items are stable)

- Enums / sum types
- Simple generics
- Map / dictionary type
- Basic pattern matching
- Formal capability system (see section 4)

---

## 4. Strategic Differentiators

These features are rare or almost non-existent in mainstream languages. They align well with RANCAGE’s stated “Universal” vision and should be treated as long-term identity pillars.

### 4.1 Capability-Based Security (Language Level)
- Functions can only perform side effects that are explicitly granted via capabilities
- No ambient authority
- Capabilities should be first-class and checked as early as possible (ideally at compile time)

**Why rare:** Most languages rely on runtime sandboxes or OS-level permissions. Very few enforce this at the language/type-system level.

### 4.2 Bounded Execution by Default
- Instruction budget and memory limits as language-level concepts
- Useful for plugins, scripting, game logic, edge devices, and untrusted code

**Why rare:** Almost never exposed as a core language feature.

### 4.3 Strict Multi-Backend Semantic Contracts
- Backends must preserve language semantics
- Platform-specific behavior must be explicitly declared and isolated
- One source language with real portability guarantees, not just “it compiles somewhere”

**Why rare:** Most multi-target languages quietly change semantics or leave large platform differences undocumented.

### 4.4 Explicit Host Boundary
- Pure RANCAGE code cannot touch the host except through well-defined interfaces
- Clear separation between portable logic and platform integration

---

## 5. Recommended Guiding Principle

> Make the language **useful first**, then make it **distinct**.

Focus near-term effort on the high-priority list so people can actually write real programs.  
Simultaneously keep the strategic differentiators (capability system + semantic multi-target guarantees) in mind so the language develops a clear identity instead of becoming “yet another simple language”.

---

## 6. Suggested Roadmap Integration

### Near-term (v0.2.x – v0.3)
- Complete high-priority language features listed above
- Improve diagnostics aggressively
- Stabilize RANCAGE-IR versioning and validation
- Continue packaging work (Windows first, then Linux/macOS when ready)

### Medium-term (v0.4+)
- Design and prototype capability system
- Research and document backend semantic contracts
- Begin serious backend work (WebAssembly recommended as first non-Python target)
- Formalize standard library design with capability awareness

### Long-term
- Self-hosting
- Native backends
- Engine adapters (only after core language and IR are mature)

---

## 7. One-Paragraph Status Note (Ready for PROJECT_STATUS.md)

> Evaluation on 17 November 2026 confirmed that RANCAGE has a strong architectural vision and unusually honest documentation for its stage. The language remains too limited for practical use. Immediate priority is completing fundamental features (arrays, structs, error handling, modules, better diagnostics). Long-term differentiation should center on capability-based security and strict multi-backend semantic guarantees — areas where almost no existing languages offer serious solutions and which align directly with the project’s “Universal” goal.

---

**End of document**