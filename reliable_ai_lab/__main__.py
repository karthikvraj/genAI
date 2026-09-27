"""CLI: python -m reliable_ai_lab demo evidence-gate."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .registry import PROJECTS, get_project


def reject_nonfinite(value):
    raise ValueError(f"Non-finite JSON value is not allowed: {value}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Reproducible AI reliability experiments; no production actions.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List the ten projects")
    for name in ["demo", "sample", "run"]:
        command = sub.add_parser(name)
        command.add_argument("project", choices=list(PROJECTS))
        command.add_argument("--seed", type=int, default=7)
        command.add_argument("--output", type=Path)
        if name == "run":
            command.add_argument("--input", type=Path, required=True)
            command.add_argument("--ollama-model", help="Opt-in local model; repair-agent only")
    server = sub.add_parser("serve", help="Local browser playground, bound only to 127.0.0.1")
    server.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            result = PROJECTS
        elif args.command == "serve":
            from .server import serve
            serve(args.port)
            return 0
        else:
            module = get_project(args.project)
            if args.command == "run":
                if args.input.stat().st_size > 5_000_000:
                    raise ValueError("input exceeds 5 MB")
                payload = json.loads(args.input.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
                if not isinstance(payload, dict):
                    raise ValueError("input JSON must be an object")
            else:
                payload = module.sample(args.seed)
            if args.command == "sample":
                result = payload
            elif args.command == "run" and args.ollama_model:
                if args.project != "repair-agent":
                    raise ValueError("--ollama-model is supported only for repair-agent")
                result = module.run(payload, planner=module.ollama_planner(args.ollama_model))
            else:
                result = module.run(payload)
        rendered = json.dumps(result, indent=2, allow_nan=False)
        output = getattr(args, "output", None)
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered + "\n", encoding="utf-8")
        else:
            print(rendered)
        return 0
    except (ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
