# Homework 6 — Educational port scanner (localhost only)

> **Topic:** sockets, `connect_ex`, timeouts, a thread pool, and a hard safety rule
> **Lecture:** [02 — File System and `subprocess`](../lecture-notes/02-file-system-and-subprocess.md)
> **Difficulty:** Advanced
> **Target time:** 1 hr
> **Why this one:** it takes sockets out of the abstract and shows you what "a port is open" actually means — a TCP handshake that either completes or is refused. Done on your own loopback, with the target locked to localhost, it is a safe, contained way to learn timeouts, exit conditions, and parallelism.

> **Hard rule:** this scans **only** `127.0.0.1` / `localhost`, and its CLI must
> refuse any other target. Scanning machines you do not own is illegal in many
> jurisdictions. This is a tool for learning about sockets, not for use against
> other people's computers.

## The Brief

Write a script that scans TCP ports on `127.0.0.1` and reports which are open.
For each port it opens a socket, attempts a connection, and records the port if
the connection is accepted. The target is fixed to localhost, and the CLI
refuses any other `--host`.

The naive version scans one port at a time and takes forever; a thread pool
scans hundreds at once, which is where the exercise gets interesting.

## Starter

```python
"""problem-06-port-scanner.py — scan TCP ports on localhost only.

    python problem-06-port-scanner.py --start 1 --end 1024
"""

from __future__ import annotations

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

ALLOWED_HOSTS = {"127.0.0.1", "localhost"}


def is_open(host: str, port: int, timeout: float) -> bool:
    """True if a TCP connect to (host, port) is accepted."""
    # TODO: socket(AF_INET, SOCK_STREAM), settimeout, connect_ex == 0
    raise NotImplementedError


def scan(host: str, start: int, end: int, timeout: float, workers: int = 100) -> list[int]:
    """Return the sorted open ports in [start, end], probed in parallel."""
    # TODO: ThreadPoolExecutor.map is_open over the range
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Scan localhost and print the open ports. Return an exit code."""
    # TODO: refuse any --host not in ALLOWED_HOSTS; scan; print
    ...


if __name__ == "__main__":
    raise SystemExit(main())
```

## Requirements

1. Use `socket.socket(AF_INET, SOCK_STREAM)` and `connect_ex((host, port))`; a
   return of `0` means the port accepted the connection.
2. Set a per-socket timeout (e.g. 0.2s) so the scan is fast.
3. CLI: `[--start 1] [--end 1024] [--host 127.0.0.1] [--timeout 0.2]`. Refuse
   any `--host` other than `127.0.0.1` / `localhost`.
4. Print the open ports and a summary count. Exit 0 on success, 1 on a refused
   target.
5. Use `concurrent.futures.ThreadPoolExecutor` so the scan runs in parallel.

## Constraints

- **The host guard is not optional and comes first.** Check `args.host in
  ALLOWED_HOSTS` before any socket is opened, and return non-zero with a message
  if it fails. This is the line that keeps a learning tool from being a weapon.
- **`connect_ex`, not `connect`.** `connect` raises on a refused port, so a scan
  of 1024 ports would be 1024 exceptions to catch. `connect_ex` returns an error
  *number* instead — `0` for success — so a closed port is a value, not a raise,
  which is what makes a tight scan loop possible.
- **Every socket gets a timeout.** A filtered port (one a firewall silently
  drops) never answers, so without a timeout the connect blocks until the OS
  gives up, which can be minutes. A short `settimeout` bounds every probe.
- **Use a `with` block for each socket.** The context manager closes the socket
  even when the probe fails, so a scan of a thousand ports does not leak a
  thousand file descriptors.

## Expected output

The shipped answer, [`problem-06-port-scanner-solution.py`](./problem-06-port-scanner-solution.py),
opens its own listener on an ephemeral port and probes controlled ports, then
prints whether each was detected rather than a machine-specific port number, so
the run is the same everywhere. It also shows the target guard rejecting a
non-localhost host. Real captured output:

```text
$ python problem-06-port-scanner-solution.py
Port Scanner — driven headless against a listener this file opens.

the port we opened is detected as open: True
a closed port reads as closed:          True
a non-localhost target is refused:      exit 1
```

The listener the demo opens is found as open; a port it deliberately freed reads
as closed; and `--host example.com` is refused with exit 1 before any socket
touches the network.

## Steps

1. Write `is_open` and test it against a port you know is listening — start
   `python -m http.server 8000` in another terminal and probe 8000.
2. Confirm a port nothing is listening on comes back closed, quickly, thanks to
   the timeout.
3. Write `scan` with a plain loop first, then swap in the `ThreadPoolExecutor`
   and notice the speed-up.
4. Add the `--host` guard and confirm anything but localhost is refused before a
   scan starts.
5. Scan `1-1024` on your own machine and see what you have listening.

## The Solution

The shipped file is your answer — `is_open`, `scan`, `main` — plus a `demo()`
that opens a listener and probes it. Your own file has no demo; you run the scan
from the shell.

```python
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
```

