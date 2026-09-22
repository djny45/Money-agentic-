from dataclasses import dataclass
from html import escape
from pathlib import Path
from .comfyui import ComfyUIClient


@dataclass(frozen=True)
class BannerBrief:
    title: str
    subtitle: str
    call_to_action: str = "Learn more"
    brand: str = "Money-Agentic"
    accent: str = "#ff9f1c"


class BannerAgent:
    """Builds transparent, fact-based SVG ad creatives from supplied offer facts."""

    def build_svg(self, brief: BannerBrief, width: int = 1200, height: int = 628) -> str:
        title = escape(brief.title[:72])
        subtitle = escape(brief.subtitle[:120])
        cta = escape(brief.call_to_action[:28])
        brand = escape(brief.brand[:32])
        accent = brief.accent if brief.accent.startswith("#") else "#ff9f1c"

        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#050505"/><stop offset="1" stop-color="#1a1a1a"/></linearGradient>
<linearGradient id="accent"><stop stop-color="{accent}"/><stop offset="1" stop-color="#ffd166"/></linearGradient>
<filter id="glow"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{width}" height="{height}" rx="36" fill="url(#bg)"/>
<circle cx="1020" cy="80" r="220" fill="none" stroke="{accent}" stroke-opacity=".12" stroke-width="2"/>
<circle cx="1050" cy="110" r="145" fill="none" stroke="{accent}" stroke-opacity=".16" stroke-width="2"/>
<path d="M760 510 C880 410 930 300 1080 145" fill="none" stroke="url(#accent)" stroke-width="10" filter="url(#glow)"/>
<path d="M1055 150 l55 -20 -20 55" fill="{accent}"/>
<text x="78" y="92" font-family="Arial,Helvetica,sans-serif" font-size="28" font-weight="700" fill="{accent}">{brand}</text>
<text x="78" y="245" font-family="Arial,Helvetica,sans-serif" font-size="68" font-weight="800" fill="#fff">{title}</text>
<text x="78" y="315" font-family="Arial,Helvetica,sans-serif" font-size="27" fill="#d6d6d6">{subtitle}</text>
<rect x="78" y="390" width="235" height="68" rx="34" fill="url(#accent)"/>
<text x="195" y="433" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="25" font-weight="800" fill="#080808">{cta}</text>
<text x="78" y="548" font-family="Arial,Helvetica,sans-serif" font-size="16" letter-spacing="4" fill="#888">CLEAR • COMPLIANT • MEASURABLE</text>
</svg>'''

    def queue_image_workflow(self, brief: BannerBrief, workflow: dict, comfyui_url: str = "http://127.0.0.1:8188") -> dict:
        """Queue a supplied ComfyUI API-format workflow using verified campaign facts."""
        prompt = self.prompt(brief)
        workflow = dict(workflow)
        for node in workflow.values():
            inputs = node.get("inputs", {}) if isinstance(node, dict) else {}
            if isinstance(inputs, dict) and "text" in inputs:
                inputs["text"] = prompt
        return ComfyUIClient(comfyui_url).queue_workflow(workflow)

    def build_file(self, brief: BannerBrief, output_path: str, width: int = 1200, height: int = 628) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.build_svg(brief, width, height), encoding="utf-8")
        return str(path)

    def prompt(self, brief: BannerBrief, aspect_ratio: str = "1.91:1") -> str:
        return (
            f"Create a clean advertising banner for {brief.brand}. "
            f"Headline: {brief.title}. Supporting text: {brief.subtitle}. "
            f"CTA: {brief.call_to_action}. Aspect ratio {aspect_ratio}. "
            "Use only supplied claims; do not add guarantees, fake testimonials, "
            "false urgency, unsupported discounts, or misleading financial claims. "
            "Keep typography readable and the CTA prominent."
        )
