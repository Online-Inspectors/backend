# backend
Python Flask API server for handling lookups and data aggregation

## Overview
Implements the foundational backend server for the Online Inspectors project using Flask. This release introduces zero-cost, public registry lookups without relying on any commercial APIs.

## Changes
- Created `app.py` featuring the root endpoint (`/`) and inspection endpoint (`/inspect`).
- Integrated zero-key **RDAP** lookups (`rdap.org`) to extract domain creation dates and registration handles.
- Integrated Google **DoH** (`dns.google`) to resolve domain A records.
- Added strict type hints (`typing.Any`) and configured local environment type-checking via `pyrightconfig.json`.
- Provided a complete `requirements.txt` locking Flask and Requests dependencies.
