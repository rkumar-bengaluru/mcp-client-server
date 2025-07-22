import json
from typing import List, Dict, Any, Optional

def ask_user_for_tool_call_consent(
    completion: Dict[str, Any],
    auto_allow: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Interactively ask the user for permission to execute each tool call
    found in an OpenAI-style chat completion.

    Parameters
    ----------
    completion : dict
        The JSON object returned by the LLM (must contain `choices[].message.tool_calls`).
    auto_allow : list[str], optional
        Tool names that do NOT need user confirmation (e.g. ["get_weather"]).

    Returns
    -------
    List[Dict[str, Any]]
        A list with only the tool-call dicts that the user allowed.
        The caller can directly forward them to the MCP server.
    """

    if auto_allow is None:
        auto_allow = []

    allowed_calls: List[Dict[str, Any]] = []

    for choice in completion.get("choices", []):
        tool_calls = choice.get("message", {}).get("tool_calls", [])
        for call in tool_calls:
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"])

            if name in auto_allow:
                allowed_calls.append(call)
                continue

            # Pretty-print the request
            print("\n🔧 The assistant wants to execute:")
            print(f"   Tool : {name}")
            print(f"   Args : {json.dumps(args, indent=4)}")

            while True:
                ans = input("   Allow? [y/N/q] > ").strip().lower()
                if ans in {"y", "yes"}:
                    allowed_calls.append(call)
                    break
                elif ans in {"n", "no", ""}:
                    break
                elif ans == "q":
                    raise KeyboardInterrupt("User aborted the session.")
                else:
                    print("   Please answer y, n, or q.")

    return allowed_calls