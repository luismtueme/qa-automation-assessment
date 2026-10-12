# GenericCRM Data Issues — Playwright Tests

Automated checks for the mock data-quality application. Tests use the Playwright sync API and pytest. Each test starts at `http://localhost:8080/index.html` and runs on its own browser page.

The files under `app/` are the provided mock and are not modified by the tests.

## Prerequisites

- Python 3.11 or newer
- Google Chrome is not required; the suite installs Playwright's Chromium

## Install

From the repository root:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run the application

In one terminal, from the repository root:

```bash
cd app
python -m http.server 8080
```

Leave that process running. The app is served at `http://localhost:8080/index.html`.

## Run the tests

In a second terminal, from the repository root (with the virtual environment activated):

```bash
pytest
```

Useful variants:

```bash
pytest tests/test_data_issues.py::test_checkbox_selection_count
pytest --headed
```

Override the start URL with `APP_URL` if the server is not on port 8080:

```bash
set APP_URL=http://localhost:8080/index.html
pytest
```

On macOS / Linux, use `export` instead of `set`.

## What is covered

| Test | Behavior |
| --- | --- |
| `test_navigate_to_data_issues_grid` | Opens Data Issues and expects 10 issue cards |
| `test_original_rows_have_non_empty_sfid` | Reads every original row and expects a non-empty sfid |
| `test_select_original_value_updates_final_row` | On the 7th card, chooses the original issue value and expects the final row to match |
| `test_edit_final_row_field` | For sfid `00Qak00000RHtuzEAD`, clears the final issue field, enters `123 Test Street`, and confirms |
| `test_checkbox_selection_count` | Checks cards 1, 3, and 5 (`3 issue(s) selected`), selects all (`10 issue(s) selected`), then deselects all and expects the counter to disappear |

Failures keep a screenshot and a trace under `test-results/`. Open a trace with:

```bash
python -m playwright show-trace test-results\<trace-zip>
```
