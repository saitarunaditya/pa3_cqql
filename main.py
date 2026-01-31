from cqql.demo_data import APARTMENTS, ATTR_TYPE
from cqql.parser import parse_formula
from cqql.weighting import expand_weights
from cqql.normalization import normalize_no_ordinal_overlaps_ast, default_get_attr
from cqql.evaluation import EvalConfig, evaluate

def main():
    print("CQQL Console (WAND/WOR syntax)")
    print("Operators: !  &  |  parentheses")
    print("Weighted:   WAND(theta1,theta2,expr1,expr2)  WOR(theta1,theta2,expr1,expr2)")
    print("Ordinal attribute encoding suggestion: price__low, price__high (attr=price)\n")

    q = input("Enter CQQL query: ").strip()
    ast = parse_formula(q)
    expanded = expand_weights(ast)
    ordinal_attrs = {"price", "dist", "size"}

    normalized = normalize_no_ordinal_overlaps_ast(
        expanded,
        ordinal_attrs=ordinal_attrs,
        get_attr=default_get_attr
    )

    print("\n--- Parsed AST ---")
    print(ast)

    print("\n--- After weight expansion ---")
    print(expanded)

    print("\n--- Normalized (no ordinal overlaps) ---")
    print(normalized)

    cfg = EvalConfig(get_attr=default_get_attr, attr_type=ATTR_TYPE)

    print("\n--- Evaluation on apartments ---")
    results = []
    for apt in APARTMENTS:
        score = evaluate(normalized, apt["scores"], cfg)
        results.append((apt["name"], score))

    results.sort(key=lambda x: x[1], reverse=True)
    for name, score in results:
        print(f"{name}: {score:.4f}")


if __name__ == "__main__":
    main()


