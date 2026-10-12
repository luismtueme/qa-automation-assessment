import os
import urllib.error
import urllib.request

import pytest
from playwright.sync_api import expect

from pages.data_issues_page import CrmApp

BASE_URL = os.environ.get("APP_URL", "http://localhost:8080/index.html")

expect.set_options(timeout=10_000)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
    }


@pytest.fixture(scope="session", autouse=True)
def app_server_running():
    probe = BASE_URL if BASE_URL.endswith("index.html") else f"{BASE_URL.rstrip('/')}/index.html"
    try:
        with urllib.request.urlopen(probe, timeout=5) as response:
            if response.status != 200:
                pytest.exit(f"App returned HTTP {response.status} at {probe}", returncode=1)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        pytest.exit(
            "The mock app is not reachable.\n"
            "From the repository root, run: cd app && python -m http.server 8080\n"
            f"({exc})",
            returncode=1,
        )


@pytest.fixture
def crm(page) -> CrmApp:
    app = CrmApp(page, base_url=BASE_URL)
    app.open()
    return app
