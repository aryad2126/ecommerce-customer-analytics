"""
generate_visual_assets.py
Generates local SVG visual assets for the E-Commerce Intelligence Dashboard.
Styles match the Burgundy, Warm Ivory, Bamboo, Cypress, and Gold palette.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "dashboard" / "assets" / "images"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Color variables
BERRY = "#621E3E"
DARK_BERRY = "#3A1024"
CYPRESS = "#667436"
BAMBOO = "#C6C954"
YLANG = "#FFEC8E"
CREAM = "#FFF3B0"
IVORY = "#FFFDF0"
LIGHT_GRAY = "#EFECE6"

# 1. Hero banner illustration
hero_banner_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240" width="100%" height="100%">
  <defs>
    <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{BERRY}" />
      <stop offset="60%" stop-color="#7B254E" />
      <stop offset="100%" stop-color="{DARK_BERRY}" />
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{YLANG}" />
      <stop offset="100%" stop-color="{BAMBOO}" />
    </linearGradient>
  </defs>
  <rect width="1200" height="240" rx="20" fill="url(#heroGrad)" />
  <circle cx="1080" cy="120" r="140" fill="{YLANG}" opacity="0.06" />
  <circle cx="950" cy="180" r="80" fill="{BAMBOO}" opacity="0.08" />
  <circle cx="1120" cy="40" r="60" fill="{CYPRESS}" opacity="0.12" />

  <!-- E-Commerce Analytics Graphic on Right -->
  <g transform="translate(860, 40)" opacity="0.95">
    <!-- Card Back -->
    <rect x="0" y="0" width="280" height="160" rx="14" fill="{IVORY}" fill-opacity="0.12" stroke="{YLANG}" stroke-width="1.5" stroke-dasharray="2 3" />
    <!-- Mini Chart Lines -->
    <path d="M 25 120 L 70 85 L 120 100 L 170 50 L 215 70 L 255 35" fill="none" stroke="url(#goldGrad)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
    <circle cx="25" cy="120" r="4.5" fill="{YLANG}" />
    <circle cx="70" cy="85" r="4.5" fill="{YLANG}" />
    <circle cx="120" cy="100" r="4.5" fill="{YLANG}" />
    <circle cx="170" cy="50" r="4.5" fill="{YLANG}" />
    <circle cx="215" cy="70" r="4.5" fill="{YLANG}" />
    <circle cx="255" cy="35" r="5" fill="{YLANG}" />

    <!-- Shopping Bag Icon -->
    <g transform="translate(30, 25)" stroke="{YLANG}" stroke-width="2" fill="none">
      <rect x="0" y="10" width="30" height="26" rx="4" fill="{YLANG}" fill-opacity="0.25" />
      <path d="M 7 10 C 7 3, 23 3, 23 10" />
    </g>
    <!-- Package Icon -->
    <g transform="translate(210, 85)" stroke="{BAMBOO}" stroke-width="1.8" fill="none">
      <polygon points="18 0, 36 9, 36 27, 18 36, 0 27, 0 9" fill="{BAMBOO}" fill-opacity="0.2" />
      <line x1="18" y1="0" x2="18" y2="36" />
      <line x1="0" y1="9" x2="36" y2="9" />
    </g>
  </g>

  <!-- Left Editorial Branding Text -->
  <g transform="translate(48, 52)">
    <rect x="0" y="0" width="168" height="26" rx="13" fill="{BAMBOO}" fill-opacity="0.22" stroke="{BAMBOO}" stroke-width="1" />
    <text x="84" y="17" fill="{YLANG}" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" letter-spacing="1.5" text-anchor="middle">ENTERPRISE INTELLIGENCE</text>

    <text x="0" y="68" fill="{IVORY}" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="800" letter-spacing="-0.5">E-Commerce Intelligence Portal</text>
    <text x="0" y="100" fill="{CREAM}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="400" opacity="0.92">Live multi-dimensional analytics for orders, customer segments, product categories, and logistics.</text>

    <g transform="translate(0, 122)">
      <circle cx="6" cy="6" r="4" fill="{BAMBOO}" />
      <text x="18" y="10" fill="{YLANG}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">Brazilian E-Commerce (Olist) Dataset · 99.4K Orders · 96.1K Customers · R$ 16.0M Gross Volume</text>
    </g>
  </g>
</svg>
"""
(ASSETS_DIR / "hero_banner.svg").write_text(hero_banner_svg, encoding="utf-8")

