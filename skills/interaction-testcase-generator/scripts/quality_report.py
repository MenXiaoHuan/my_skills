import re
from collections import defaultdict


TITLE_PREFIX_RE = re.compile(r"^\s*\[P[0-3]\]\s*", re.IGNORECASE)
TRAILING_PUNCTUATION_RE = re.compile(r"[\s。.!！?？；;，,]+$")
FINGERPRINT_FIELDS = (
    "module_ref",
    "business_object",
    "pre_state",
    "trigger",
    "condition",
    "assertion_target",
    "post_state",
    "actor_refs",
    "permission_refs",
    "state_refs",
    "request_contract",
    "recovery_behavior",
    "business_result",
)


def normalize_case_title(title: str) -> str:
    text = TITLE_PREFIX_RE.sub("", str(title or ""))
    text = TRAILING_PUNCTUATION_RE.sub("", text.strip())
    return re.sub(r"\s+", "", text).lower()


def _canonical(value):
    if isinstance(value, dict):
        return tuple(
            sorted(
                (_canonical(key), _canonical(item))
                for key, item in value.items()
            )
        )
    if isinstance(value, list):
        return tuple(sorted(_canonical(item) for item in value))
    return re.sub(r"\s+", "", str(value or "")).lower()


def verification_fingerprint(case: dict) -> tuple:
    values = tuple(_canonical(case.get(field)) for field in FINGERPRINT_FIELDS)
    if any(values):
        return values
    return (
        _canonical(case.get("module_ref")),
        normalize_case_title(case.get("title", "")),
        _canonical(case.get("path_type")),
    )


def _required_high_risk_paths(ir):
    return {
        (str(goal["id"]), str(path))
        for goal in ir.get("business_goals", [])
        if str(goal.get("risk", "")).lower() == "high"
        for path in goal.get("required_paths", [])
    }


def _case_paths(case):
    return {
        (str(goal_id), str(case.get("path_type")))
        for goal_id in case.get("goal_refs", [])
        if case.get("path_type")
    }


def select_minimum_sufficient_cases(ir: dict) -> list[str]:
    atoms = {atom["id"]: atom for atom in ir.get("coverage_atoms", [])}
    required_atoms = {
        atom_id for atom_id, atom in atoms.items() if atom.get("required", False)
    }
    required_paths = _required_high_risk_paths(ir)
    cases = list(ir.get("candidate_cases", []))
    selected = []
    selected_ids = set()
    covered_atoms = set()
    covered_paths = set()

    while not (required_atoms <= covered_atoms and required_paths <= covered_paths):
        best = None
        best_score = None
        for index, case in enumerate(cases):
            case_id = str(case.get("id", ""))
            if not case_id or case_id in selected_ids:
                continue
            case_atoms = set(case.get("coverage_atoms", [])) & required_atoms
            new_atoms = case_atoms - covered_atoms
            new_paths = (_case_paths(case) & required_paths) - covered_paths
            if not (new_atoms or new_paths):
                continue
            atom_score = sum(
                int(atoms.get(atom_id, {}).get("risk_weight", 1))
                for atom_id in new_atoms
            )
            score = (
                atom_score
                + 2 * len(new_paths)
                - int(case.get("execution_cost", 0))
                - len(case_atoms & covered_atoms)
            )
            candidate_key = (score, -index)
            if best_score is None or candidate_key > best_score:
                best_score = candidate_key
                best = case
        if best is None:
            break
        case_id = str(best["id"])
        selected.append(case_id)
        selected_ids.add(case_id)
        covered_atoms.update(set(best.get("coverage_atoms", [])) & required_atoms)
        covered_paths.update(_case_paths(best) & required_paths)
    return selected


def _coverage(required_ids, covered_ids):
    required = set(required_ids)
    covered = required & set(covered_ids)
    return {
        "covered": sorted(covered),
        "total": len(required),
        "rate": round(len(covered) / len(required), 4) if required else 1.0,
    }


def _duplicate_clusters(cases):
    by_atoms = defaultdict(list)
    by_fingerprint = defaultdict(list)
    for case in cases:
        atoms = tuple(sorted(set(case.get("coverage_atoms", []))))
        if atoms:
            by_atoms[atoms].append(case)
        by_fingerprint[verification_fingerprint(case)].append(case)

    clusters = []
    seen = set()
    for kind, groups in (
        ("coverage_atoms", by_atoms.values()),
        ("verification_fingerprint", by_fingerprint.values()),
    ):
        for group in groups:
            case_ids = tuple(str(case["id"]) for case in group)
            if len(case_ids) < 2 or case_ids in seen:
                continue
            seen.add(case_ids)
            paths = {case.get("path_type") for case in group}
            clusters.append(
                {
                    "kind": kind,
                    "case_ids": list(case_ids),
                    "decision": "keep_separate" if len(paths) > 1 else "adjudication_required",
                }
            )
    return clusters


