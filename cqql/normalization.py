from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Set, Tuple, Union
import sympy as sp
from sympy.logic.boolalg import And as SAnd, Or as SOr, Not as SNot, Boolean
from cqql.ast import Formula, Atom, Not, And, Or



@dataclass(frozen=True)
class AttrConfig:
    ordinal_attrs: Set[str]
    get_attr: Callable[[str], str]


def default_get_attr(atom_name: str) -> str:
    if "__" in atom_name:
        return atom_name.split("__", 1)[0]
    return atom_name



def ast_to_sympy(f: Formula) -> Boolean:
    if isinstance(f, Atom):
        return sp.Symbol(f.name)
    if isinstance(f, Not):
        return sp.Not(ast_to_sympy(f.sub))
    if isinstance(f, And):
        return sp.And(ast_to_sympy(f.left), ast_to_sympy(f.right))
    if isinstance(f, Or):
        return sp.Or(ast_to_sympy(f.left), ast_to_sympy(f.right))
    raise TypeError(f"Unsupported AST node for normalization: {type(f)}")


def sympy_to_ast(e: Boolean) -> Formula:
    if e is sp.true:
        return Atom("TRUE")
    if e is sp.false:
        return Atom("FALSE")

    if isinstance(e, sp.Symbol):
        return Atom(str(e))

    if isinstance(e, SNot):
        return Not(sympy_to_ast(e.args[0]))

    if isinstance(e, SAnd):
        args = list(e.args)
        cur = sympy_to_ast(args[0])
        for a in args[1:]:
            cur = And(cur, sympy_to_ast(a))
        return cur

    if isinstance(e, SOr):
        args = list(e.args)
        cur = sympy_to_ast(args[0])
        for a in args[1:]:
            cur = Or(cur, sympy_to_ast(a))
        return cur

    raise TypeError(f"Unsupported SymPy node: {type(e)} / {e}")



Literal = Union[sp.Symbol, SNot]


def to_dnf_expr(e: Boolean) -> Boolean:
    return sp.to_dnf(e, simplify=True)


def dnf_terms(dnf_e: Boolean) -> List[Boolean]:
    if isinstance(dnf_e, SOr):
        return list(dnf_e.args)
    return [dnf_e]


def term_literals(term: Boolean) -> List[Literal]:
    if isinstance(term, SAnd):
        lits: List[Literal] = []
        for a in term.args:
            if isinstance(a, (sp.Symbol, SNot)):
                lits.append(a)  # literal
            else:
                lits.append(a)  # type: ignore
        return lits
    return [term]  # type: ignore


def lit_symbol(l: Literal) -> sp.Symbol:
    return l.args[0] if isinstance(l, SNot) else l


def is_neg(l: Literal) -> bool:
    return isinstance(l, SNot)


def make_and(parts: Iterable[Boolean]) -> Boolean:
    parts = list(parts)
    if not parts:
        return sp.true
    if len(parts) == 1:
        return parts[0]
    return sp.And(*parts)


def make_or(parts: Iterable[Boolean]) -> Boolean:
    parts = list(parts)
    if not parts:
        return sp.false
    if len(parts) == 1:
        return parts[0]
    return sp.Or(*parts)



def find_overlapping_ordinal_attr(
    dnf_e: Boolean,
    cfg: AttrConfig
) -> Optional[str]:
    terms = dnf_terms(dnf_e)


    seen: dict[str, Set[Tuple[str, bool]]] = {}

    for t in terms:
        lits = term_literals(t)
        for l in lits:
            if not isinstance(l, (sp.Symbol, SNot)):
                continue
            sym = lit_symbol(l)
            name = str(sym)
            attr = cfg.get_attr(name)
            if attr not in cfg.ordinal_attrs:
                continue
            sig = (name, is_neg(l))
            seen.setdefault(attr, set()).add(sig)

    for attr, sigs in seen.items():
        if len(sigs) >= 2:
            return attr
    return None


def choose_split_literal(
    dnf_e: Boolean,
    cfg: AttrConfig,
    attr: str
) -> Literal:

    for t in dnf_terms(dnf_e):
        for l in term_literals(t):
            if isinstance(l, (sp.Symbol, SNot)):
                sym = lit_symbol(l)
                name = str(sym)
                if cfg.get_attr(name) == attr:
                    return l
    raise ValueError(f"Could not find a literal for attribute '{attr}' to split on.")



def normalize_no_ordinal_overlaps_sympy(
    e: Boolean,
    cfg: AttrConfig,
    max_depth: int = 50
) -> Boolean:
    if max_depth <= 0:
        return to_dnf_expr(e)

    dnf_e = to_dnf_expr(e)
    attr = find_overlapping_ordinal_attr(dnf_e, cfg)
    if attr is None:
        return dnf_e

    o = choose_split_literal(dnf_e, cfg, attr)
    o_sym = lit_symbol(o)
    o_pos = o_sym if not is_neg(o) else sp.Not(o_sym)
    o_neg = sp.Not(o_pos)



    terms = dnf_terms(dnf_e)

    e1_terms: List[Boolean] = []
    e2_terms: List[Boolean] = []

    for t in terms:
        lits = term_literals(t)


        has_o_pos = any((l == o_pos) for l in lits)
        has_o_neg = any((l == o_neg) for l in lits)


        if has_o_pos and has_o_neg:
            continue


        if not has_o_neg:

            filtered = [x for x in lits if x != o_pos]
            e1_terms.append(make_and(filtered))


        if not has_o_pos:
            filtered = [x for x in lits if x != o_neg]
            e2_terms.append(make_and(filtered))

    e1 = to_dnf_expr(make_or(e1_terms))
    e2 = to_dnf_expr(make_or(e2_terms))


    combined = to_dnf_expr(sp.Or(sp.And(o_pos, e1), sp.And(o_neg, e2)))


    e1n = normalize_no_ordinal_overlaps_sympy(e1, cfg, max_depth=max_depth - 1)
    e2n = normalize_no_ordinal_overlaps_sympy(e2, cfg, max_depth=max_depth - 1)
    return to_dnf_expr(sp.Or(sp.And(o_pos, e1n), sp.And(o_neg, e2n)))


def normalize_no_ordinal_overlaps_ast(
    f: Formula,
    ordinal_attrs: Set[str],
    get_attr: Callable[[str], str] = default_get_attr
) -> Formula:
    cfg = AttrConfig(ordinal_attrs=ordinal_attrs, get_attr=get_attr)
    e = ast_to_sympy(f)
    normalized = normalize_no_ordinal_overlaps_sympy(e, cfg)
    return sympy_to_ast(normalized)
