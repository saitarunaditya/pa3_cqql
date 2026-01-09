# from cqql.parser import parse_formula
#
# tests = [
#     "A",
#     "!A",
#     "A & B | !C",
#     "A & (B | !C)",
#     "WAND(theta1,theta2,A,B)",
#     "WOR(t1,t2,A,(B|!C))",
#     "WAND(theta1,theta2, A & B, !(C | D)) | E"
# ]
#
# for t in tests:
#     f = parse_formula(t)
#     print("IN :", t)
#     print("AST:", f)
#     print("-" * 40)

# Weighting

# from cqql.parser import parse_formula
# from cqql.weighting import expand_weights
#
# q = "WAND(theta1,theta2, A, (B | !C)) | WOR(t1,t2, D, !E)"
# ast = parse_formula(q)
# expanded = expand_weights(ast)
#
# print("INPUT   :", q)
# print("PARSED  :", ast)
# print("EXPANDED:", expanded)

# Normalization

# from cqql.parser import parse_formula
# from cqql.weighting import expand_weights
# from cqql.normalization import normalize_no_ordinal_overlaps_ast
#
# # Example where ordinal overlap exists on attribute "price":
# # DNF-ish: (price__low & A) | (price__high & B)
# q = "(price__low & A) | (price__high & B)"
#
# ast = parse_formula(q)
# expanded = expand_weights(ast)
#
# normalized = normalize_no_ordinal_overlaps_ast(
#     expanded,
#     ordinal_attrs={"price"}  # tell normalizer which attrs are ordinal
# )
#
# print("INPUT     :", q)
# print("EXPANDED  :", expanded)
# print("NORMALIZED:", normalized)

# Evaluation
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

    # ---- Configure which attributes are ordinal (prox-like)
    # For now we assume: any attr you put here is ordinal.
    # Example: price, dist, rating ...

    # ordinal_attrs = {"price", "dist"}
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

    # # ---- Example object scoring (for demo)
    # # You will replace/extend this with a small dataset for the presentation.
    # objects = [
    #     {
    #         "name": "Obj1",
    #         "scores": {
    #             "A": 1, "B": 1, "C": 0,
    #             "price__low": 0.9, "price__high": 0.1,
    #             "theta1": 0.7, "theta2": 0.4
    #         }
    #     },
    #     {
    #         "name": "Obj2",
    #         "scores": {
    #             "A": 1, "B": 0, "C": 1,
    #             "price__low": 0.2, "price__high": 0.8,
    #             "theta1": 0.7, "theta2": 0.4
    #         }
    #     }
    # ]
    #
    # # Attribute types (DB=0/1, others=[0,1])
    # # Using default_get_attr: "price__low" -> "price"
    # attr_type = {
    #     "A": "db", "B": "db", "C": "db",
    #     "theta1": "db", "theta2": "db",
    #     "price": "prox",
    #     "dist": "prox",
    # }
    #
    # cfg = EvalConfig(get_attr=default_get_attr, attr_type=attr_type)
    #
    # print("\n--- Evaluation on demo objects ---")
    # results = []
    # for obj in objects:
    #     score = evaluate(normalized, obj["scores"], cfg)
    #     results.append((obj["name"], score))
    #
    # results.sort(key=lambda x: x[1], reverse=True)
    # for name, score in results:
    #     print(f"{name}: {score:.4f}")

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