def build_quality_report(ir: dict, selected_case_ids: list[str] | None = None) -> dict:
    if selected_case_ids is None:
        selected_case_ids = select_minimum_sufficient_cases(ir)
    selected_id_set = set(selected_case_ids)
    cases = [
        case
        for case in ir.get("candidate_cases", [])
        if str(case.get("id")) in selected_id_set
    ]
    atoms = {atom["id"]: atom for atom in ir.get("coverage_atoms", [])}
    covered_atom_ids = {
        atom_id for case in cases for atom_id in case.get("coverage_atoms", [])
    }
    required_atom_ids = {
        atom_id for atom_id, atom in atoms.items() if atom.get("required", False)
    }

    source_ids = {source["id"] for source in ir.get("sources", [])}
    covered_sources = {
        ref for case in cases for ref in case.get("source_refs", []) if ref in source_ids
    }
    goal_ids = {goal["id"] for goal in ir.get("business_goals", [])}
    covered_goals = {
        ref for case in cases for ref in case.get("goal_refs", []) if ref in goal_ids
    }
    required_paths = _required_high_risk_paths(ir)
    covered_paths = {path for case in cases for path in _case_paths(case)}

    api_contracts = {
        item["id"]: item for item in ir.get("api_contracts", [])
    }
    api_atoms = {
        atom_id
        for atom_id, atom in atoms.items()
        if atom.get("kind") == "api_contract"
    }
    data_atoms = {
        atom_id
        for atom_id, atom in atoms.items()
        if atom.get("kind") == "data_consistency"
    }
    state_atoms = {
        atom_id
        for atom_id, atom in atoms.items()
        if atom.get("kind") == "state_transition"
    }
    api_without_source = []
    data_without_invariant = []
    for case in cases:
        case_atoms = set(case.get("coverage_atoms", []))
        targeted_api_ids = {
            atoms[atom_id].get("target_ref")
            for atom_id in case_atoms & api_atoms
            if atom_id in atoms
        }
        case_sources = set(case.get("source_refs", []))
        if targeted_api_ids and any(
            not (
                case_sources
                & set(api_contracts.get(api_id, {}).get("source_refs", []))
            )
            for api_id in targeted_api_ids
        ):
            api_without_source.append(str(case["id"]))
        targeted_invariant_ids = {
            atoms[atom_id].get("target_ref")
            for atom_id in case_atoms & data_atoms
            if atom_id in atoms
        }
        if not targeted_invariant_ids <= set(case.get("invariant_refs", [])):
            data_without_invariant.append(str(case["id"]))

    duplicate_clusters = _duplicate_clusters(cases)
    unresolved_duplicates = [
        cluster
        for cluster in duplicate_clusters
        if cluster["decision"] == "adjudication_required"
    ]
    uncovered_required = sorted(required_atom_ids - covered_atom_ids)
    missing_high_risk_paths = sorted(required_paths - covered_paths)
    blocking = {
        "uncovered_required_atoms": uncovered_required,
        "missing_high_risk_paths": [list(item) for item in missing_high_risk_paths],
        "api_without_source": api_without_source,
        "data_without_invariant": data_without_invariant,
        "unresolved_duplicate_clusters": unresolved_duplicates,
    }

    dimensions = {
        atom.get("kind")
        for atom in atoms.values()
        if atom.get("kind")
    }
    covered_dimensions = {
        atoms[atom_id].get("kind")
        for atom_id in covered_atom_ids
        if atom_id in atoms
    }
    return {
        "source_coverage": _coverage(source_ids, covered_sources),
        "goal_coverage": _coverage(goal_ids, covered_goals),
        "risk_coverage": {
            "required_high_risk_paths": len(required_paths),
            "covered_high_risk_paths": len(required_paths & covered_paths),
            "high_risk_path_rate": (
                round(len(required_paths & covered_paths) / len(required_paths), 4)
                if required_paths
                else 1.0
            ),
        },
        "dimension_coverage": _coverage(dimensions, covered_dimensions),
        "api_coverage": _coverage(api_atoms, covered_atom_ids),
        "data_invariant_coverage": _coverage(data_atoms, covered_atom_ids),
        "state_transition_coverage": _coverage(state_atoms, covered_atom_ids),
        "required_atom_coverage": _coverage(required_atom_ids, covered_atom_ids),
        "duplicate_clusters": duplicate_clusters,
        "merged_cases": [],
        "uncovered_atoms": sorted(set(atoms) - covered_atom_ids),
        "selected_case_ids": selected_case_ids,
        "assumptions": list(ir.get("assumptions", [])),
        "conflicts": list(ir.get("conflicts", [])),
        "quality_gates": {
            "passed": not any(blocking.values()),
            "blocking": blocking,
        },
    }