**`connect_ex` turns a refused port from an exception into a value.** `connect`
raises `ConnectionRefusedError` on a closed port, which would mean wrapping every
one of a thousand probes in `try/except`. `connect_ex` returns the OS error code
instead — `0` when the handshake completed, non-zero otherwise — so `is_open` is
a one-line comparison and the scan loop stays tight. That is the difference
between a scanner you can point at 1024 ports and one that drowns in
exceptions.

**Every socket has a timeout, and it is why filtered ports do not hang the
scan.** There are three outcomes for a probe, not two: the port answers (open),
the OS refuses immediately (closed), or *nothing answers* — a firewall silently
dropped the packet (filtered). The third case never completes, so without
`settimeout` the connect blocks until the kernel's own long timeout. A short
per-socket timeout turns "filtered" into "closed enough" fast, which is the only
way a full scan finishes in seconds.

**The thread pool is the whole speed story.** A port probe spends almost all its
time *waiting* on the network, not using the CPU, so it is exactly the workload
threads are good at even under Python's GIL: while one thread waits on
`connect_ex`, another runs. `ThreadPoolExecutor(max_workers=100).map(...)` fans a
thousand mostly-waiting probes across a hundred threads and finishes roughly a
hundred times faster than a serial loop, with none of the complexity of writing
the threads by hand.

**The host guard is the first thing `main` does.** Before a single socket is
opened, `args.host in ALLOWED_HOSTS` is checked, and a failure returns 1 with a
message. Putting it first, and making it a hard `return`, is what turns "please
only scan localhost" from a comment into a rule the program enforces — the same
shape as the scraper refusing a `--url` flag.

## Download and run

Download
[problem-06-port-scanner-solution.py](./problem-06-port-scanner-solution.py)
and run it:

```bash
python problem-06-port-scanner-solution.py
```

It opens its own loopback listener, probes it, and refuses a non-localhost
target — all on `127.0.0.1`, touching nothing beyond your own machine.

## Common bugs to catch

- **The scan hangs for minutes on some ports.** You forgot `settimeout`. A
  filtered port never answers, so the connect blocks until the OS gives up.
- **A wall of `ConnectionRefusedError` tracebacks.** You used `connect`, which
  raises on a closed port. Use `connect_ex`, which returns an error number.
- **The scan is glacially slow even though it works.** You scanned serially. A
  `ThreadPoolExecutor` overlaps the waiting and is the point of the bonus.
- **File-descriptor exhaustion on a big range.** You did not close the sockets.
  Use a `with` block so each one closes even on failure.
- **`--host 192.168.1.5` actually scans it.** Your guard was missing or ran
  after the scan started. Check the host first, and hard-return on failure.
- **`connect_ex` returns non-zero on an open port on some systems.** You
  compared against `1` instead of `0`. Only `0` means the connection succeeded.

## Under the hood

<details>
<summary>Under the hood — what "the port accepted the connection" means, and the three-way handshake</summary>

Opening a TCP connection is a three-step conversation. Your machine sends a
`SYN` ("I would like to talk"), a listening service replies `SYN-ACK` ("go
ahead"), and you send `ACK` ("connected") — the *three-way handshake*.
`connect_ex` returning `0` means all three completed: something is listening and
accepted. A `ConnectionRefusedError` (which `connect_ex` reports as a non-zero
error number instead of raising) means the machine actively said no — it sent a
`RST`, "nothing is listening here" — which is why a closed port answers
*instantly*, faster than an open one.

The third outcome is the interesting one. A firewall configured to *drop* rather
than *reject* simply throws your `SYN` away and sends nothing back. Your side
keeps waiting for the `SYN-ACK` that never comes, which is exactly the case the
timeout exists for — and it is also how a real scanner distinguishes "closed"
(got a `RST`, fast) from "filtered" (got silence, timed out). This is a
*connect* scan, the kind any program can do with ordinary sockets, and it
completes the handshake, so the service on the other end sees a real connection.
The stealthier scans you may have heard of (`SYN` scans that never send the final
`ACK`) need raw-socket privileges and exist precisely to avoid leaving that
trace — which is well past what a localhost learning tool has any business doing.

</details>

## Acceptance checklist

- [ ] A port with a listener is reported open; a closed one is not.
- [ ] The scan does not hang on filtered ports — every socket has a timeout.
- [ ] `--host` anything other than `127.0.0.1` / `localhost` is refused before
      the scan runs.
- [ ] The scan uses a `ThreadPoolExecutor` and is noticeably faster than serial.
- [ ] Sockets are closed (a `with` block) so a large scan leaks nothing.
- [ ] Committed to Git with a message like
      `Add Week 12 homework 6: localhost port scanner`.

## Stretch

- Map open ports to their well-known service names with
  `socket.getservbyport(port)` so `80` prints as `http`.
- Add `--timeout` tuning and a `--top-ports` mode that scans only the common
  ones, the way real scanners default.
- Compare the wall-clock time of a serial scan and the threaded one over the
  same range and print the speed-up, so the pool earns its place.

That is the whole homework set. The week's capstone is the
[Mini-Project — File Organizer Bot](../mini-project/README.md).
