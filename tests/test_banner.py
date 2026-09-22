from app.banner import BannerAgent, BannerBrief


def test_banner_contains_supplied_facts():
    svg = BannerAgent().build_svg(
        BannerBrief(
            title="Review this offer",
            subtitle="See the current offer details before deciding.",
            call_to_action="Learn more",
        )
    )
    assert "Review this offer" in svg
    assert "current offer details" in svg
    assert "Learn more" in svg


def test_banner_escapes_text():
    svg = BannerAgent().build_svg(
        BannerBrief(title="<Offer>", subtitle="A & B")
    )
    assert "&lt;Offer&gt;" in svg
    assert "A &amp; B" in svg
