#!/usr/bin/env python3
"""Query devspace ticket data directly through the devspace MCP gateway,
stripping the ~40KB schema preamble and printing only the fields needed.

Usage:
  devspace_query.py basic    <taskNo>            # ticket core info
  devspace_query.py comments <taskNo>            # comments + key stage changes
  devspace_query.py impact    <taskNo>           # impact & config statements
  devspace_query.py sql       <taskNo>           # SQL scripts on the branch
  devspace_query.py raw <toolName> '<jsonArgs>'  # generic stripped passthrough

Credentials: reads URL/token from ~/.zcode/cli/config.json (mcp.servers.devspace-mcp).
Override with DEVSPACE_MCP_URL / DEVSPACE_MCP_TOKEN env vars.
"""
import json
import os
import re
import sys
import urllib.request

CONFIG_PATH = os.path.expanduser("~/.zcode/cli/config.json")


def load_endpoint():
    url = os.environ.get("DEVSPACE_MCP_URL")
    token = os.environ.get("DEVSPACE_MCP_TOKEN")
    if url and token:
        return url, token
    try:
        cfg = json.load(open(CONFIG_PATH, encoding="utf-8"))
        srv = cfg["mcp"]["servers"]["devspace-mcp"]
        return srv["url"], srv["headers"]["Authorization"].split(" ", 1)[1]
    except Exception as e:
        sys.exit(f"cannot resolve devspace MCP endpoint: {e}\n"
                 f"set DEVSPACE_MCP_URL / DEVSPACE_MCP_TOKEN or configure {CONFIG_PATH}")


TASK_WITH_FLAGS = [
    "withAction", "withAllTaskType", "withAttach", "withBranchVersion",
    "withBuildHis", "withConfig", "withDevCase", "withEdo", "withOwnerUser",
    "withParent", "withProductModule", "withProductVersion", "withProject",
    "withTaskDoc", "withTaskField", "withTaskFlowStage", "withTaskImpact",
    "withTaskPlan", "withTaskType", "withTestCase", "withZmpProject",
]


def task_args(task_no, **overrides):
    """Underlying API requires every with* flag present; default all False."""
    args = {k: False for k in TASK_WITH_FLAGS}
    args["taskNo"] = task_no
    args.update(overrides)
    return args


def call_tool(name, arguments):
    url, token = load_endpoint()
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                          "params": {"name": name, "arguments": arguments}}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {token}",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    if body.startswith("event:") or body.startswith("data:"):
        body = "".join(line[5:] for line in body.splitlines()
                       if line.startswith("data:"))
    rpc = json.loads(body)
    if "error" in rpc:
        sys.exit(f"MCP error: {rpc['error']}")
    text = rpc["result"]["content"][0]["text"]
    marker = "## Original Response"
    payload_start = text.rfind(marker)
    raw = text[payload_start + len(marker):].strip() if payload_start >= 0 else text
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(f"unexpected tool result (no JSON payload): {text[:300]}")
    if str(data.get("code")) not in ("9999", "0"):
        sys.exit(f"API error: {data.get('code')} {data.get('msg')}")
    return data.get("data") or {}


def pick(d, *keys):
    return {k: d.get(k) for k in keys if d.get(k) is not None}


def cmd_basic(task_no):
    d = call_tool("qryApiTaskDtoByTaskNo",
                  task_args(task_no, withTaskFlowStage=True,
                            withTaskImpact=True))
    task = d.get("apiTask") or {}
    out = {
        "task": pick(task, "taskNo", "taskTitle", "comments", "taskSrc",
                     "finishFlag", "finishDate", "regressionCount",
                     "isCommitCode", "branchVersionId", "productVersionId",
                     "productModuleId", "expectPublishDate", "createdDate"),
        "stage": pick(d.get("apiTaskFlowStage") or {}, "stageName", "stageType",
                      "isRegression"),
        "impact": d.get("apiTaskImpactDto"),
        "projectSetting": pick(d.get("apiProjectSettingDto") or {},
                               "isTesterCase"),
    }
    return out


def cmd_comments(task_no):
    d = call_tool("qryApiTaskDtoByTaskNo", task_args(task_no, withAction=True))
    actions = d.get("taskActionDtoList") or []
    comments = []
    stages = []
    for it in reversed(actions):  # oldest first
        act = it.get("adTaskAction") or {}
        who = (it.get("createUserDto") or {}).get("displayName", "?")
        entry = {"time": act.get("createdDate"), "user": who}
        if it.get("comment"):
            entry["comment"] = (act.get("comments") or "").strip()
            comments.append(entry)
        elif act.get("fieldName") == "TASK_FLOW_STAGE_ID":
            entry["stage"] = f"{act.get('oldValueDesc')} -> {act.get('newValueDesc')}"
            stages.append(entry)
    return {"comments": comments, "stageHistory": stages,
            "regressionCount": (d.get("apiTask") or {}).get("regressionCount")}


def cmd_impact(task_no):
    d = call_tool("qryApiTaskDtoByTaskNo",
                  task_args(task_no, withTaskImpact=True, withConfig=True))
    return {"impact": d.get("apiTaskImpactDto"), "config": d.get("apiTaskConfigDto")}


def cmd_sql(task_no):
    return call_tool("qryApiSqlDetailRespDtoListByTaskNo", {"taskNo": task_no})


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    mode = sys.argv[1]
    if mode == "raw":
        if len(sys.argv) < 4:
            sys.exit("raw needs: raw <toolName> '<jsonArgs>'")
        result = call_tool(sys.argv[2], json.loads(sys.argv[3]))
    else:
        handlers = {"basic": cmd_basic, "comments": cmd_comments,
                    "impact": cmd_impact, "sql": cmd_sql}
        if mode not in handlers:
            sys.exit(f"unknown mode: {mode}")
        result = handlers[mode](sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
