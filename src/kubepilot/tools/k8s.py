import subprocess
from typing import Optional


def run_tool_by_name(tool_name: str, args: dict) -> str:
    tool_dispatcher = {
        "kubectl_get": kubectl_get,
        "kubectl_describe": kubectl_describe,
        "kubectl_logs": kubectl_logs,
        "kubectl_events": kubectl_events,
        "kubectl_top_pods": kubectl_top_pods,
        "kubectl_top_nodes": kubectl_top_nodes,
    }
    tool_function = tool_dispatcher.get(tool_name)
    if tool_function:
        if tool_name == "kubectl_logs":
            mapped_args = {
                "pod_name": args.get("name"),
                "namespace": args.get("namespace", "default"),
            }
            return tool_function(**mapped_args)
        return tool_function(**args)
    return f"Unknown tool: {tool_name}"


def kubectl_get(
    resource: str,
    name: Optional[str] = None,
    namespace: Optional[str] = "default",
    label_selector: Optional[str] = None,
) -> str:
    """
    Generic get command for any Kubernetes resource.
    ...
    """
    cmd = ["kubectl", "get", resource]

    if name:
        cmd.append(name)

    if namespace and resource not in {
        "nodes",
        "persistentvolumes",
        "storageclasses",
        "clusterroles",
    }:
        cmd += ["-n", namespace]

    if label_selector:
        cmd += ["-l", label_selector]

    return _run_cmd(cmd)


def kubectl_describe(resource: str, name: str, namespace: str = "default") -> str:
    cmd = ["kubectl", "describe", resource, name]
    if resource not in {"nodes", "persistentvolumes", "storageclasses", "clusterroles"}:
        cmd += ["-n", namespace]
    return _run_cmd(cmd)


def kubectl_logs(
    pod_name: str, container_name: Optional[str] = None, namespace: str = "default"
) -> str:
    cmd = ["kubectl", "logs", pod_name, "-n", namespace]
    if container_name:
        cmd += ["-c", container_name]
    return _run_cmd(cmd)


def kubectl_events(
    namespace: str = "default", field_selector: Optional[str] = None
) -> str:
    cmd = ["kubectl", "get", "events"]
    if namespace not in {"", "cluster-wide"}:
        cmd += ["-n", namespace]
    if field_selector:
        cmd += ["--field-selector", field_selector]
    return _run_cmd(cmd)


def kubectl_top_pods(namespace: str = "default") -> str:
    cmd = ["kubectl", "top", "pods", "-n", namespace]
    return _run_cmd(cmd)


def kubectl_top_nodes() -> str:
    cmd = ["kubectl", "top", "nodes"]
    return _run_cmd(cmd)


def _run_cmd(cmd: list) -> str:
    try:
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, timeout=30
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out: {' '.join(cmd)}"
    except subprocess.CalledProcessError as e:
        return f"Error running command: {' '.join(cmd)}\nStderr: {e.stderr.strip()}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
