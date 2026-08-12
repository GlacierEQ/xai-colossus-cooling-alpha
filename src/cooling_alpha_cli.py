"""Installed CLI for Cooling Alpha's bounded requirement evaluator."""
from __future__ import annotations

import argparse
import json

from thermal_spec import Envelope, within_spec


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a local steady-state cooling requirement")
    parser.add_argument("--inlet-c", type=float, default=25.0)
    parser.add_argument("--max-delta-t", type=float, default=15.0)
    parser.add_argument("--design-mw", type=float, default=50.0)
    parser.add_argument("--measured-outlet-c", type=float, default=38.0)
    parser.add_argument("--observed-flow-lpm", type=float, default=60_000.0)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args(argv)
    result = within_spec(
        Envelope(args.inlet_c, args.max_delta_t, args.design_mw),
        args.measured_outlet_c,
        args.observed_flow_lpm,
    )
    print(json.dumps(result, sort_keys=True, indent=None if args.compact else 2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
