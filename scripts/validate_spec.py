import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = ["tools", "rules"]
REQUIRED_TOOL_FIELDS = ["name", "version"]
REQUIRED_RULE_FIELDS = ["name", "shell_cmd"]


def validate_spec(path: Path):
    errors = []
    
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        return [f"Invalid JSON: {e}"]

    # ---- Top-level keys ----
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"Missing top-level key: '{key}'")

    # ---- Tools validation ----
    tools = data.get("tools", [])
    if not isinstance(tools, list):
        errors.append("'tools' must be a list")
    else:
        for i, tool in enumerate(tools):
            for field in REQUIRED_TOOL_FIELDS:
                if field not in tool:
                    errors.append(f"Tool[{i}] missing field '{field}'")

    # ---- Rules validation ----
    rules = data.get("rules", [])
    rule_names = set()

    if not isinstance(rules, list):
        errors.append("'rules' must be a list")
    else:
        for i, rule in enumerate(rules):
            for field in REQUIRED_RULE_FIELDS:
                if field not in rule:
                    errors.append(f"Rule[{i}] missing field '{field}'")
            if "name" in rule:
                rule_names.add(rule["name"])

    # ---- DAG edges validation (if exists) ----
    dag_edges = data.get("dag_edges", [])
    if dag_edges:
        if not isinstance(dag_edges, list):
            errors.append("'dag_edges' must be a list")
        else:
            for edge in dag_edges:
                if len(edge) != 2:
                    errors.append(f"Invalid dag edge: {edge}")
                else:
                    if edge[0] not in rule_names:
                        errors.append(f"DAG edge references unknown rule: {edge[0]}")
                    if edge[1] not in rule_names:
                        errors.append(f"DAG edge references unknown rule: {edge[1]}")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_spec.py specs/*.json")
        sys.exit(1)

    for file in sys.argv[1:]:
        path = Path(file)
        print(f"\nChecking {path}")
        errors = validate_spec(path)
        if errors:
            print("❌ FAILED")
            for err in errors:
                print("   -", err)
        else:
            print("✅ PASSED")


if __name__ == "__main__":
    main()