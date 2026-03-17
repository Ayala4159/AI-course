# Detailed UI/UX Design Specification - Taskly Cozy Project

## 1. Design Philosophy: The "Cozy-Digital" Approach
The core objective of this project was to subvert the traditional, cold, and "institutional" feel of productivity apps. Most task managers focus on "efficiency" through rigid grids and stark white/blue contrasts. Our goal was to create a "Safe Space" for task management.

### 1.1 Visual Keywords
* **Weightlessness:** Elements should appear to float.
* **Softness:** Zero sharp corners. All radii are at least 20px-40px.
* **Etherealism:** A focus on feathers, clouds, and diffused lighting.

## 2. Technical UI Implementation
### 2.1 Background & Transparency (The Blur Factor)
We implemented a multi-layered background approach. 
* **Primary Layer:** A high-resolution macro photograph of feathers.
* **Overlay Layer:** A "Glassmorphism" container (`.dashboard`) with a background color of `rgba(255, 255, 255, 0.45)`.
* **Filtering:** To ensure readability despite the complex background, we applied `-webkit-backdrop-filter: blur(25px)`. This creates a frosted glass effect that separates the content from the background noise while maintaining the pastel color bleed.

### 2.2 Typography & Readability
We selected the **Plus Jakarta Sans** font for headings due to its modern, slightly geometric yet friendly curves. For the main Hebrew text, we used **Assistant** (Hebrew-optimized Sans Serif) to ensure that the RTL (Right-to-Left) layout remains professional and legible.

### 2.3 Interaction Feedback
* **Hover States:** Task cards use a subtle `scale(1.02)` and `translateX(-5px)` to simulate a "physical" lift when the user interacts with them.
* **Priority Dots:** Instead of harsh labels, we used glowing "Chalky" circles. 
    * *Critical:* Soft Red (`#ff9aa2`) with an 8px glow.
    * *Low:* Sage Green (`#e2f0cb`).