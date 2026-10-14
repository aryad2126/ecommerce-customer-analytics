"""
generate_overview_assets.py
Generates local, offline SVG illustrations for the Overview landing page:
1. Hero E-Commerce Composition (Shopping bags, delivery parcels, analytics badges, gold stars)
2. Card: Sales & Revenue (Cart with goods, trajectory metrics, coin/price tags)
3. Card: Customer Intelligence (Customer persona, RFM segment rings, loyalty indicator)
4. Card: Products & Fulfillment (Delivery van, dispatch box, SLA success badge)
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "dashboard" / "assets" / "images"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Hero E-Commerce Composition SVG (520 x 380)
hero_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 380" width="100%" height="100%">
  <defs>
    <linearGradient id="bagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8A2B59" />
      <stop offset="100%" stop-color="#501531" />
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFEC8E" />
      <stop offset="100%" stop-color="#C6C954" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Ambient Glow Circles -->
  <circle cx="380" cy="140" r="130" fill="#FFEC8E" opacity="0.08" filter="url(#glow)" />
  <circle cx="140" cy="260" r="100" fill="#C6C954" opacity="0.06" />

  <!-- Floating Analytics Card (Top Left) -->
  <g transform="translate(30, 40)">
    <rect x="0" y="0" width="190" height="95" rx="14" fill="#FFFFFF" fill-opacity="0.14" stroke="#FFEC8E" stroke-width="1.5" stroke-dasharray="3 3" />
    <text x="16" y="26" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="11" font-weight="700" letter-spacing="1">REVENUE VELOCITY</text>
    <text x="16" y="52" fill="#FFFDF0" font-family="system-ui, sans-serif" font-size="20" font-weight="800">+28.4%</text>
    <path d="M 16 78 Q 55 58 90 72 T 165 48" fill="none" stroke="url(#goldGrad)" stroke-width="3.5" stroke-linecap="round" />
    <circle cx="165" cy="48" r="4.5" fill="#FFEC8E" />
  </g>

  <!-- Main Shopping Bag (Center) -->
  <g transform="translate(180, 100)">
    <!-- Shadow -->
    <ellipse cx="100" cy="230" rx="95" ry="16" fill="#220513" opacity="0.45" />
    <!-- Handles -->
    <path d="M 65 50 C 65 -5, 135 -5, 135 50" fill="none" stroke="#FFEC8E" stroke-width="6" stroke-linecap="round" />
    <!-- Body -->
    <rect x="25" y="45" width="150" height="175" rx="16" fill="url(#bagGrad)" stroke="#FFEC8E" stroke-width="2" />
    <!-- Accent Fold -->
    <path d="M 25 45 L 45 65 L 155 65 L 175 45 Z" fill="#FFFFFF" opacity="0.12" />
    <!-- Brand Crest -->
    <circle cx="100" cy="125" r="26" fill="#FFEC8E" fill-opacity="0.18" stroke="#FFEC8E" stroke-width="1.5" />
    <text x="100" y="133" text-anchor="middle" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="22">🛍️</text>
    <line x1="25" y1="170" x2="175" y2="170" stroke="#FFEC8E" stroke-width="2" stroke-dasharray="4 4" />
  </g>

  <!-- Parcel / Package Box (Front Right) -->
  <g transform="translate(320, 185)">
    <ellipse cx="75" cy="145" rx="70" ry="12" fill="#220513" opacity="0.4" />
    <polygon points="75,10 145,45 75,80 5,45" fill="#FFF3B0" stroke="#621E3E" stroke-width="1" />
    <polygon points="5,45 75,80 75,140 5,105" fill="#DECE88" stroke="#621E3E" stroke-width="1" />
    <polygon points="145,45 75,80 75,140 145,105" fill="#C6C954" opacity="0.9" stroke="#621E3E" stroke-width="1" />
    <line x1="40" y1="27" x2="110" y2="62" stroke="#621E3E" stroke-width="5" stroke-opacity="0.6" />
    <circle cx="120" cy="95" r="16" fill="#621E3E" stroke="#FFEC8E" stroke-width="1.5" />
    <text x="120" y="100" text-anchor="middle" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="12" font-weight="800">✓</text>
  </g>

  <!-- Floating Customer Badge (Bottom Left) -->
  <g transform="translate(45, 235)">
    <rect x="0" y="0" width="160" height="60" rx="12" fill="#FFFDF0" fill-opacity="0.15" stroke="#C6C954" stroke-width="1.5" />
    <circle cx="28" cy="30" r="16" fill="#C6C954" fill-opacity="0.3" />
    <text x="28" y="35" text-anchor="middle" fill="#FFEC8E" font-size="14">👥</text>
    <text x="54" y="26" fill="#FFFDF0" font-family="system-ui, sans-serif" font-size="13" font-weight="800">96,000+</text>
    <text x="54" y="44" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="10" font-weight="600">Verified Buyers</text>
  </g>

  <!-- Gold Star Accents -->
  <g fill="#FFEC8E">
    <polygon points="170,30 174,38 182,42 174,46 170,54 166,46 158,42 166,38" opacity="0.85" />
    <polygon points="470,100 473,106 479,109 473,112 470,118 467,112 461,109 467,106" opacity="0.75" />
  </g>
</svg>'''
(ASSETS_DIR / "hero_ecommerce.svg").write_text(hero_svg, encoding="utf-8")
print("Saved hero_ecommerce.svg")

# 2. Card 1: Sales & Revenue Card Visual (380 x 180)
card1_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 180" width="100%" height="100%">
  <defs>
    <linearGradient id="c1Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#621E3E" />
      <stop offset="100%" stop-color="#3A1024" />
    </linearGradient>
    <linearGradient id="c1Accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFEC8E" />
      <stop offset="100%" stop-color="#C6C954" />
    </linearGradient>
  </defs>
  <rect width="380" height="180" rx="16" fill="url(#c1Grad)" />
  <circle cx="320" cy="60" r="70" fill="#FFEC8E" opacity="0.08" />

  <!-- Shopping Cart with Product Boxes -->
  <g transform="translate(45, 45)" stroke="#FFEC8E" stroke-width="2.5" fill="none">
    <circle cx="25" cy="80" r="8" fill="#FFEC8E" />
    <circle cx="75" cy="80" r="8" fill="#FFEC8E" />
    <path d="M 0 10 L 15 10 L 35 60 L 85 60 L 98 25 L 20 25" stroke-linecap="round" stroke-linejoin="round" />
    <line x1="2" y1="10" x2="-6" y2="2" stroke-linecap="round" />
  </g>

  <!-- Items inside cart -->
  <g transform="translate(80, 52)">
    <rect x="0" y="0" width="28" height="28" rx="4" fill="#FFF3B0" fill-opacity="0.85" stroke="#621E3E" stroke-width="1" />
    <text x="14" y="18" text-anchor="middle" fill="#621E3E" font-size="12" font-weight="bold">🎁</text>
    <rect x="20" y="-12" width="24" height="24" rx="4" fill="#C6C954" fill-opacity="0.9" stroke="#621E3E" stroke-width="1" />
    <text x="32" y="5" text-anchor="middle" fill="#621E3E" font-size="11" font-weight="bold">🏷️</text>
  </g>

  <!-- Trajectory Metric Box (Right) -->
  <g transform="translate(185, 38)">
    <rect x="0" y="0" width="155" height="95" rx="12" fill="#FFFDF0" fill-opacity="0.12" stroke="#FFEC8E" stroke-width="1.2" />
    <text x="16" y="26" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="10" font-weight="700" letter-spacing="1">SALES TRAJECTORY</text>
    <text x="16" y="52" fill="#FFFDF0" font-family="system-ui, sans-serif" font-size="20" font-weight="800">R$ 16.0M</text>
    <rect x="16" y="66" width="14" height="16" rx="2" fill="#667436" />
    <rect x="36" y="60" width="14" height="22" rx="2" fill="#C6C954" />
    <rect x="56" y="52" width="14" height="30" rx="2" fill="#FFEC8E" />
    <rect x="76" y="44" width="14" height="38" rx="2" fill="#FFF3B0" />
    <path d="M 16 64 Q 50 48 85 40" fill="none" stroke="url(#c1Accent)" stroke-width="2" />
  </g>
</svg>'''
(ASSETS_DIR / "card_sales_revenue.svg").write_text(card1_svg, encoding="utf-8")
print("Saved card_sales_revenue.svg")

# 3. Card 2: Customer Intelligence Card Visual (380 x 180)
card2_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 180" width="100%" height="100%">
  <defs>
    <linearGradient id="c2Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#501531" />
      <stop offset="100%" stop-color="#621E3E" />
    </linearGradient>
  </defs>
  <rect width="380" height="180" rx="16" fill="url(#c2Grad)" />
  <circle cx="80" cy="90" r="65" fill="#C6C954" opacity="0.08" />

  <!-- Customer Persona Graphic (Left) -->
  <g transform="translate(45, 35)">
    <circle cx="55" cy="55" r="48" fill="none" stroke="#FFEC8E" stroke-width="1.5" stroke-dasharray="4 4" />
    <circle cx="55" cy="55" r="38" fill="#FFFDF0" fill-opacity="0.15" stroke="#C6C954" stroke-width="2" />
    <circle cx="55" cy="44" r="14" fill="#FFEC8E" />
    <path d="M 35 75 C 35 60, 75 60, 75 75 Z" fill="#FFEC8E" />
    <circle cx="88" cy="30" r="12" fill="#D9282D" stroke="#FFFDF0" stroke-width="1" />
    <text x="88" y="34" text-anchor="middle" fill="#FFFFFF" font-size="10">♥</text>
  </g>

  <!-- Segmentation Box (Right) -->
  <g transform="translate(180, 38)">
    <rect x="0" y="0" width="160" height="95" rx="12" fill="#FFFDF0" fill-opacity="0.12" stroke="#FFEC8E" stroke-width="1.2" />
    <text x="16" y="26" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="10" font-weight="700" letter-spacing="1">RFM SEGMENTS</text>
    <text x="16" y="52" fill="#FFFDF0" font-family="system-ui, sans-serif" font-size="17" font-weight="800">High-Value</text>
    <text x="16" y="68" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="11" font-weight="500">Repeat Cohorts: 1.88x AOV</text>
    <rect x="16" y="74" width="60" height="14" rx="7" fill="#667436" />
    <text x="46" y=\"84\" text-anchor="middle" fill="#FFFDF0" font-size="8" font-weight="700">VIP CLUSTER</text>
    <rect x="82" y="74" width="55" height="14" rx="7" fill="#C6C954" fill-opacity="0.3" stroke="#FFEC8E" stroke-width="0.8" />
    <text x="109" y="84" text-anchor="middle" fill="#FFEC8E" font-size="8" font-weight="700">RETENTION</text>
  </g>
</svg>'''
(ASSETS_DIR / "card_customer_intelligence.svg").write_text(card2_svg, encoding="utf-8")
print("Saved card_customer_intelligence.svg")

# 4. Card 3: Products & Fulfillment Card Visual (380 x 180)
card3_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 180" width="100%" height="100%">
  <defs>
    <linearGradient id="c3Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3A1024" />
      <stop offset="100%" stop-color="#621E3E" />
    </linearGradient>
  </defs>
  <rect width="380" height="180" rx="16" fill="url(#c3Grad)" />
  <circle cx="310" cy="120" r="60" fill="#667436" opacity="0.15" />

  <!-- Delivery Fulfillment Graphic (Left) -->
  <g transform="translate(40, 42)">
    <line x1="0" y1="40" x2="16" y2="40" stroke="#FFEC8E" stroke-width="2" stroke-dasharray="3 3" />
    <line x1="-6" y1="55" x2="12" y2="55" stroke="#C6C954" stroke-width="2" stroke-dasharray="4 2" />
    <path d="M 20 20 L 70 20 L 85 40 L 105 40 L 105 70 L 20 70 Z" fill="#FFFDF0" fill-opacity="0.18" stroke="#FFEC8E" stroke-width="2" />
    <circle cx="40" cy="72" r="10" fill="#621E3E" stroke="#FFEC8E" stroke-width="2.5" />
    <circle cx="88" cy="72" r="10" fill="#621E3E" stroke="#FFEC8E" stroke-width="2.5" />
    <rect x="35" y="32" width="22" height="20" rx="2" fill="#C6C954" fill-opacity="0.8" stroke="#621E3E" stroke-width="1" />
    <text x="46" y="46" text-anchor="middle" fill="#621E3E" font-size="10" font-weight="bold">📦</text>
  </g>

  <!-- Performance Badge (Right) -->
  <g transform="translate(180, 38)">
    <rect x="0" y="0" width="160" height="95" rx="12" fill="#FFFDF0" fill-opacity="0.12" stroke="#C6C954" stroke-width="1.2" />
    <text x="16" y="26" fill="#FFEC8E" font-family="system-ui, sans-serif" font-size="10" font-weight="700" letter-spacing="1">FULFILLMENT SLA</text>
    <text x="16" y="52" fill="#FFFDF0" font-family="system-ui, sans-serif" font-size="20" font-weight="800">92.0%</text>
    <text x="16" y="70" fill="#C6C954" font-family="system-ui, sans-serif" font-size="11" font-weight="600">On-Time Success</text>
    <text x="16" y="85" fill="#FFF3B0" font-family="system-ui, sans-serif" font-size="10" opacity="0.85">73 Catalog Categories</text>
  </g>
</svg>'''
(ASSETS_DIR / "card_products_fulfillment.svg").write_text(card3_svg, encoding="utf-8")
print("Saved card_products_fulfillment.svg")
