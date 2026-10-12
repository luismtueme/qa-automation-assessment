"""Page object for the GenericCRM data-quality mock.

The app is nested: index.html -> vf-container.html -> app.html.
A welcome dialog and a container spinner sit in front of the inner app,
and the issues grid plus inline edits resolve after a short delay.
"""

import re

from playwright.sync_api import FrameLocator, Locator, Page, expect


class CrmApp:
    def __init__(self, page: Page, base_url: str = "http://localhost:8080/index.html"):
        self.page = page
        self.base_url = base_url
        self._shell: FrameLocator = page.frame_locator("#outerFrame")
        self.app: FrameLocator = self._shell.frame_locator("#appFrame")

    def open(self) -> None:
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        welcome = self.page.locator("#welcomeModal")
        expect(welcome).to_be_visible()
        welcome.get_by_role("button", name="Got it").click()
        expect(welcome).to_be_hidden()
        expect(self._shell.locator("#spinnerOverlay")).to_have_class(re.compile(r"\bhidden\b"))
        expect(self.app.get_by_role("button", name="Review & Fix Issues")).to_be_visible()

    def open_data_issues(self) -> None:
        self.app.get_by_role("button", name="Review & Fix Issues").click()
        expect(self.issue_cards).to_have_count(10, timeout=20_000)

    @property
    def issue_cards(self) -> Locator:
        return self.app.locator(".issue-card")

    def issue_card(self, position: int) -> Locator:
        """Return a card by 1-based position on the grid."""
        return self.issue_cards.nth(position - 1)

    def card_by_sfid(self, sfid: str) -> Locator:
        return self.app.locator(f"[data-record-id='{sfid}']")

    def extract_original_rows(self) -> list[dict[str, str]]:
        cards = self.issue_cards
        rows: list[dict[str, str]] = []
        for index in range(cards.count()):
            card = cards.nth(index)
            headers = self._column_headers(card)
            cells = [
                text.strip()
                for text in card.locator("tr[data-row-type='original'] td").all_inner_texts()
            ]
            values = cells[1:]  # drop the "Original" row label
            row = dict(zip(headers, values))
            row["sfid"] = values[-1]
            rows.append(row)
        return rows

    def select_original_value(self, card: Locator) -> str:
        original = card.locator("tr[data-row-type='original'] td.cell-issue")
        value = original.locator("span").inner_text().strip()
        original.locator("input[type='radio'][value='original']").check()
        return value

    def final_issue_value(self, card: Locator) -> Locator:
        return card.locator("tr[data-row-type='final'] .cell-editable span")

    def edit_final_issue_value(self, card: Locator, new_value: str) -> None:
        cell = card.locator("tr[data-row-type='final'] .cell-editable")
        cell.click()
        editor = cell.locator("input.inline-edit-input")
        expect(editor).to_be_visible()
        editor.clear()
        editor.press_sequentially(new_value)
        editor.press("Enter")

    @property
    def selection_counter(self) -> Locator:
        return self.app.locator("#confirmBar")

    def select_issue_checkboxes(self, positions: list[int]) -> None:
        for position in positions:
            self.issue_card(position).locator("input.issue-checkbox").check()

    def select_all_issues(self) -> None:
        self.app.locator("#selectAll").check()

    def deselect_all_issues(self) -> None:
        self.app.locator("#selectAll").uncheck()

    def _column_headers(self, card: Locator) -> list[str]:
        headers: list[str] = []
        for header in card.locator("thead th").all():
            label = header.locator(":scope > span").first
            if label.count():
                headers.append(label.inner_text().strip())
            else:
                text = header.inner_text().strip()
                if text:
                    headers.append(text)
        return headers
