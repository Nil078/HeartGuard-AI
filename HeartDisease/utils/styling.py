"""utils/styling.py — Crimson Medical Design System for HeartGuard AI.

Dark blood-red / crimson palette with deep burgundy, bright red accents,
white typography, glassmorphism cards, and clinical telemetry styling.
"""

from __future__ import annotations

from typing import Any
import streamlit as st

# ── Core Crimson Medical Palette ──────────────────────────────────────────────
CRIMSON_950 = "#0f0004"          # Deepest Blood-Red / Ambient Canvas
CRIMSON_900 = "#1a0008"          # Deep Burgundy
CRIMSON_850 = "#260010"          # Card Background Base
CRIMSON_800 = "#350018"          # Elevated Surface
CRIMSON_700 = "#520020"          # Dark Crimson
CRIMSON_600 = "#7a0028"
CRIMSON_500 = "#a50034"          # Burgundy Accent
CRIMSON_400 = "#c8003f"

RED_VIVID   = "#e8001e"          # Primary Bright Medical Red
RED_BRIGHT  = "#ff1a33"          # Glowing Neon Red Accent
RED_ACCENT  = "#ff4455"          # Secondary Red
RED_SOFT    = "#ff6677"          # Muted Coral Red
RED_GLOW    = "rgba(232, 0, 30, 0.45)"

# White & Neutrals
WHITE       = "#ffffff"
GREY_100    = "rgba(255, 255, 255, 0.95)"
GREY_200    = "rgba(255, 255, 255, 0.85)"
GREY_300    = "rgba(255, 255, 255, 0.72)"
GREY_400    = "rgba(255, 255, 255, 0.55)"
GREY_500    = "rgba(255, 255, 255, 0.38)"

# Semantic Mappings for compatibility with existing modules
PRIMARY = RED_VIVID
PRIMARY_CONTAINER = "#c80028"
PRIMARY_FIXED = RED_ACCENT
PRIMARY_FIXED_DIM = RED_SOFT
ON_PRIMARY = WHITE
ON_PRIMARY_CONTAINER = WHITE

SECONDARY = CRIMSON_500
SECONDARY_CONTAINER = CRIMSON_600
SECONDARY_FIXED = RED_SOFT
ON_SECONDARY = WHITE

TERTIARY = "#059669"             # Optimal / Favorable Clinical Green
TERTIARY_CONTAINER = "#10b981"   # Mint Green
TERTIARY_FIXED = "#a7f3d0"

ERROR = RED_VIVID
ERROR_CONTAINER = CRIMSON_800
ON_ERROR = WHITE
ON_ERROR_CONTAINER = RED_SOFT

AMBER = "#f59e0b"
AMBER_CONTAINER = "#2e1220"

BACKGROUND = CRIMSON_950
SURFACE = CRIMSON_900
SURFACE_CONTAINER_LOWEST = CRIMSON_950
SURFACE_CONTAINER_LOW = CRIMSON_900
SURFACE_CONTAINER = CRIMSON_850
SURFACE_CONTAINER_HIGH = CRIMSON_800
SURFACE_CONTAINER_HIGHEST = CRIMSON_700

ON_SURFACE = WHITE
ON_SURFACE_VARIANT = GREY_300
OUTLINE = "rgba(232, 0, 30, 0.35)"
OUTLINE_VARIANT = "rgba(255, 255, 255, 0.12)"

LIME = TERTIARY_CONTAINER
VIOLET = RED_ACCENT
DANGER = ERROR
TEXT_PRIMARY = ON_SURFACE
TEXT_MUTED = ON_SURFACE_VARIANT

