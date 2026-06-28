import json
import re
from pathlib import Path

from demo import (
    load_investigation_context,
    run_planning_stage,
    run_investigation_pipeline,
    normalize_date,
)

EVAL_DIR = Path(__file__).resolve().parent.parent / "evals"


def load_cases():

    cases = []

    for path in sorted(EVAL_DIR.glob("*.json")):

        if not path.exists():
            continue

        try:

            data = json.loads(path.read_text())

        except Exception:

            continue

        if isinstance(data, list):

            cases.extend(data)

        elif isinstance(data, dict):

            cases.append(data)

    return cases


def evaluate(case):

    question = case.get("question")

    if not question:

        return {
            "question": "<missing question>",
            "passed": False,
            "reason": "missing question",
        }

    show_date = "1977/05/08"

    # Search for YYYY/MM/DD
    match = re.search(r"(\d{4}/\d{2}/\d{2})", question)
    if match:
        show_date = match.group(1)
    else:
        # Search for MM/DD/YYYY or M/D/YY style dates
        match = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})", question)
        if match:
            show_date = normalize_date(match.group(1))

    session = load_investigation_context(
        question=question,
        show_date=show_date,
    )

    try:

        run_planning_stage(session)

        run_investigation_pipeline(session)

    except Exception as exc:

        return {
            "question": question,
            "passed": False,
            "reason": str(exc),
        }

    planned_skills = session.selected_skills
    skill_results = {skill: session.stage_results.get(skill, False) for skill in planned_skills}

    planning_ok = len(planned_skills) > 0

    execution_ok = all(skill_results.values())

    report_ok = bool(session.final_report)

    passed = (
        planning_ok
        and execution_ok
        and report_ok
    )

    return {
        "question": question,
        "passed": passed,
        "planning": planning_ok,
        "execution": execution_ok,
        "report": report_ok,
        "skills": skill_results,
    }


def main():

    cases = load_cases()

    passed = 0

    failed = 0

    for case in cases:

        result = evaluate(case)

        if result["passed"]:

            passed += 1

            print(f"[PASS] {result['question']}")

        else:

            failed += 1

            print(f"[FAIL] {result['question']}")

            if "reason" in result:

                print(f"       {result['reason']}")

        for skill, success in result.get("skills", {}).items():
            mark = "✓" if success else "✗"
            print(f"    {mark} {skill}")

    print()
    print("========================================")
    print("Evaluation Summary")
    print("========================================")
    total = passed + failed
    print(f"Total : {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    coverage = (passed / total * 100) if total > 0 else 0.0
    print(f"Coverage: {coverage:.2f}%")


if __name__ == "__main__":

    main()