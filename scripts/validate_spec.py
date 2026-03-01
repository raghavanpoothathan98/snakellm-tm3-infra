import json
import sys
from pathlib import Path

from pydantic import ValidationError
from spec_schema import PipelineSpec


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_spec.py specs/*.json")
        sys.exit(1)

    ok = True

    for file in sys.argv[1:]:
        path = Path(file)
        print(f"\nChecking {path}")

        try:
            data = json.loads(path.read_text())
            spec = PipelineSpec.model_validate(data)
        except json.JSONDecodeError as e:
            ok = False
            print("❌ FAILED (invalid JSON)")
            print("   -", str(e))
            continue
        except ValidationError as e:
            ok = False
            print("❌ FAILED (schema validation)")
            for err in e.errors()[:25]:
                loc = ".".join(str(x) for x in err.get("loc", []))
                msg = err.get("msg", "")
                print(f"   - {loc}: {msg}")
            if len(e.errors()) > 25:
                print(f"   - ... ({len(e.errors())-25} more)")
            continue

        # ---- extra semantic checks (beyond schema) ----
        rule_names = {r.name for r in spec.rules}
        if spec.dag_edges:
            for a, b in spec.dag_edges:
                if a not in rule_names:
                    ok = False
                    print(f"❌ FAILED (dag edge unknown rule): {a}")
                if b not in rule_names:
                    ok = False
                    print(f"❌ FAILED (dag edge unknown rule): {b}")

        if ok:
            print("✅ PASSED")

    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()