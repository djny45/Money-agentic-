from dataclasses import dataclass, asdict
from pathlib import Path
import json

from .banner import BannerAgent, BannerBrief


@dataclass(frozen=True)
class CreativePackage:
    title: str
    subtitle: str
    call_to_action: str
    svg_path: str
    image_prompt: str
    upload_status: str = "approval_required"


class CreativePipeline:
    """Creates an ad-ready creative package without publishing or spending ad budget."""

    def __init__(self, output_dir: str = "data/creatives"):
        self.output_dir = Path(output_dir)
        self.banner = BannerAgent()

    def build(self, brief: BannerBrief, slug: str) -> CreativePackage:
        safe = "".join(ch.lower() if ch.isalnum() else "-" for ch in slug).strip("-")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        svg_path = self.output_dir / f"{safe or 'creative'}.svg"
        self.banner.build_file(brief, str(svg_path))
        return CreativePackage(
            title=brief.title,
            subtitle=brief.subtitle,
            call_to_action=brief.call_to_action,
            svg_path=str(svg_path),
            image_prompt=self.banner.prompt(brief),
        )

    def write_manifest(self, package: CreativePackage) -> str:
        path = Path(package.svg_path).with_suffix(".json")
        path.write_text(json.dumps(asdict(package), indent=2), encoding="utf-8")
        return str(path)