# ── Dark Crimson Plotly Layout ────────────────────────────────────────────────
CLINICAL_PLOTLY_LAYOUT: dict[str, Any] = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(26, 0, 8, 0.55)",
    font=dict(family="Inter, Open Sans, sans-serif", color="#ffffff", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    colorway=[RED_VIVID, RED_ACCENT, TERTIARY_CONTAINER, RED_SOFT, CRIMSON_400, "#ff8090"],
    xaxis=dict(
        gridcolor="rgba(232, 0, 30, 0.12)",
        zerolinecolor="rgba(232, 0, 30, 0.25)",
        tickfont=dict(color="rgba(255, 255, 255, 0.75)", size=11),
        title_font=dict(color="#ffffff", size=12),
    ),
    yaxis=dict(
        gridcolor="rgba(232, 0, 30, 0.12)",
        zerolinecolor="rgba(232, 0, 30, 0.25)",
        tickfont=dict(color="rgba(255, 255, 255, 0.75)", size=11),
        title_font=dict(color="#ffffff", size=12),
    ),
    legend=dict(
        bgcolor="rgba(26, 0, 8, 0.85)",
        bordercolor="rgba(232, 0, 30, 0.3)",
        borderwidth=1,
        font=dict(color="#ffffff", size=11),
    ),
)
DARK_PLOTLY_LAYOUT = CLINICAL_PLOTLY_LAYOUT

