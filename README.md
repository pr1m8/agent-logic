<!-- PROJECT SHIELDS -->
<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.11%2B-blue.svg" alt="Python 3.11+"/>
  </a>
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/Dependency-Poetry-0175C2" alt="Poetry"/>
  </a>
  <a href="https://docs.pydantic.dev/latest/">
    <img src="https://img.shields.io/badge/Pydantic-v2-FF6A00" alt="Pydantic v2"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"/>
  </a>
</p>

# 🤖 agent-logic — Modular Symbolic Logic for Agents, SAT, and LLM‑Enhanced Proofs

**agent-logic** is a modular Python library for constructing, evaluating, transforming, and proving logical expressions — a lightweight **symbolic logic + SAT** engine designed for **LLM‑driven agent systems**.

> **Structured. Serializable. Reasonable. Agent‑Ready.**

---

## 🚀 Overview

It enables:

- ✅ **Propositional Logic** — `AND`, `OR`, `NOT`, `IMPLIES`, `IFF`
- ✅ **Predicate Logic** — Terms, Predicates, Quantifiers (`∀`, `∃`)
- ✅ **Formal Proof Validation** — inference rules & structured derivations
- ✅ **Truth Tables & Satisfiability** — tautology / contradiction checks
- ✅ **Logical Transformations** — equivalences, CNF/DNF (where applicable)
- ✅ **AST Parsing** — recursive, typed abstract syntax trees
- ✅ **Type‑Safe Models** — **Pydantic v2** schemas for strict, serializable I/O
- 🔜 **SAT Backbone** — CNF conversion + DPLL/modern SAT (in progress)

> 🔗 Works great as a **structured tool** for LLMs (LangChain/OpenAI Tools/JSON Mode).

---

## 💪 Current Status

- Core symbolic logic (propositions, connectives, predicates, quantifiers) — **implemented**.
- Truth tables, tautology/contradiction checking, core proof validation — **working & tested**.
- Inference rules (e.g., **Modus Ponens**, **Modus Tollens**, **HS**, **Dilemmas**, **↔ elimination**) — **available**.
- AST parsing, SAT‑based search, deeper quantifier handling — **in progress**.

> ⚠️ Advanced quantifier transformations and large proof automation are under active development.

---

## 🔧 Installation

```bash
pip install agent-logic
# or from source
git clone https://github.com/pr1m8/agent-logic.git
cd agent-logic
poetry install
```

---

## 📦 Concepts & Data Model

**Design goals**
- **Explicit structure** over strings; runtime‑validatable (Pydantic v2)
- **Deterministic** evaluation; pure, testable transforms
- **LLM‑friendly**: JSON‑serializable nodes, strict enums, Literals

**Core types (illustrative)**

```python
# agent_logic/core/ast.py (conceptual)
from pydantic import BaseModel
from typing import Literal, List, Optional

class Proposition(BaseModel):
    name: str

class UnaryOp(BaseModel):
    operator: Literal["NOT"]
    operand: "Expression"

class BinaryOp(BaseModel):
    operator: Literal["AND","OR","IMPLIES","IFF"]
    left: "Expression"
    right: "Expression"

class Quantifier(BaseModel):
    kind: Literal["FORALL","EXISTS"]
    var: str
    body: "Expression"

Expression = Proposition | UnaryOp | BinaryOp | Quantifier
```

All nodes are **JSON‑serializable** and suitable for **structured outputs**.

---

## 💡 Example Usage (Propositional)

```python
from agent_logic.core.operations import Proposition, BinaryOp
from agent_logic.evaluation.truth_table import TruthTable

# Define propositions
p = Proposition(name="P")
q = Proposition(name="Q")

# (P AND Q)
expr = BinaryOp(left=p, right=q, operator="AND")

# Truth table
table = TruthTable(expression=expr)
for row in table.generate():
    print(row)

print("Is tautology:", table.is_tautology())
print("Is contradiction:", table.is_contradiction())
```

**Output (sketch):**
```
P Q | P∧Q
0 0 | 0
0 1 | 0
1 0 | 0
1 1 | 1
Is tautology: False
Is contradiction: False
```

