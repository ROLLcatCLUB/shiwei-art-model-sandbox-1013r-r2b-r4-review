import json
from pathlib import Path
STAGE="1013R_R3_MODEL_OUTPUT_FAILURE_OR_PASS_ANALYSIS"
REQ=["1013R_R3_result.json","model_output_gap_analysis_1013R_R3.md","issue_tags_1013R_R3.json","prompt_repair_targets_1013R_R3.json","schema_repair_targets_1013R_R3.json","validate_1013R_R3_model_output_failure_or_pass_analysis.py"]
root=Path(__file__).resolve().parent
errors=[]
for name in REQ:
    if not (root/name).exists(): errors.append(f"missing {name}")
if not errors:
    result=json.loads((root/"1013R_R3_result.json").read_text(encoding="utf-8"))
    tags=json.loads((root/"issue_tags_1013R_R3.json").read_text(encoding="utf-8"))
    if result.get("stage")!=STAGE: errors.append("stage mismatch")
    b=result.get("boundary",{})
    for k in ["provider_called","model_called","formal_apply_performed","R36_modified","runtime_connected","database_written","memory_written","vector_index_written","feishu_written","main_project_pushed"]:
        if b.get(k) is not False: errors.append(f"{k} must be false")
    for k in ["unit_design","lesson_design","teaching_process","art_demo_block","courseware_display","assessment_design"]:
        if k not in tags.get("category_findings",{}): errors.append(f"missing category {k}")
if errors:
    print(json.dumps({"status":"FAIL","stage":STAGE,"errors":errors},ensure_ascii=False,indent=2)); raise SystemExit(1)
print(json.dumps({"status":"PASS","stage":STAGE,"checked_files":REQ,"provider_called":False,"model_called":False,"R36_modified":False},ensure_ascii=False,indent=2))
