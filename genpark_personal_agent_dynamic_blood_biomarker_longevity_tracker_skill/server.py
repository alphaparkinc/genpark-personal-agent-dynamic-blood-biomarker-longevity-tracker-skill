# -*- coding: utf-8 -*-
"""Model Context Protocol (MCP) Server for Dynamic Blood Biomarker & Longevity Protocol Optimizer Skill
Powered by GenPark (https://www.genpark.ai).
"""
import sys
import json
import logging
from .core import *

TOOLS_METADATA = [
  {
    "name": "audit_blood_biomarker_panel",
    "description": "Evaluate key cardiovascular, metabolic, and inflammatory biomarkers against optimal longevity ranges (e.g. ApoB < 70 mg/dL, hs-CRP < 0.8 mg/L).",
    "inputSchema": {
      "type": "object",
      "properties": {
        "apob_mg_dl": {
          "type": "number"
        },
        "hba1c_pct": {
          "type": "number"
        },
        "hscrp_mg_l": {
          "type": "number"
        },
        "vitamin_d_ng_ml": {
          "type": "number"
        },
        "chronological_age_years": {
          "type": "integer"
        }
      },
      "required": [
        "apob_mg_dl",
        "hba1c_pct",
        "hscrp_mg_l",
        "chronological_age_years"
      ]
    }
  },
  {
    "name": "recommend_longevity_interventions",
    "description": "Generate evidence-based dietary, supplement, and exercise micro-protocols targeting sub-optimal biomarker deviations.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "primary_risk_factor": {
          "type": "string",
          "enum": [
            "atherogenic_lipids",
            "glycemic_dysregulation",
            "systemic_inflammation",
            "optimal_homeostasis"
          ]
        },
        "estimated_biological_age_delta": {
          "type": "number"
        }
      },
      "required": [
        "primary_risk_factor",
        "estimated_biological_age_delta"
      ]
    }
  }
]

def handle_rpc(request_str: str) -> str:
    try:
        req = json.loads(request_str)
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
    
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-dynamic-blood-biomarker-longevity-tracker-skill",
                    "version": "1.0.0",
                    "vendor": "GenPark (https://www.genpark.ai)"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_METADATA}
        })

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        func = globals().get(tool_name)
        if not func or not callable(func):
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            })
        
        try:
            call_res = func(**arguments)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(call_res, ensure_ascii=False, indent=2)}
                    ]
                }
            })
        except Exception as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Execution error: {str(err)}"}
            })

    return json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method '{method}'"}
    })

def run_self_test():
    print(f"=== Running Self Test for genpark-personal-agent-dynamic-blood-biomarker-longevity-tracker-skill ===")
    init_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert "result" in init_res, "Initialize failed"
    print("[PASS] MCP initialize")

    list_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 2, "Tool count mismatch"
    print(f"[PASS] MCP tools/list (2 tools registered)")

    # Execute smoke test for each tool

    call1 = json.loads(handle_rpc(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "audit_blood_biomarker_panel",
            "arguments": {
                "apob_mg_dl": 84.0,
                "hba1c_pct": 5.5,
                "hscrp_mg_l": 0.6,
                "chronological_age_years": 42
            }
        }
    })))
    assert "result" in call1, "Call1 failed"
    print("[PASS] Tool smoke test: audit_blood_biomarker_panel")

    print("[ALL TESTS PASSED] Self-test verified successfully.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_self_test()
        sys.exit(0 if success else 1)
    
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
