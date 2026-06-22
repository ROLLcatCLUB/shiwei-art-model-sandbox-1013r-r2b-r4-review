import json
from pathlib import Path
STAGE="1013R_R4_PROMPT_AND_RETURN_SCHEMA_FAST_REPAIR"
REQ=["1013R_R4_result.json","revised_prompt_patch_1013R_R4.md","revised_return_schema_1013R_R4.json","one_case_expected_output_shape_1013R_R4.json","validate_1013R_R4_prompt_and_return_schema_fast_repair.py"]
root=Path(__file__).resolve().parent
errors=[]
for name in REQ:
    if not (root/name).exists(): errors.append(f"missing {name}")
if not errors:
    result=json.loads((root/"1013R_R4_result.json").read_text(encoding="utf-8"))
    schema=json.loads((root/"revised_return_schema_1013R_R4.json").read_text(encoding="utf-8"))
    if result.get("stage")!=STAGE: errors.append("stage mismatch")
    b=result.get("boundary",{})
    for k in ["provider_called","model_called","formal_apply_performed","R36_modified","runtime_connected","database_written","memory_written","vector_index_written","feishu_written","main_project_pushed"]:
        if b.get(k) is not False: errors.append(f"{k} must be false")
    props=schema.get("schema",{}).get("properties",{})
    for k in ["teacher_reading_structure","classroom_script_reference","courseware_screen_structure","big_screen_short_text","assessment_evidence"]:
        if k not in props: errors.append(f"schema missing {k}")
    if props.get("assessment_evidence",{}).get("properties",{}).get("formal_scoring",{}).get("const") is not False:
        errors.append("formal_scoring const false missing")
if errors:
    print(json.dumps({"status":"FAIL","stage":STAGE,"errors":errors},ensure_ascii=False,indent=2)); raise SystemExit(1)
print(json.dumps({"status":"PASS","stage":STAGE,"checked_files":REQ,"provider_called":False,"model_called":False,"R36_modified":False,"formal_apply_performed":False},ensure_ascii=False,indent=2))