# ── Central CSS Stylesheet ───────────────────────────────────────────────────
_CSS = f"""
/* ═══════════════════════════════════════════════════════════════════
   HEARTGUARD AI — CRIMSON MEDICAL DESIGN SYSTEM
   Dark Blood-Red + White + Glowing Red Accents
   ═══════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Open+Sans:wght@400;600;700&display=swap');

:root {{
  --crimson-950: {CRIMSON_950};
  --crimson-900: {CRIMSON_900};
  --crimson-850: {CRIMSON_850};
  --crimson-800: {CRIMSON_800};
  --red-vivid: {RED_VIVID};
  --red-bright: {RED_BRIGHT};
  --red-accent: {RED_ACCENT};
  --red-soft: {RED_SOFT};
  --white: {WHITE};
  --radius-card: 20px;
  --radius-pill: 9999px;
  --shadow-glass: 0 12px 40px rgba(0, 0, 0, 0.55), 0 0 20px rgba(232, 0, 30, 0.12);
  --shadow-red: 0 0 28px rgba(232, 0, 30, 0.45);
}}

/* ── Global Layout & Background ── */
html, body, [data-testid="stAppViewContainer"] {{
  background-color: #0f0004 !important;
  background-image:
    radial-gradient(ellipse at 75% 15%, rgba(200, 0, 35, 0.22) 0%, transparent 60%),
    radial-gradient(ellipse at 15% 85%, rgba(160, 0, 25, 0.18) 0%, transparent 55%),
    radial-gradient(circle at 20% 30%, rgba(232, 0, 30, 0.05) 0 60px, transparent 60px),
    radial-gradient(circle at 80% 70%, rgba(200, 0, 40, 0.06) 0 90px, transparent 90px),
    linear-gradient(180deg, #0f0004 0%, #1a0008 50%, #260010 100%) !important;
  background-attachment: fixed !important;
  color: #ffffff !important;
  font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

[data-testid="stMain"] {{
  background: transparent !important;
}}

.block-container {{
  padding-top: 1.5rem !important;
  padding-bottom: 3.5rem !important;
  max-width: 1280px !important;
}}

/* ── Global Typography Overrides ── */
h1, h2, h3, h4, h5, h6 {{
  font-family: 'Inter', sans-serif !important;
  color: #ffffff !important;
  letter-spacing: -0.02em !important;
}}

p, span, li, label {{
  color: rgba(255, 255, 255, 0.85);
}}

/* ── Header Chrome & Sidebar Controls ── */
header[data-testid="stHeader"] {{
  background: transparent !important;
  color: #ffffff !important;
}}

#MainMenu, [data-testid="stStatusWidget"], footer,
[data-testid="stDeployButton"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stSidebarNavItems"] {{
  display: none !important;
}}

[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {{
  display: flex !important;
  visibility: visible !important;
  opacity: 1 !important;
  color: #ff4455 !important;
  background: rgba(232, 0, 30, 0.18) !important;
  border: 1px solid rgba(232, 0, 30, 0.35) !important;
  border-radius: 8px !important;
  padding: 4px !important;
  transition: all 0.2s ease !important;
}}

[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="stSidebarCollapseButton"]:hover {{
  background: rgba(232, 0, 30, 0.35) !important;
  color: #ffffff !important;
  box-shadow: 0 0 12px rgba(232, 0, 30, 0.5) !important;
}}

/* ── Glassmorphic Crimson Sidebar ── */
[data-testid="stSidebar"] {{
  background: rgba(18, 0, 5, 0.94) !important;
  backdrop-filter: blur(24px) !important;
  -webkit-backdrop-filter: blur(24px) !important;
  border-right: 1px solid rgba(232, 0, 30, 0.22) !important;
  box-shadow: 4px 0 28px rgba(0, 0, 0, 0.6) !important;
}}

[data-testid="stSidebarContent"] {{
  padding: 1.2rem 1rem !important;
}}

/* ── Sidebar Logo & Brand ── */
.hg-sidebar-brand {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.6rem 0.5rem 1.4rem;
  border-bottom: 1px solid rgba(232, 0, 30, 0.2);
  margin-bottom: 1.2rem;
}}

.hg-brand-logo-wrap {{
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #e8001e 0%, #a50034 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 1.3rem;
  box-shadow: 0 0 18px rgba(232, 0, 30, 0.5);
  flex-shrink: 0;
}}

.hg-brand-text {{
  font-family: 'Inter', sans-serif !important;
  font-size: 1.2rem;
  font-weight: 800;
  color: #ffffff !important;
  letter-spacing: -0.02em;
  line-height: 1.1;
}}
.hg-brand-text span {{
  color: #ff1a33;
}}

.hg-brand-sub {{
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.55) !important;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-top: 2px;
}}

/* ── Sidebar Navigation Items (st.page_link) ── */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] a,
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {{
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  padding: 0.65rem 1rem !important;
  border-radius: var(--radius-pill) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.92rem !important;
  font-weight: 600 !important;
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(232, 0, 30, 0.22) !important;
  transition: all 0.2s ease !important;
  margin-bottom: 8px !important;
  text-decoration: none !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
}}

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] *,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span {{
  color: #ffffff !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
}}

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] a:hover {{
  background: rgba(232, 0, 30, 0.18) !important;
  border-color: #ff1a33 !important;
  transform: translateX(4px) !important;
  box-shadow: 0 4px 16px rgba(232, 0, 30, 0.3) !important;
}}

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"].active,
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {{
  background: linear-gradient(135deg, #e8001e 0%, #a50034 100%) !important;
  border-color: #ff1a33 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 20px rgba(232, 0, 30, 0.55) !important;
}}

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] *,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"].active *,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] p,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] span {{
  color: #ffffff !important;
  font-weight: 700 !important;
}}

/* ── Sidebar Footer Callout ── */
.hg-sidebar-footer {{
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(232, 0, 30, 0.22);
  border-radius: 16px;
  padding: 0.9rem 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}}

.hg-sidebar-footer .sf-label {{
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #ff6677;
  font-weight: 700;
  margin-bottom: 0.3rem;
}}

.hg-sidebar-footer .sf-text {{
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.65);
  line-height: 1.4;
}}

.hg-sidebar-footer .sf-pill {{
  display: inline-block;
  background: rgba(232, 0, 30, 0.15);
  color: #ff6677;
  border: 1px solid rgba(232, 0, 30, 0.3);
  border-radius: var(--radius-pill);
  padding: 3px 10px;
  font-size: 0.7rem;
  font-weight: 700;
  margin-top: 0.5rem;
}}

/* ── Glass Containers & Cards ── */
.glass-panel, .hg-card {{
  background: rgba(38, 0, 16, 0.45) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(232, 0, 30, 0.22) !important;
  border-radius: var(--radius-card) !important;
  box-shadow: var(--shadow-glass) !important;
  padding: 1.4rem 1.6rem !important;
  margin-bottom: 1.2rem !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
  color: #ffffff !important;
}}

.glass-panel:hover {{
  box-shadow: 0 16px 44px rgba(0, 0, 0, 0.65), 0 0 24px rgba(232, 0, 30, 0.2) !important;
  border-color: rgba(232, 0, 30, 0.38) !important;
}}

/* ── Top Bar / Header ── */
.hg-topbar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1.4rem;
  border-bottom: 1px solid rgba(232, 0, 30, 0.2);
  margin-bottom: 1.5rem;
}}

.hg-topbar-title {{
  font-family: 'Inter', sans-serif !important;
  font-size: 2.1rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #ffffff !important;
  line-height: 1.1;
}}

.hg-topbar-pill {{
  background: rgba(232, 0, 30, 0.12);
  border: 1px solid rgba(232, 0, 30, 0.35);
  border-radius: var(--radius-pill);
  padding: 0.45rem 1.15rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: #ff6677 !important;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 12px rgba(232, 0, 30, 0.15);
}}

.hg-topbar-pill .pill-dot {{
  width: 8px;
  height: 8px;
  background: #ff1a33;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 10px #ff1a33;
  animation: pulse-dot 2s infinite ease-in-out;
}}

@keyframes pulse-dot {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50%       {{ opacity: 0.35; transform: scale(0.8); }}
}}

/* ── Stat Metric Cards ── */
.hg-stat-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 1.5rem;
}}

.hg-stat-card {{
  background: rgba(38, 0, 16, 0.48);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(232, 0, 30, 0.22);
  border-radius: var(--radius-card);
  padding: 1.25rem 1.4rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  transition: all 0.2s ease;
}}

.hg-stat-card:hover {{
  transform: translateY(-2px);
  border-color: rgba(255, 26, 51, 0.45);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(232, 0, 30, 0.18);
}}

.hg-stat-card .sc-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 0.6rem;
}}

.hg-stat-card .sc-icon-badge {{
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.05rem;
  background: rgba(232, 0, 30, 0.15);
  border: 1px solid rgba(232, 0, 30, 0.3);
  color: #ff4455;
}}

.hg-stat-card .sc-label {{
  font-family: 'Inter', sans-serif;
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(255, 255, 255, 0.65);
  font-weight: 700;
}}

.hg-stat-card .sc-value {{
  font-family: 'Inter', sans-serif;
  font-size: 1.85rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #ffffff;
  line-height: 1.15;
}}

.hg-stat-card .sc-sub {{
  font-size: 0.76rem;
  color: #ff6677;
  margin-top: 0.25rem;
}}

/* ── Section Titles ── */
.hg-section-title {{
  font-family: 'Inter', sans-serif !important;
  font-size: 1.25rem;
  font-weight: 800;
  color: #ffffff !important;
  letter-spacing: -0.02em;
  margin: 1.6rem 0 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}}

/* ── Medical Disclaimer (Burgundy Glass Card) ── */
.glass-amber, .hg-disclaimer-glass {{
  background: rgba(53, 0, 24, 0.45) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(232, 0, 30, 0.3) !important;
  border-left: 4px solid #ff4455 !important;
  border-radius: 16px !important;
  padding: 1rem 1.25rem !important;
  margin: 0.9rem 0 1.4rem !important;
  color: rgba(255, 255, 255, 0.85) !important;
  font-size: 0.88rem !important;
  line-height: 1.55 !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}}

.hg-disclaimer-glass strong {{
  color: #ff8090 !important;
}}

/* ── Prediction Result Banners ── */
.hg-result-card-low {{
  background: rgba(5, 150, 105, 0.18) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(16, 185, 129, 0.4) !important;
  border-radius: var(--radius-card) !important;
  padding: 1.5rem !important;
  margin-bottom: 1.2rem !important;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5), 0 0 20px rgba(5, 150, 105, 0.15) !important;
  color: #ffffff !important;
}}

.hg-result-card-high {{
  background: rgba(165, 0, 52, 0.28) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(232, 0, 30, 0.55) !important;
  border-radius: var(--radius-card) !important;
  padding: 1.5rem !important;
  margin-bottom: 1.2rem !important;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.6), 0 0 28px rgba(232, 0, 30, 0.3) !important;
  color: #ffffff !important;
}}

/* ── Form Inputs Glassmorphism ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {{
  background: rgba(255, 255, 255, 0.06) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(232, 0, 30, 0.3) !important;
  border-radius: 14px !important;
  color: #ffffff !important;
  font-family: 'Open Sans', sans-serif !important;
  font-weight: 500 !important;
  padding: 0.55rem 0.85rem !important;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.2s ease !important;
}}

[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {{
  border-color: #ff1a33 !important;
  background: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 0 0 3px rgba(232, 0, 30, 0.25) !important;
}}

/* Dropdown popover options */
[data-baseweb="popover"], [data-baseweb="menu"] {{
  background-color: #1a0008 !important;
  border: 1px solid rgba(232, 0, 30, 0.3) !important;
  color: #ffffff !important;
}}

[data-baseweb="menu"] li {{
  color: #ffffff !important;
}}
[data-baseweb="menu"] li:hover {{
  background-color: rgba(232, 0, 30, 0.25) !important;
}}

label, [data-testid="stWidgetLabel"] p {{
  font-family: 'Inter', sans-serif !important;
  font-size: 0.84rem !important;
  font-weight: 600 !important;
  color: rgba(255, 255, 255, 0.85) !important;
  margin-bottom: 0.25rem !important;
}}

/* ── Primary CTA Button (Bright Vivid Red) ── */
[data-testid="stButton"] button {{
  background: linear-gradient(135deg, #e8001e 0%, #c80028 100%) !important;
  color: #ffffff !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 700 !important;
  border: 1px solid rgba(255, 26, 51, 0.5) !important;
  border-radius: var(--radius-pill) !important;
  padding: 0.65rem 2rem !important;
  font-size: 0.96rem !important;
  box-shadow: 0 6px 22px rgba(232, 0, 30, 0.5) !important;
  transition: all 0.2s ease !important;
  letter-spacing: -0.01em !important;
}}

[data-testid="stButton"] button:hover {{
  transform: translateY(-2px) !important;
  background: linear-gradient(135deg, #ff1a33 0%, #e8001e 100%) !important;
  box-shadow: 0 10px 30px rgba(232, 0, 30, 0.65) !important;
  color: #ffffff !important;
}}

[data-testid="stButton"] button:disabled {{
  background: rgba(255, 255, 255, 0.1) !important;
  color: rgba(255, 255, 255, 0.4) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
  box-shadow: none !important;
  transform: none !important;
}}

/* ── Risk Factor Pills & Lifestyle Cards ── */
.hg-risk-pill-grid {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0.6rem 0 1.2rem;
}}

.hg-risk-pill {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(232, 0, 30, 0.2);
  border: 1px solid rgba(232, 0, 30, 0.45);
  color: #ff8090 !important;
  border-radius: var(--radius-pill);
  padding: 0.4rem 0.95rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
}}

.hg-neutral-pill {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(5, 150, 105, 0.2);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #a7f3d0;
  border-radius: var(--radius-pill);
  padding: 0.4rem 0.95rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
}}

.hg-lifestyle-card {{
  background: rgba(38, 0, 16, 0.45);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(232, 0, 30, 0.22);
  border-left: 4px solid #e8001e;
  border-radius: 16px;
  padding: 1rem 1.25rem;
  margin-bottom: 0.85rem;
  box-shadow: var(--shadow-glass);
}}

.hg-lifestyle-title {{
  font-family: 'Inter', sans-serif;
  font-size: 0.92rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.3rem;
}}

.hg-lifestyle-reason {{
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.45;
}}

/* ── Data Table Styling ── */
[data-testid="stDataFrame"] {{
  background: rgba(38, 0, 16, 0.45) !important;
  border: 1px solid rgba(232, 0, 30, 0.25) !important;
  border-radius: 16px !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-glass) !important;
}}

/* ── Expanders ── */
[data-testid="stExpander"] {{
  background: rgba(38, 0, 16, 0.35) !important;
  border: 1px solid rgba(232, 0, 30, 0.22) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
}}

[data-testid="stExpander"] summary {{
  color: #ffffff !important;
}}

hr {{
  border-color: rgba(232, 0, 30, 0.2) !important;
  margin: 1.8rem 0 !important;
}}

/* ── ECG Animations ── */
@keyframes heart-pulse {{
  0%   {{ transform: scale(1); filter: drop-shadow(0 0 14px rgba(232,0,30,0.6)); }}
  50%  {{ transform: scale(1.05); filter: drop-shadow(0 0 24px rgba(255,26,51,0.9)); }}
  100% {{ transform: scale(1); filter: drop-shadow(0 0 14px rgba(232,0,30,0.6)); }}
}}

@keyframes draw-ecg {{
  0%   {{ stroke-dashoffset: 600; }}
  100% {{ stroke-dashoffset: 0; }}
}}

.ecg-anim-path {{
  stroke-dasharray: 600;
  stroke-dashoffset: 600;
  animation: draw-ecg 2.8s linear infinite;
}}
"""


