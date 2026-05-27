---
name: Don't Read oversized PNGs directly
description: When verifying PNG renders from deck/graphic builds, never open files larger than ~2000px on the long edge with the Read tool — it breaks the conversation's image budget and walls the session.
type: feedback
originSessionId: 8ca1f606-f5f3-410d-96f9-947a8fcbb8e3
---
Never use the Read tool on PNG files larger than ~2000px on the longest edge. This applies especially to 1920×1080 (and larger) slide renders, retina/2x exports, and 3840×2160 4K renders produced by the Metafore deck/graphic/brochure pipelines.

**Why:** During the May 2026 metafore-deck build session, reading a 3840×2160 verification PNG triggered "An image in the conversation exceeds the dimension limit for many-image requests (2000px)" and every subsequent turn errored out — the session hit its message-request wall and had to be handed off to a new chat.

**How to apply:** To inspect rendered output, either:
1. Render at ≤1920×1080 (under the 2000px cap)
2. Downscale a copy first via Python/PIL or `sips -Z 1600 input.png --out preview.png` before Read
3. Inspect dimensions/colors programmatically (PIL, ImageMagick `identify`) without loading into the conversation
4. For PPTX builds specifically: verify by opening the .pptx file structure or running the build script's exit code, not by reading the slide PNG renders directly

This rule applies to any Metafore HTML→image pipeline (deck, brochure, graphic, dashboard).
