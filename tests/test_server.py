from neon_agency.server import NeonAgencyServer


def test_root_serves_web_ui_html():
    html = NeonAgencyServer().index_html()

    assert "Neon Agency Control Deck" in html
    assert "fetch('/state')" in html
    assert 'data-action="help"' in html


def test_web_ui_contains_core_sections():
    html = NeonAgencyServer().index_html()

    assert 'id="api-status"' in html
    assert 'id="reputation"' in html
    assert 'id="entities"' in html
    assert 'id="target-select"' in html
    assert 'id="reactions-log"' in html
    assert 'id="reset-button"' in html


def test_web_ui_calls_json_api_and_renders_simulation_concepts():
    html = NeonAgencyServer().index_html()

    assert "fetch('/action'" in html
    assert "fetch('/reset'" in html
    assert "renderState" in html
    assert "renderResult" in html
    assert "city_reputation" in html
    assert "dialogue_source" in html
    assert "relationship" in html
    assert "memories" in html
