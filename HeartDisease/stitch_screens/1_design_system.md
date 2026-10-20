---
name: Clinical Clarity
colors:
  surface: '#f7f9ff'
  surface-dim: '#ccdcf0'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#edf4ff'
  surface-container: '#e3efff'
  surface-container-high: '#daeafe'
  surface-container-highest: '#d4e4f8'
  on-surface: '#0d1d2b'
  on-surface-variant: '#3f484d'
  inverse-surface: '#233241'
  inverse-on-surface: '#e8f1ff'
  outline: '#6f787e'
  outline-variant: '#bec8ce'
  surface-tint: '#006783'
  primary: '#00627d'
  on-primary: '#ffffff'
  primary-container: '#0e7c9d'
  on-primary-container: '#f3faff'
  inverse-primary: '#7cd1f6'
  secondary: '#5b4ebc'
  on-secondary: '#ffffff'
  secondary-container: '#988cff'
  on-secondary-container: '#2e1a8f'
  tertiary: '#006743'
  on-tertiary: '#ffffff'
  tertiary-container: '#008356'
  on-tertiary-container: '#e6ffed'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bce9ff'
  primary-fixed-dim: '#7cd1f6'
  on-primary-fixed: '#001f2a'
  on-primary-fixed-variant: '#004d63'
  secondary-fixed: '#e4dfff'
  secondary-fixed-dim: '#c7bfff'
  on-secondary-fixed: '#170065'
  on-secondary-fixed-variant: '#4334a3'
  tertiary-fixed: '#88f8bf'
  tertiary-fixed-dim: '#6bdba4'
  on-tertiary-fixed: '#002112'
  on-tertiary-fixed-variant: '#005234'
  background: '#f7f9ff'
  on-background: '#0d1d2b'
  surface-variant: '#d4e4f8'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Open Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Open Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
---

## Brand & Style

This design system is built for a high-trust healthcare environment where data density must coexist with visual calm. The brand personality is professional, clinical, and precise, utilizing a sophisticated **Glassmorphism** aesthetic to create a sense of lightness and transparency.

The interface prioritizes a "breathable" layout to reduce cognitive load during medical data review. By layering translucent surfaces over a soft, organic background, the UI achieves a sense of depth and modernism without appearing overly decorative or "tech-heavy." The emotional response should be one of reassurance, safety, and technological intelligence.

## Colors

The palette is anchored by **Deep Teal**, chosen for its historical association with medical professionalism and digital trust. This is supported by **Soft Violet** for secondary data points and a clear semantic system for status indicators.

The background is a dynamic, layered environment. Use a linear gradient from top-left to bottom-right (#EAF3FB to #EAF7F1). Behind the primary glass containers, place large, 400px diameter blurred "blobs" in Teal, Blue, and Violet at 10% opacity to provide subtle chromatic depth without distracting from the data.

## Typography

The typographic hierarchy employs **Inter** for structural elements and headings to maintain a modern, geometric precision. **Open Sans** is utilized for all body copy and long-form data to leverage its superior legibility and humanist curves, which feel more approachable in a healthcare context.

Maintain generous line heights to ensure readability of clinical notes. Headings should always use the Charcoal Navy (#1C2B3A) color to ensure strong visual anchoring on translucent backgrounds.

## Layout & Spacing

This design system uses a **12-column fluid grid** for desktop, transitioning to a **4-column grid** for mobile. The layout relies on "Safe Zones"—internal padding within glass panels—to ensure content does not crowd the 20px rounded corners.

- **Desktop (1024px+):** 12 columns, 24px gutters, auto margins.
- **Tablet (768px - 1023px):** 8 columns, 20px gutters, 24px side margins.
- **Mobile (Up to 767px):** 4 columns, 16px gutters, 16px side margins.

Vertical rhythm is strictly maintained using multiples of 8px (24px, 40px, 64px) to create a structured, clinical feel.

## Elevation & Depth

Depth is established through physical layering and optical blurring rather than traditional heavy shadows.

- **The Surface:** All primary containers use `rgba(255, 255, 255, 0.55)` with a `backdrop-filter: blur(20px)`.
- **The Stroke:** Each glass panel must have a 1px solid border of `rgba(255, 255, 255, 0.6)` to simulate a "beveled edge" light catch.
- **The Shadow:** Use a singular, very diffuse shadow for floating elements: `0 8px 32px rgba(31, 41, 55, 0.08)`. This provides a subtle lift without muddying the background colors.
- **Level 1:** Background (Gradients/Blobs).
- **Level 2:** Main Content Panels (Glass).
- **Level 3:** Overlays, Modals, and Popovers (Glass with shadow).

## Shapes

The shape language is defined by large, friendly radii. Primary glass panels and cards use a **20px radius**. Interactive elements like buttons and chips should utilize a **Pill-shape (100px)** to distinguish them from the containers they sit within. 

Input fields and smaller components follow the `rounded-lg` (16px) standard to maintain harmony with the larger panel curves.

## Components

### Navigation
The top navbar is a fixed 72px tall frosted glass strip. It should have a 1px bottom border (`rgba(255, 255, 255, 0.3)`) and no shadow. Navigation links use Deep Teal for the active state with a 2px bottom indicator.

### Buttons
- **Primary:** Deep Teal (#0E7C9D) background, white text, pill-shaped.
- **Secondary:** Glass background, Deep Teal border (1px), Deep Teal text.
- **Ghost:** No background, Deep Teal text, used for less frequent actions.

### Cards & Panels
Cards are the standard container. They must always use the 20px blur and white border. For data-heavy cards, use a 24px internal padding.

### Forms
Input fields should be semi-transparent `rgba(255, 255, 255, 0.4)` with 16px rounding. On focus, the border color shifts to Deep Teal. Floating labels should use the `label-sm` typography style in Slate Gray (#5C6B7A).

### Data Visualization
Charts should avoid harsh black lines. Use Slate Gray for axes at 20% opacity. Use the Primary (Teal) and Secondary (Violet) colors for data series. Heatmaps for heart rate or risk should transition from Teal (Low) to Amber (Warning) to Coral-Red (Danger).