---

## 🧠 Predicate Logic (Quantifiers)

```python
from agent_logic.core.operations import Predicate, Quantified

# ∀x. Likes(x, Pizza) → Exists y. Likes(y, Pizza)
forall_likes = Quantified.forall(
    var="x",
    body=Predicate(name="Likes", terms=["x","Pizza"])
)
exists_liker = Quantified.exists(
    var="y",
    body=Predicate(name="Likes", terms=["y","Pizza"])
)
implication = forall_likes >> exists_liker  # syntactic sugar for IMPLIES
```

- Variable scoping and capture‑avoiding substitution are handled in the model layer.
- Advanced transformations (Skolemization/Unification) **planned**.

---

## 🧩 Proof System

**Supported rules (subset):**
- **MP** (Modus Ponens), **MT** (Modus Tollens)
- **HS** (Hypothetical Syllogism), **DS** (Disjunctive Syllogism)
- **Constructive / Destructive Dilemmas**
- **↔‑Elimination**, **→‑Elimination/Introduction**
- **∧‑Introduction/Elimination**, **∨‑Introduction**
- Quantifier rules (intro/elimination) — **basic forms**

**Derivation sketch:**

```python
from agent_logic.proof.rules import modus_ponens, biconditional_elim
from agent_logic.proof.derivation import Derivation

D = Derivation()
D.assume("P")
D.assume("P -> Q")
D.apply(modus_ponens, "P", "P -> Q")   # yields Q
D.qed(target="Q")
```

The proof engine enforces **well‑typed steps**, tracks **line references**, and can export **structured proof objects**.

---

## 🧪 Truth Tables & Satisfiability

- `TruthTable(expr).is_tautology()` and `.is_contradiction()`
- `satisfiable(expr)` and **model enumeration** (bounded)
- CNF/DNF transforms where applicable; full SAT (DPLL/modern) **in progress**

---

## 🔄 Transformations

- De Morgan, Double Negation, Implication/Biconditional Elimination
- Normal Forms (CNF/DNF) where defined
- Alpha‑equivalence for predicate logic (variable renaming)

---

## 🧭 Roadmap

- [x] Propositional & Predicate Logic Core
- [x] Truth Tables & Tautology Checking
- [x] Structured Proof Validation Engine
- [ ] Advanced SAT Solving (CNF + DPLL/modern)
- [ ] Quantifier Manipulation (Skolemization, Unification)
- [ ] NL → Formal Logic Parsing (experimental)
- [ ] Web Visualizer Playground

---

## 🧱 Project Structure (suggested)

```
agent_logic/
├── core/
│   ├── ast.py                # Node definitions
│   ├── operations.py         # Constructors, sugar, helpers
├── evaluation/
│   ├── truth_table.py        # Table + tautology/contradiction
│   └── satisfiability.py     # Model search (bounded), CNF helpers
├── transform/
│   └── normalize.py          # CNF/DNF, equivalences
├── proof/
│   ├── rules.py              # Inference rules
│   ├── derivation.py         # Proof objects & checking
│   └── checker.py            # Validation engine
├── parsing/
│   ├── parser.py             # (planned) from strings to AST
│   └── printer.py            # pretty printers / LaTeX
├── integrations/
│   └── tools.py              # LangChain/OpenAI Tools wrappers
└── tests/
```

---

## 🧰 Development

```bash
git clone https://github.com/pr1m8/agent-logic.git
cd agent-logic
poetry install
poetry run pytest -q
```

Quality & style:
- **Tests**: `pytest -q`
- **Lint**: `ruff format .` + `ruff check .`
- **Types**: `pyright` or `mypy`
- **Docs**: Google‑style docstrings; examples for public APIs

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Open an issue to discuss substantial changes
2. Keep PRs focused; include tests and examples
3. Follow typing and modeling patterns (Pydantic v2)

See **CONTRIBUTING.md** and **CODE_OF_CONDUCT.md**.

---

## 🎉 License

MIT License — see **LICENSE**.

---

> **Empower your agents with true reason.**  
> _“Teach your models to reason, not just predict.”_