# Category icon helper
def make_category_svg(name, icon_inner, bg_color="#F8F4EE", stroke_color=BERRY):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="100%" height="100%">
  <rect width="120" height="120" rx="20" fill="{bg_color}" />
  <circle cx="60" cy="60" r="42" fill="{IVORY}" stroke="{stroke_color}" stroke-opacity="0.15" stroke-width="1" />
  <g transform="translate(36, 36)" stroke="{stroke_color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
    {icon_inner}
  </g>
</svg>"""

CATEGORIES_ICONS = {
    "bed_bath_table": """
      <!-- Bed & linens -->
      <path d="M 4 36 L 4 16 L 44 16 L 44 36" />
      <path d="M 4 28 L 44 28" />
      <path d="M 10 22 C 10 18, 20 18, 20 22 Z" fill="{BAMBOO}" fill-opacity="0.3" />
      <path d="M 28 22 C 28 18, 38 18, 38 22 Z" fill="{BAMBOO}" fill-opacity="0.3" />
      <line x1="4" y1="36" x2="4" y2="42" />
      <line x1="44" y1="36" x2="44" y2="42" />
    """,
    "health_beauty": """
      <!-- Lotion / perfume bottle -->
      <rect x="14" y="16" width="20" height="28" rx="6" fill="{YLANG}" fill-opacity="0.3" />
      <rect x="20" y="8" width="8" height="8" rx="2" />
      <line x1="24" y1="4" x2="24" y2="8" />
      <path d="M 18 28 Q 24 34, 30 28" />
      <circle cx="36" cy="12" r="2" fill="{CYPRESS}" />
    """,
    "sports_leisure": """
      <!-- Dumbbell / sports -->
      <line x1="8" y1="24" x2="40" y2="24" stroke-width="4" />
      <rect x="6" y="14" width="6" height="20" rx="3" fill="{BERRY}" fill-opacity="0.3" />
      <rect x="36" y="14" width="6" height="20" rx="3" fill="{BERRY}" fill-opacity="0.3" />
      <rect x="2" y="17" width="4" height="14" rx="2" />
      <rect x="42" y="17" width="4" height="14" rx="2" />
    """,
    "computers_accessories": """
      <!-- Laptop -->
      <rect x="8" y="10" width="32" height="22" rx="3" fill="{BAMBOO}" fill-opacity="0.25" />
      <line x1="4" y1="36" x2="44" y2="36" stroke-width="3" />
      <circle cx="24" cy="20" r="3" fill="{CYPRESS}" />
    """,
    "furniture_decor": """
      <!-- Armchair / lamp -->
      <path d="M 10 32 L 10 20 C 10 16, 14 14, 24 14 C 34 14, 38 16, 38 20 L 38 32 Z" fill="{YLANG}" fill-opacity="0.25" />
      <path d="M 6 24 C 6 20, 10 20, 10 24 L 10 32 L 6 32 Z" />
      <path d="M 42 24 C 42 20, 38 20, 38 24 L 38 32 L 42 32 Z" />
      <line x1="12" y1="36" x2="8" y2="44" />
      <line x1="36" y1="36" x2="40" y2="44" />
    """,
    "watches_gifts": """
      <!-- Watch -->
      <circle cx="24" cy="24" r="14" fill="{YLANG}" fill-opacity="0.3" />
      <polyline points="24 16, 24 24, 29 27" />
      <path d="M 18 10 L 18 2 L 30 2 L 30 10" />
      <path d="M 18 38 L 18 46 L 30 46 L 30 38" />
    """,
    "telephony": """
      <!-- Smartphone -->
      <rect x="12" y="4" width="24" height="40" rx="5" fill="{CYPRESS}" fill-opacity="0.2" />
      <line x1="20" y1="8" x2="28" y2="8" />
      <circle cx="24" cy="38" r="2" fill="{BERRY}" />
    """,
    "housewares": """
      <!-- Pot / Cooking pan -->
      <ellipse cx="24" cy="28" rx="16" ry="10" fill="{BAMBOO}" fill-opacity="0.3" />
      <path d="M 8 28 L 8 18 C 8 18, 14 14, 24 14 C 34 14, 40 18, 40 18 L 40 28" />
      <path d="M 24 10 L 24 14" />
      <line x1="40" y1="22" x2="46" y2="22" stroke-width="3" />
      <line x1="8" y1="22" x2="2" y2="22" stroke-width="3" />
    """,
    "auto": """
      <!-- Car front -->
      <rect x="8" y="20" width="32" height="18" rx="4" fill="{BERRY}" fill-opacity="0.2" />
      <path d="M 12 20 L 16 10 L 32 10 L 36 20 Z" />
      <circle cx="14" cy="28" r="3" fill="{YLANG}" />
      <circle cx="34" cy="28" r="3" fill="{YLANG}" />
      <line x1="10" y1="38" x2="10" y2="44" stroke-width="4" />
      <line x1="38" y1="38" x2="38" y2="44" stroke-width="4" />
    """,
    "toys": """
      <!-- Teddy bear / toy blocks -->
      <circle cx="24" cy="24" r="14" fill="{YLANG}" fill-opacity="0.3" />
      <circle cx="14" cy="12" r="5" />
      <circle cx="34" cy="12" r="5" />
      <circle cx="20" cy="22" r="1.5" fill="{BERRY}" />
      <circle cx="28" cy="22" r="1.5" fill="{BERRY}" />
      <path d="M 21 28 Q 24 31, 27 28" />
    """,
    "garden_tools": """
      <!-- Shovel & plant -->
      <path d="M 24 38 L 24 14" stroke-width="3" />
      <path d="M 16 8 L 32 8" />
      <path d="M 18 36 C 18 44, 30 44, 30 36 Z" fill="{CYPRESS}" fill-opacity="0.3" />
      <path d="M 32 24 Q 40 20, 36 14 Q 30 18, 32 24 Z" fill="{BAMBOO}" fill-opacity="0.4" />
    """,
    "baby": """
      <!-- Baby stroller -->
      <path d="M 10 16 C 10 26, 20 32, 34 32 L 36 16 Z" fill="{YLANG}" fill-opacity="0.3" />
      <circle cx="16" cy="38" r="4" fill="{CYPRESS}" />
      <circle cx="32" cy="38" r="4" fill="{CYPRESS}" />
      <path d="M 36 16 L 42 8" stroke-width="3" />
    """,
    "default_product": """
      <!-- Shopping Bag -->
      <rect x="8" y="14" width="32" height="28" rx="4" fill="{YLANG}" fill-opacity="0.25" />
      <path d="M 16 14 C 16 6, 32 6, 32 14" />
      <circle cx="24" cy="26" r="3" fill="{BERRY}" />
    """,
    "empty_state": """
      <!-- Empty Box / Magnifying Glass -->
      <rect x="6" y="18" width="36" height="26" rx="4" stroke-dasharray="3 3" />
      <line x1="6" y1="26" x2="42" y2="26" />
      <circle cx="24" cy="14" r="8" stroke="{CYPRESS}" />
      <line x1="30" y1="20" x2="36" y2="26" stroke="{CYPRESS}" stroke-width="3" />
    """
}

for name, icon_markup in CATEGORIES_ICONS.items():
    svg_content = make_category_svg(name, icon_markup)
    (ASSETS_DIR / f"{name}.svg").write_text(svg_content, encoding="utf-8")

print(f"Generated {len(CATEGORIES_ICONS) + 1} SVG assets in {ASSETS_DIR}")
