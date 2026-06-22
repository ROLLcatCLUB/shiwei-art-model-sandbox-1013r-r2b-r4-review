import json
from pathlib import Path
STAGE="1013R_R2B_ONE_CASE_MODEL_SANDBOX_CALL"
REQ=["1013R_R2B_result.json","model_request_context_1013R_R2B.json","model_raw_response_1013R_R2B.json","model_parsed_candidate_1013R_R2B.json","model_output_quality_label_review_1013R_R2B.json","validate_1013R_R2B_one_case_model_sandbox_call.py"]
root=Path(__file__).resolve().parent
errors=[]
for name in REQ:
    if not (root/name).exists(): errors.append(f"missing {name}")
if not errors:
    result=json.loads((root/"1013R_R2B_result.json").read_text(encoding="utf-8"))
    ctx=json.loads((root/"model_request_context_1013R_R2B.json").read_text(encoding="utf-8"))
    raw=json.loads((root/"model_raw_response_1013R_R2B.json").read_text(encoding="utf-8"))
    review=json.loads((root/"model_output_quality_label_review_1013R_R2B.json").read_text(encoding="utf-8"))
    b=result.get("boundary",{})
    if result.get("stage")!=STAGE: errors.append("stage mismatch")
    for k in ["single_case_only","provider_called","model_called"]:
        if b.get(k) is not True: errors.append(f"{k} must be true")
    for k in ["retry_allowed","formal_apply_performed","R36_modified","runtime_connected","database_written","memory_written","vector_index_written","feishu_written","main_project_pushed"]:
        if b.get(k) is not False: errors.append(f"{k} must be false")
    if b.get("provider_call_count_limit") != 1 or b.get("actual_provider_call_count") != 1: errors.append("provider call count must be exactly 1")
    if ctx.get("selected_case_id") != "1013R_R1_case_color_contrast_harmony": errors.append("selected case mismatch")
    if raw.get("provider_meta",{}).get("model") != "MiniMax-M3": errors.append("model mismatch")
    if not isinstance(review.get("issue_tags"), list): errors.append("issue_tags missing")
if errors:
    print(json.dumps({"status":"FAIL","stage":STAGE,"errors":errors},ensure_ascii=False,indent=2)); raise SystemExit(1)
print(json.dumps({"status":"PASS","stage":STAGE,"checked_files":REQ,"single_case_only":True,"provider_call_count":1,"retry_allowed":False,"R36_modified":False,"runtime_connected":False,"formal_apply_performed":False},ensure_ascii=False,indent=2))