def load_css() -> None:
    """Inject the Crimson Medical design system stylesheet."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def render_sidebar(current_page: str = "Home") -> None:
    """Render the Crimson Medical glassmorphic sidebar with active page links."""
    import base64
    from pathlib import Path

    logo_path = Path(__file__).resolve().parent.parent / "stitch_screens" / "2_heartguard_ai_logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            b64_logo = base64.b64encode(f.read()).decode("utf-8")
        logo_html = f'<img src="data:image/png;base64,{b64_logo}" style="width:38px; height:38px; object-fit:contain; border-radius:8px; box-shadow:0 0 12px rgba(232,0,30,0.5);">'
    else:
        logo_html = "🫀"

    with st.sidebar:
        st.markdown(
            f"""
            <div class="hg-sidebar-brand">
              <div class="hg-brand-logo-wrap">{logo_html}</div>
              <div>
                <div class="hg-brand-text">HeartGuard <span>AI</span></div>
                <div class="hg-brand-sub">Clinical Precision in Prediction</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Prediction.py", label="Prediction", icon="🔍")
        st.page_link("pages/2_Data_Analysis.py", label="Data Analysis", icon="📊")
        st.page_link("pages/3_Model_Performance.py", label="Model Performance", icon="📈")
        st.page_link("pages/4_About.py", label="About", icon="ℹ️")

        st.markdown(
            """
            <div class="hg-sidebar-footer">
              <div class="sf-label">Clinical Dataset</div>
              <div class="sf-text">
                UCI Cleveland Heart Disease<br>
                303 Patients · 13 Biometric Features
              </div>
              <div class="sf-pill">Research & Education</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_nav_bar(current_page: str = "Home") -> None:
    """Render a persistent horizontal top navigation bar across all pages."""
    nav_cols = st.columns(5)
    with nav_cols[0]:
        st.page_link("app.py", label="Home", icon="🏠", use_container_width=True)
    with nav_cols[1]:
        st.page_link("pages/1_Prediction.py", label="Prediction", icon="🔍", use_container_width=True)
    with nav_cols[2]:
        st.page_link("pages/2_Data_Analysis.py", label="Data Analysis", icon="📊", use_container_width=True)
    with nav_cols[3]:
        st.page_link("pages/3_Model_Performance.py", label="Model Performance", icon="📈", use_container_width=True)
    with nav_cols[4]:
        st.page_link("pages/4_About.py", label="About", icon="ℹ️", use_container_width=True)
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)


def topbar(title: str, metadata: dict | None) -> None:
    """Render the dark crimson glass topbar with screen title + live engine metadata pill."""
    if metadata:
        model_name = metadata.get("best_model_name", "Model Ready")
        trained_at = metadata.get("trained_at", "")
        date_str = trained_at[:10] if trained_at else "Trained"
        pill_content = f'<span class="pill-dot"></span>{model_name} &nbsp;·&nbsp; {date_str}'
    else:
        pill_content = '<span class="pill-dot"></span>Logistic Regression — Active'

    st.markdown(
        f"""
        <div class="hg-topbar">
          <div class="hg-topbar-title">{title}</div>
          <div class="hg-topbar-pill">{pill_content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def disclaimer_card(key: str = "disclaimer") -> None:
    """Render the burgundy-tinted clinical disclaimer card."""
    from utils.model_utils import DISCLAIMER

    st.markdown(
        f"""
        <div class="hg-disclaimer-glass" id="disclaimer-{key}">
          <strong>Important Medical Disclaimer:</strong> {DISCLAIMER}
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(icon: str, label: str, value: str, sub: str = "", accent: str = "red") -> str:
    """Return HTML for a dark glass stat card with crimson accents."""
    return (
        f'<div class="hg-stat-card">'
        f'  <div class="sc-header">'
        f'    <div class="sc-icon-badge">{icon}</div>'
        f'    <div class="sc-label">{label}</div>'
        f"  </div>"
        f'  <div class="sc-value">{value}</div>'
        f'  <div class="sc-sub">{sub}</div>'
        f"</div>"
    )


def stat_grid(*cards: str) -> None:
    """Render a responsive grid of glass stat cards."""
    inner = "".join(cards)
    st.markdown(f'<div class="hg-stat-grid">{inner}</div>', unsafe_allow_html=True)


def section_title(text: str) -> None:
    """Render a section header with typography matching Inter headline-md."""
    st.markdown(f'<div class="hg-section-title">{text}</div>', unsafe_allow_html=True)
