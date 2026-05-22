from pipeline.lib.html_templates import page, brand_bar, crumbs


def test_page_returns_html_skeleton():
    out = page(title="Test", body="<p>hi</p>", asset_prefix="./", scripts=[])
    assert "<!DOCTYPE html>" in out
    assert "<title>Lernplatt · Test</title>" in out
    assert "<p>hi</p>" in out
    assert 'href="./assets/style.css"' in out


def test_brand_bar_has_logout():
    out = brand_bar(asset_prefix="../")
    assert 'href="../dashboard.html"' in out
    assert "Lernplatt · by Can Siebert" in out
    assert "Logout" in out


def test_crumbs_renders_chevrons():
    out = crumbs([
        {"label": "Kurs 22", "href": "../index.html"},
        {"label": "Tag 3", "href": None},
    ])
    assert "Kurs 22" in out
    assert "Tag 3" in out
    assert "›" in out
