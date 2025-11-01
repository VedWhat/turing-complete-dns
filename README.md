# Turing-Complete DNS Server
<sub>I know it's not exactly turing complete dns but this makes me sound cool</sub>

A DNS server that computes Rule 110 cellular automaton in response to queries. Because why not?

## What is this?

Rule 110 is a Turing-complete cellular automaton. This project embeds that computation in a DNS server, returning the results as TXT records. Each domain query generates a unique computation based on the domain's hash.

## Quick Start

```bash
# Start the server
python3 dns_rule_110.py

# Query from another terminal
dig @localhost -p 5454 google.com TXT
```

Each domain produces a different Rule 110 pattern:

```
$ dig @localhost -p 5454 github.com TXT +short
"Gen  0:              ████  █ █     ████████ █            "
"Gen  1:             ██  █ ███    ██      ███            "
"Gen  2:            ███ ████ █   ███     ██ █            "
"Gen  3:           ██  ██  ███  ██ █    █████            "
"Gen  4:          ███ ███ ██ █ ███████  ██   █            "
```

## Files

- **`dns_rule_110.py`** - Main implementation (DNS + Rule 110)
- **`test_dns_client.py`** - Python DNS client for testing

## How It Works

1. Client queries any domain via DNS
2. Server hashes domain name to create initial state
3. Server runs Rule 110 for N generations
4. Result is encoded in DNS TXT record
5. Client receives computation result

## Requirements

Python 3.6+ with standard library only. No dependencies.

## Why?

To prove that DNS can be more than just a lookup table. Also, it's fun.
