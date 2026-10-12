"""Data Issues grid scenarios for the QA automation assessment."""

from playwright.sync_api import expect

from pages.data_issues_page import CrmApp

TARGET_SFID = "00Qak00000RHtuzEAD"
EDITED_VALUE = "123 Test Street"


def test_navigate_to_data_issues_grid(crm: CrmApp):
    """Navigate to the Data Issues page and assert that 10 issue cards are displayed."""
    crm.open_data_issues()
    expect(crm.issue_cards).to_have_count(10)


def test_original_rows_have_non_empty_sfid(crm: CrmApp):
    """Extract original row data from all 10 cards and require a non-empty sfid on each."""
    crm.open_data_issues()

    rows = crm.extract_original_rows()

    assert len(rows) == 10
    sfids = [row["sfid"] for row in rows]
    assert all(sfid.strip() for sfid in sfids)
    assert len(set(sfids)) == 10
    assert TARGET_SFID in sfids


def test_select_original_value_updates_final_row(crm: CrmApp):
    """Select the original issue-column value on the 7th card and confirm the final row updates."""
    crm.open_data_issues()
    card = crm.issue_card(7)

    original_value = crm.select_original_value(card)

    expect(crm.final_issue_value(card)).to_have_text(original_value)


def test_edit_final_row_field(crm: CrmApp):
    """Clear the final issue column for a specific sfid, enter a new value, and confirm it."""
    crm.open_data_issues()
    card = crm.card_by_sfid(TARGET_SFID)

    crm.edit_final_issue_value(card, EDITED_VALUE)

    expect(crm.final_issue_value(card)).to_have_text(EDITED_VALUE)


def test_checkbox_selection_count(crm: CrmApp):
    """Selection counter follows individual checks, select all, and deselect all."""
    crm.open_data_issues()

    crm.select_issue_checkboxes([1, 3, 5])
    expect(crm.selection_counter).to_be_visible()
    expect(crm.selection_counter).to_have_text("3 issue(s) selected")

    crm.select_all_issues()
    expect(crm.selection_counter).to_have_text("10 issue(s) selected")

    crm.deselect_all_issues()
    expect(crm.selection_counter).to_be_hidden()
