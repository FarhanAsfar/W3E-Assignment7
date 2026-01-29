# Expense Tracker CLI

A command-line Expense Tracker built with **Python**, designed to practice clean architecture, CLI design, validation, and file-based persistence.

The project uses:

* `argparse` for CLI commands and flags
* `pydantic` for domain validation
* JSON file storage (no database)
* Clear separation of concerns (CLI / Service / Storage / Models)

---

## Features

* Add expenses (with optional date)
* List expenses with multiple filters
* View summaries (totals + per-category breakdown)
* Edit existing expenses by ID
* Delete expenses by ID
* Persistent storage in `data/expenses.json`

---

## Project Structure

```text
tracker/
├── __main__.py        # Entry point (python -m tracker)
├── cli.py             # CLI argument parsing & output
├── service.py         # Business logic
├── storage.py         # JSON load/save only
├── models.py          # Pydantic Expense model
├── utils.py           # Reusable validators (date, month)
└── data/
    └── expenses.json  # Auto-created on first run
```

---

## Requirements

* Python **3.10+** (tested on Python 3.12)
* `pip`

---

## Project Setup (Virtual Environment Required)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

All commands must be run from the project root:

```bash
python -m tracker <command> [options]
```

Example:

```bash
python -m tracker list
```

---

## Expense ID Format

Each expense is automatically assigned an ID:

```
EXP-YYYYMMDD-####
```

Example:

```
EXP-20260201-0003
```

---

## Commands & Usage

---

## `add` — Add a New Expense

Adds a new expense entry.

If `--date` is omitted, **today’s date** is used automatically.

### Command

```bash
python -m tracker add [options]
```

### Options

| Option       | Required | Description                        |
| ------------ | -------- | ---------------------------------- |
| `--date`     | No       | Date in `YYYY-MM-DD` format        |
| `--category` | Yes      | Expense category (e.g. food, rent) |
| `--amount`   | Yes      | Amount (> 0)                       |
| `--currency` | No       | Currency code (default: BDT)       |
| `--note`     | No       | Optional note                      |

### Example

```bash
python -m tracker add \
  --date 2026-02-01 \
  --category food \
  --amount 250 \
  --currency BDT \
  --note lunch
```

---

## `list` — List Expenses

Lists all expenses. If no filters are provided, **all expenses are shown**.

### Command

```bash
python -m tracker list [filters]
```

### Common Filters

| Option         | Description                 |
| -------------- | --------------------------- |
| `--month`      | Filter by month (`YYYY-MM`) |
| `--from-month` | Start month (`YYYY-MM`)     |
| `--to-month`   | End month (`YYYY-MM`)       |
| `--category`   | Filter by category          |

> Note: Use either `--month` **OR** `--from-month` + `--to-month`, not both.

### List-Only Filters

| Option      | Description                     |
| ----------- | ------------------------------- |
| `--min`     | Minimum amount                  |
| `--max`     | Maximum amount                  |
| `--sort-by` | `date`, `amount`, or `category` |
| `--desc`    | Sort descending                 |

### Examples

```bash
python -m tracker list
```

```bash
python -m tracker list --category food
```

```bash
python -m tracker list --from-month 2026-01 --to-month 2026-02
```

```bash
python -m tracker list --min 100 --max 500 --sort-by amount --desc
```

---

## `summary` — Expense Summary

Shows total expenses and breakdown by category.

### Command

```bash
python -m tracker summary [filters]
```

### Filters (Same as `list` common filters)

| Option         | Description                     |
| -------------- | ------------------------------- |
| `--month`      | Summary for a month (`YYYY-MM`) |
| `--from-month` | Start month                     |
| `--to-month`   | End month                       |
| `--category`   | Filter by category              |

### Example

```bash
python -m tracker summary --month 2026-02
```

---

## `edit` — Edit an Expense

Updates one or more fields of an existing expense.

### Command

```bash
python -m tracker edit --id <EXP_ID> [fields]
```

### Editable Fields

| Option       | Description             |
| ------------ | ----------------------- |
| `--date`     | New date (`YYYY-MM-DD`) |
| `--category` | New category            |
| `--amount`   | New amount              |
| `--currency` | New currency            |
| `--note`     | New note                |

### Example

```bash
python -m tracker edit \
  --id EXP-20260201-0003 \
  --amount 300 \
  --note "updated lunch"
```

---

## `delete` — Delete an Expense

Deletes an expense permanently by ID.

### Command

```bash
python -m tracker delete --id <EXP_ID>
```

### Example

```bash
python -m tracker delete --id EXP-20260201-0003
```

---

## Data Storage

* Data is stored in `data/expenses.json`
* The file and directory are created automatically
* Old or invalid records are safely skipped during listing

---

## Error Handling

* Invalid CLI input is rejected early (argparse validation)
* Domain validation errors are handled via Pydantic
* Friendly error messages are shown instead of stack traces

---
