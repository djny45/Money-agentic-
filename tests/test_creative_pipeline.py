from app.creative_pipeline import CreativePipeline
from app.banner import BannerBrief


def test_creative_pipeline(tmp_path):
    package = CreativePipeline(str(tmp_path)).build(
        BannerBrief("Example offer", "Review the current details.", "Learn more"),
        "example-offer",
    )
    assert package.svg_path.endswith("example-offer.svg")
    assert "Example offer" in package.image_prompt
    assert (tmp_path / "example-offer.svg").exists()
