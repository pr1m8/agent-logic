# 🤖 agent-logic

### Modular Symbolic Logic for Agent Reasoning, SAT Solving, and LLM-Enhanced Proof Systems

## 🚀 Overview

**agent-logic** is a modular Python library for constructing, evaluating, transforming, and proving logical expressions — designed to act as a lightweight symbolic logic and SAT solving engine for LLM-driven agent systems.

It enables:

- ✅ Propositional Logic (AND, OR, IMPLIES, IFF, NOT)
- ✅ Predicate Logic (Terms, Predicates, Quantifiers: FORALL ∀, EXISTS ∃)
- ✅ Formal Proof Validation (Inference Rules, Structured Derivations)
- ✅ Truth Table Generation and Logical Satisfiability Checking
- ✅ Logical Transformations (Equivalences, Normal Forms)
- ✅ Recursive Abstract Syntax Tree (AST) Parsing
- ✅ Native Pydantic Models and Strong Typing for Safe Structured Outputs

> 🔗 **Structured. Serializable. Reasonable. Agent-Ready.**

## 💪 Current Status

- Core symbolic logic (propositions, connectives, predicates, quantifiers) is **fully implemented**.
- Truth tables, tautology/contradiction checking, and core proof validation are **working and tested**.
- **Inference rules** are largely implemented (Modus Ponens, Modus Tollens, Hypothetical Syllogism, Dilemmas, Biconditional Elimination, etc).
- **AST parsing, SAT-based search, and deeper quantifier handling** are **in progress**.

⚠️ **Note:**

- Some features (e.g., deeper quantifier transformations, large proof automation) are **actively being debugged**.
- Basic and intermediate logical operations are stable; complex proof search under refinement.

## 📊 Motivation

Large Language Models can predict, generate, and reflect — but they struggle with formal, structured, symbolic reasoning.

**agent-logic** empowers:

- Agents that perform **valid, step-by-step derivations**.
- LLMs that **validate**, **transform**, and **construct proofs**.
- Systems that **reason explicitly** over symbolic structures, not just language.

By combining a **SAT-solving core**, **formal proof system**, and **structured Pydantic output models**, it provides the foundation for **autonomous, interpretable reasoning agents**.

> **"Prediction ends where true reasoning begins."**

## 💡 Key Features

| Feature                 | Details                                                               |
| :---------------------- | :-------------------------------------------------------------------- |
| **Propositional Logic** | Build expressions with AND, OR, NOT, IMPLIES, IFF                     |
| **Predicate Logic**     | Define predicates, terms, universal and existential quantifiers       |
| **Inference System**    | Apply formal inference rules to derive conclusions                    |
| **Truth Tables**        | Generate complete truth tables, detect tautologies and contradictions |
| **AST-Based Parsing**   | Logical expressions modeled as fully typed recursive trees            |
| **Pydantic Models**     | All structures serializable, introspectable, LLM-compatible           |
| **SAT Solver Backbone** | Solve satisfiability and consistency of logical expressions (planned) |
| **Type-Safe API**       | Full typing with Pydantic v2, Literal types, structured validation    |

## 💡 Example Usage

```python
from agent_logic.core.operations import Proposition, BinaryOp
from agent_logic.evaluation.truth_table import TruthTable

# Define propositions
p = Proposition(name="P")
q = Proposition(name="Q")

# Create an expression: (P AND Q)
expr = BinaryOp(left=p, right=q, operator="AND")

# Generate a truth table
table = TruthTable(expression=expr)
for row in table.generate():
    print(row)

# Check logical properties
print("Is tautology:", table.is_tautology())
print("Is contradiction:", table.is_contradiction())
```

## 📙 LLM and Agent Toolkit Use Cases

- Formal proof verification of LLM-generated outputs
- Autonomous deduction chains in multi-agent debates
- Structured symbolic output parsing for LangChain tools / OpenAI functions
- Hypothetical reasoning, consequence checking, and goal validation
- Safe, introspectable logical reasoning pipelines for AI agents

All models use **Pydantic v2**, meaning:

- JSON-serializable and function-call ready
- Validatable against strict schemas
- Compatible with LangChain Structured Tools, OpenAI Tools, JSON mode parsing

> "Not just token prediction. Formal reasoning."

## 🌟 Roadmap

- [x] Propositional and Predicate Logic Core
- [x] Truth Tables and Tautology Checking
- [x] Structured Proof Validation Engine
- [ ] Advanced SAT Solving and Forward/Backward Proof Search
- [ ] Quantifier Manipulation (Skolemization, Unification)
- [ ] Natural Language to Formal Logic Parsing (Experimental)
- [ ] Web Visualizer Playground

## 🚀 Getting Started

```bash
pip install agent-logic
```

_(Coming soon to PyPI. Install locally for now.)_

```bash
git clone https://github.com/yourusername/agent-logic.git
cd agent-logic
poetry install
```

## 👤 Authors

Built by developers passionate about combining **symbolic logic**, **autonomous reasoning**, and **practical agentic AI design**.

Contributions, ideas, and PRs are welcome!

## 🎉 License

MIT License.

# Empower Your Agents with True Reason.

> 💡 "Teach your models to reason, not just predict."
