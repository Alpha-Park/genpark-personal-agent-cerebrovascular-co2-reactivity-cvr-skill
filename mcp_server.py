"""
MCP Server for Cerebrovascular CO2 Reactivity (CVR) & Breath-Holding Vasomotor Reserve.
Exposes JSON-RPC endpoints for computing the Breath-Holding Index (BHI) and cerebrovascular reserve.
"""

import json
import sys
from client import CerebrovascularReactivityClient

client = CerebrovascularReactivityClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_breath_holding_index",
                        "description": "Calculates Breath-Holding Index (BHI in %/s) from middle cerebral artery flow velocity (CBFv) changes during voluntary breath hold, scoring cerebrovascular reserve.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "baseline_cbfv_cm_s": {"type": "number", "description": "Baseline mean cerebral blood flow velocity in cm/s (e.g. 58.0)"},
                                "hypercapnia_peak_cbfv_cm_s": {"type": "number", "description": "Peak mean cerebral blood flow velocity at end of apnea in cm/s (e.g. 84.0)"},
                                "apnea_duration_sec": {"type": "number", "default": 30.0, "description": "Duration of voluntary breath hold in seconds"}
                            },
                            "required": ["baseline_cbfv_cm_s", "hypercapnia_peak_cbfv_cm_s"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "calculate_breath_holding_index":
            res = client.calculate_breath_holding_index(
                baseline_cbfv_cm_s=args.get("baseline_cbfv_cm_s", 58.0),
                hypercapnia_peak_cbfv_cm_s=args.get("hypercapnia_peak_cbfv_cm_s", 84.0),
                apnea_duration_sec=args.get("apnea_duration_sec", 30.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
