"""problem-06-port-scanner-solution.py — the localhost port scanner, headless.

The homework answer scans TCP ports on 127.0.0.1 and reports which accept a
connection — and it refuses, by design, to point anywhere else. Your own
problem-06-port-scanner.py ends in ``raise SystemExit(main())``.

> Only 127.0.0.1 / localhost. Scanning other hosts without permission is illegal
> in many places, so the CLI rejects any other target. This is a tool for
> learning about sockets in a contained way, not for use against other machines.

Which ports are open on a real machine changes from run to run, so a live scan
cannot match a recording. The demo instead opens its own listener on an
ephemeral port and probes controlled ports, printing whether each was detected
rather than its number, so the run is the same everywhere. The probe being
tested is identical either way.

Run it with::

    python problem-06-port-scanner-solution.py
"""

from __future__ import annotations

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

ALLOWED_HOSTS = {"127.0.0.1", "localhost"}


def is_open(host: str, port: int, timeout: float) -> bool:
    """True if a TCP connect to (host, port) is accepted.

    connect_ex returns 0 on success and an error number otherwise, so it reports
    a closed port without raising — which is what lets a scan sweep a thousand
    ports without a thousand try/excepts.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0


def scan(host: str, start: int, end: int, timeout: float, workers: int = 100) -> list[int]:
    """Return the sorted open ports in [start, end], probed in parallel."""
    ports = range(start, end + 1)
    with ThreadPoolExecutor(max_workers=min(workers, max(len(ports), 1))) as pool:
        results = pool.map(lambda port: (port, is_open(host, port, timeout)), ports)
    return sorted(port for port, open_ in results if open_)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scan-local",
        description="Scan TCP ports on localhost only.",
    )
    parser.add_argument("--host", default="127.0.0.1",
                        help="Only 127.0.0.1 or localhost is allowed (default: %(default)s)")
    parser.add_argument("--start", type=int, default=1, help="First port (default: %(default)s)")
    parser.add_argument("--end", type=int, default=1024, help="Last port (default: %(default)s)")
    parser.add_argument("--timeout", type=float, default=0.2,
                        help="Per-port timeout in seconds (default: %(default)s)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Scan localhost and print the open ports. Return an exit code."""
    args = build_parser().parse_args(argv)

    if args.host not in ALLOWED_HOSTS:
        print(f"error: refusing to scan {args.host!r}; only 127.0.0.1 or localhost",
              file=sys.stderr)
        return 1

    open_ports = scan(args.host, args.start, args.end, args.timeout)
    for port in open_ports:
        print(f"{port:<6} open")
    print(f"{len(open_ports)} open port(s) on {args.host} in {args.start}-{args.end}")
    return 0


# --------------------------------------------------------------------------- #
# The headless demo — a listener this file opens, and controlled probes. Your
# own file has no demo; you run the scan from the shell.
# --------------------------------------------------------------------------- #


def free_port() -> int:
    """Bind port 0 to borrow a free port number, then release it (stays closed)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def demo() -> None:
    """Probe one open port and one closed one, and show the target guard."""
    print("Port Scanner — driven headless against a listener this file opens.")
    print()

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen()
    open_port = listener.getsockname()[1]
    try:
        detected = scan("127.0.0.1", open_port, open_port, timeout=0.5)
        print(f"the port we opened is detected as open: {open_port in detected}")
    finally:
        listener.close()

    closed_port = free_port()
    still_open = scan("127.0.0.1", closed_port, closed_port, timeout=0.5)
    print(f"a closed port reads as closed:          {closed_port not in still_open}")

    code = main(["--host", "example.com", "--start", "1", "--end", "1"])
    print(f"a non-localhost target is refused:      exit {code}")


if __name__ == "__main__":
    demo()
