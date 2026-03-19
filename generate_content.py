#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         PROTEINER CONTENT CALENDAR GENERATOR                                ║
║         @proteiner.kr — High-Protein Fast Food Seoul                        ║
║         Automated Instagram Reel Generator — 16 Videos / 4 Weeks            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python generate_content.py

Requirements:
    pip install anthropic python-dotenv
    Set ANTHROPIC_API_KEY in your .env file or environment.

Output:
    Proteiner_Content_Calendar/
        RESEARCH_FINDINGS.txt
        Week1.txt  Week2.txt  Week3.txt  Week4.txt
        FULL_CALENDAR.txt
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# ── Dependency check ──────────────────────────────────────────────────────────
try:
    import anthropic
except ImportError:
    print("ERROR: 'anthropic' package not found.")
    print("Fix: pip install anthropic python-dotenv")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env loading is optional; key can be set in environment directly

# ── Constants ─────────────────────────────────────────────────────────────────
MODEL          = "claude-opus-4-6"
OUTPUT_DIR     = Path("Proteiner_Content_Calendar")
DIVIDER        = "━" * 80
THICK_DIVIDER  = "═" * 80

BRAND_CONTEXT = """
Brand Name    : Proteiner (프로티너)
Concept       : High-protein fast food
Instagram     : @proteiner.kr
Audience      : Korean fitness community, gym-goers, health-conscious Koreans, ages 18–35
Locations     : Sinchon, Seongsu, Gangnam, Sinnonhyeon, Yeouido (7 locations total)
Goal          : 100,000+ views per Instagram Reel
Tone          : Energetic, authentic, native Korean — never westernised or corporate
""".strip()

STYLE_REFS = [
    "@keanu.visuals     — cinematic slow-mo, moody colour grading, smooth cuts",
    "@learnwithkayo     — bold text overlays, educational pacing, strong scroll-stop hooks",
    "@stevenwommack     — lifestyle warmth, natural light, authentic everyday feel",
    "@build.withcrystal — satisfying process shots, clear step progression, clean framing",
    "@thepostprotocol   — structured storytelling, high-retention pacing, cliffhanger cuts",
]

CONTENT_TYPES = [
    "Protein reveal / macro showcase",
    "ASMR food sounds (no music — pure natural sound only)",
    "Gym and fitness lifestyle connection",
    "Pure entertainment — funny, satisfying, surprising, or emotional content featuring Proteiner",
    "Trending format creatively adapted to Proteiner food",
    "Storytelling or POV format",
    "Challenge or transformation format",
    "Behind-the-scenes or food preparation process",
]

FILMING_RULES = """
CRITICAL FILMING RULES (apply to every shot list):
1. No AI-generated people — ever.
2. The person filming cannot show other people — only themselves if necessary.
3. If a person appears: write "You will film yourself doing this." Specify exactly which body
   parts are visible (hands only / arms only / full body from behind). Avoid face shots.
4. If a face is absolutely required: write "FACE SWAP NEEDED — film yourself doing this action,
   then use Higgsfield face swap to replace your face."
5. Design most shots with NO person at all — food, environment, hands, abstract angles.
""".strip()

# ── Prompts ───────────────────────────────────────────────────────────────────

RESEARCH_PROMPT = f"""
You are a viral content researcher with expert-level knowledge of Instagram Reels,
YouTube Shorts, and TikTok as of early 2026.

TASK: Research the top trending content formats, hooks, and editing styles going viral
GLOBALLY across ALL niches — comedy, challenges, satisfying, life hacks, storytelling,
POV, reaction, transformation, sports, gaming, fashion, fitness, and food.

Then analyse how each format can be adapted for Proteiner (프로티너), a high-protein
fast food brand in Seoul targeting Korean fitness enthusiasts aged 18–35.

Korean social media context to factor in:
- Korean audiences respond strongly to: ASMR, satisfying food prep, gym lifestyle content,
  "real talk" honesty, transformation reveals, and community/challenge formats.
- Trending Korean content aesthetics: clean minimal framing, moody warm tones, bold Hangul
  text overlays, fast-cut editing with sound-sync, and authentic non-staged moments.
- Top Korean fitness creators use a mix of intensity and humour — never pure advertisement.

Return ONLY a valid JSON object (no markdown, no code fences) matching this exact schema:
{{
  "research_date": "YYYY-MM-DD",
  "top_viral_formats": [
    {{
      "format_name": "string",
      "description": "string",
      "why_it_works": "string",
      "proteiner_adaptation": "string",
      "trending_audio_style": "string"
    }}
  ],
  "hook_patterns": [
    {{
      "pattern": "string",
      "korean_example": "string (in Korean)",
      "why_it_stops_scroll": "string"
    }}
  ],
  "editing_trends": ["string"],
  "korean_specific_insights": ["string"],
  "content_calendar_strategy": "string"
}}

Include 12 viral formats, 8 hook patterns, 6 editing trends, 6 Korean insights.
Be specific, creative, and current. Think about what is actually going viral in early 2026.
"""


def build_week_prompt(week_num: int, research: dict, week_start: datetime) -> str:
    """Return the generation prompt for one week's 4 videos."""

    # Summarise research compactly to save tokens
    formats_summary = ""
    for f in research.get("top_viral_formats", [])[:10]:
        formats_summary += (
            f"  • {f.get('format_name','')}: {f.get('proteiner_adaptation','')}\n"
        )

    hooks_summary = ""
    for h in research.get("hook_patterns", [])[:6]:
        hooks_summary += f"  • {h.get('korean_example','')}\n"

    editing_trends = "\n".join(
        f"  • {t}" for t in research.get("editing_trends", [])
    )
    korean_insights = "\n".join(
        f"  • {i}" for i in research.get("korean_specific_insights", [])
    )
    strategy = research.get("content_calendar_strategy", "")

    dates = [(week_start + timedelta(days=d)).strftime("%A %b %d") for d in range(7)]
    style_refs_block = "\n".join(STYLE_REFS)
    content_types_block = "\n".join(f"  {i+1}. {ct}" for i, ct in enumerate(CONTENT_TYPES))

    return f"""
You are the senior creative director for @proteiner.kr — a high-protein fast food brand
in Seoul, South Korea. Your job is to generate Week {week_num} of a 4-week Instagram Reel
content calendar. Each video must be genuinely entertaining AND brand-relevant.

══════════════════════════════════════════════════════════════════
BRAND
══════════════════════════════════════════════════════════════════
{BRAND_CONTEXT}

══════════════════════════════════════════════════════════════════
STYLE REFERENCES
══════════════════════════════════════════════════════════════════
{style_refs_block}

══════════════════════════════════════════════════════════════════
RESEARCH — TRENDING FORMATS TO DRAW FROM
══════════════════════════════════════════════════════════════════
Proteiner adaptations of top viral formats:
{formats_summary}
Proven Korean scroll-stop hooks:
{hooks_summary}
Current editing trends:
{editing_trends}
Korean audience insights:
{korean_insights}
Overall calendar strategy: {strategy}

══════════════════════════════════════════════════════════════════
FILMING RULES
══════════════════════════════════════════════════════════════════
{FILMING_RULES}

══════════════════════════════════════════════════════════════════
CONTENT TYPES (rotate — do not repeat the same type twice in one week)
══════════════════════════════════════════════════════════════════
{content_types_block}

══════════════════════════════════════════════════════════════════
WEEK {week_num} DATES:  {dates[0]} → {dates[6]}
══════════════════════════════════════════════════════════════════

Generate exactly 4 Instagram Reel ideas for Week {week_num}.
Use 4 DIFFERENT content types from the list above.
Each idea must be scroll-stopping, culturally Korean, and production-ready.

Use this EXACT output format for every video — no deviations:

{THICK_DIVIDER}
VIDEO [X] OF 4  |  WEEK {week_num}
{THICK_DIVIDER}

1. VIDEO TITLE
[Short internal name — 3–6 words]

2. HOOK  (Korean — first 3 seconds)
[Exact Korean text or on-screen visual that appears in the first 3 seconds.
 Must be designed to stop the scroll immediately. Must be in Korean (한국어).]

3. CONCEPT
[2–3 sentences: what this video is, which trending format it is adapted from,
 and exactly why it will perform well with the Korean fitness audience.]

4. WHAT TO FILM
[Detailed shot list. Include exact angles (overhead / close-up / side /
 macro / Dutch tilt etc.), lighting tips, duration per shot, and what
 specific moments to capture.
 Apply filming rules above — specify body parts if person appears.
 Use "FACE SWAP NEEDED" if a face is required.]

5. CAPCUT EDITING INSTRUCTIONS
Step 1: ...
Step 2: ...
[Cover: clip order, speed ramps, transitions, text overlays with EXACT Korean
 wording, font style, animation type, music genre to search in CapCut,
 colour filter/LUT to apply, caption placement, auto-caption on/off.
 Assume basic CapCut knowledge — spell out every single step.]

6. HIGGSFIELD AI INSTRUCTIONS
[Option A — If AI visuals are needed:
   Provide the exact Higgsfield prompt as a JSON object:
   {{
     "subject": "...",
     "style": "...",
     "mood": "...",
     "lighting": "...",
     "camera_movement": "...",
     "aspect_ratio": "9:16",
     "additional_details": "..."
   }}
 Option B — If face swap is needed:
   "FACE SWAP — film yourself performing [action]. In Higgsfield use Face Swap:
    upload your face photo, apply to footage. Settings: [specific settings]."
 Option C — If not needed:
   "Not needed for this video."]

7. INSTAGRAM CAPTION
[Full Korean caption — ready to copy-paste. Include:
 • Strong opening line (first line = hook)
 • Main message / story
 • Save prompt ("저장해두세요!" or similar)
 • Call to action
 • Location tag suggestion
 • 20–25 hashtags mixing Korean and English tags (fitness, food, Seoul culture)]

8. BEST TIME TO POST
[Day of week + exact time in KST — based on Korean fitness audience activity.]

9. PREDICTED VIRAL FACTOR
[One sentence: why this specific video has 100k+ view potential, which trending
 format powers it, and why that format resonates with this audience.]

{DIVIDER}

Generate all 4 videos now. Make every hook genuinely scroll-stopping in Korean.
Make every Higgsfield JSON prompt complete and paste-ready with zero modifications.
Make every video feel like it was made by a Korean creator, not a foreign brand.
"""


# ── API Calls ─────────────────────────────────────────────────────────────────

def call_api(client: anthropic.Anthropic, prompt: str, max_tokens: int,
             label: str, retries: int = 4) -> str:
    """Call the Claude API with exponential backoff on failure."""
    wait = 2
    for attempt in range(1, retries + 1):
        try:
            msg = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text
        except anthropic.RateLimitError:
            print(f"   ⚠  Rate limit hit for {label}. Waiting {wait}s...")
            time.sleep(wait)
            wait *= 2
        except anthropic.APIConnectionError:
            if attempt == retries:
                raise
            print(f"   ⚠  Connection error for {label}. Retrying in {wait}s...")
            time.sleep(wait)
            wait *= 2
        except anthropic.APIStatusError as e:
            print(f"   ✗  API error {e.status_code}: {e.message}")
            raise
    raise RuntimeError(f"Failed to complete {label} after {retries} attempts.")


def run_research_phase(client: anthropic.Anthropic) -> dict:
    """Phase 1 — Research trending formats. Returns structured dict."""
    print("\n" + DIVIDER)
    print("  PHASE 1 — RESEARCH: Analysing global viral trends + Korean social media")
    print(DIVIDER)
    print("  Studying: Instagram Reels, TikTok, YouTube Shorts across all niches")
    print("  Identifying: hooks, formats, editing styles, Korean audience insights\n")

    raw = call_api(client, RESEARCH_PROMPT, max_tokens=4096, label="Research")

    # Strip markdown fences if present  (```json ... ``` or ``` ... ```)
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]                          # drop opening fence / language tag
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]                     # drop closing fence
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Best-effort: try to extract JSON object
        start = text.find("{")
        end   = text.rfind("}") + 1
        if start != -1 and end > start:
            try:
                data = json.loads(text[start:end])
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

    # Provide fallback values so the rest of the script always works
    data.setdefault("research_date", datetime.now().strftime("%Y-%m-%d"))
    data.setdefault("top_viral_formats", [])
    data.setdefault("hook_patterns", [])
    data.setdefault("editing_trends", [])
    data.setdefault("korean_specific_insights", [])
    data.setdefault("content_calendar_strategy",
                    "Blend globally trending viral formats with Korean fitness culture "
                    "to create authentic, entertaining content that drives shares and saves.")
    data["_raw_research"] = raw   # keep original in case of partial parse

    print(f"  ✅ Research complete — {len(data.get('top_viral_formats',[]))} viral formats identified")
    return data


def generate_week(client: anthropic.Anthropic, week_num: int,
                  research: dict, week_start: datetime) -> str:
    """Phase 2 — Generate 4 video ideas for one week."""
    print(f"\n  Generating Week {week_num} (4 videos)...", end="", flush=True)
    prompt  = build_week_prompt(week_num, research, week_start)
    content = call_api(client, prompt, max_tokens=8000, label=f"Week {week_num}")
    print(" ✅")
    return content


# ── File Writers ──────────────────────────────────────────────────────────────

def week_header(week_num: int, week_start: datetime, gen_date: str) -> str:
    week_end = week_start + timedelta(days=6)
    return f"""
{THICK_DIVIDER}
  PROTEINER (@proteiner.kr) — INSTAGRAM REEL CONTENT CALENDAR
  WEEK {week_num} OF 4  |  {week_start.strftime("%b %d")} – {week_end.strftime("%b %d, %Y")}
{THICK_DIVIDER}
Generated : {gen_date}
Brand     : Proteiner (프로티너) — High-Protein Fast Food Seoul
Goal      : 100,000+ views per Reel

HOW TO USE THIS FILE
  1. Read each video plan fully before picking up a camera.
  2. Film all shots listed under WHAT TO FILM.
  3. Edit in CapCut following every numbered step exactly.
  4. Generate AI shots / face swaps via Higgsfield (instructions included).
  5. Copy-paste the Instagram caption — it is ready to use.
  6. Post at the exact time listed. Do not post early or late.

{DIVIDER}
"""


def research_summary_block(research: dict) -> str:
    lines = [
        "",
        THICK_DIVIDER,
        "  RESEARCH FINDINGS (auto-generated at runtime)",
        THICK_DIVIDER,
        f"  Date      : {research.get('research_date', 'N/A')}",
        f"  Strategy  : {research.get('content_calendar_strategy', '')}",
        "",
        "  TOP VIRAL FORMATS IDENTIFIED:",
    ]
    for f in research.get("top_viral_formats", []):
        lines.append(f"  • {f.get('format_name','')}")
        lines.append(f"    → Proteiner adaptation: {f.get('proteiner_adaptation','')}")
    lines += ["", "  KOREAN AUDIENCE INSIGHTS:"]
    for i in research.get("korean_specific_insights", []):
        lines.append(f"  • {i}")
    lines += ["", "  CURRENT EDITING TRENDS:"]
    for t in research.get("editing_trends", []):
        lines.append(f"  • {t}")
    lines += ["", DIVIDER, ""]
    return "\n".join(lines)


def write_week_file(week_num: int, content: str,
                    week_start: datetime, gen_date: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / f"Week{week_num}.txt"
    header = week_header(week_num, week_start, gen_date)
    footer = f"\n{DIVIDER}\n  END OF WEEK {week_num} — {week_start.strftime('%b %d')} to {(week_start+timedelta(6)).strftime('%b %d, %Y')}\n{DIVIDER}\n"
    path.write_text(header + content + footer, encoding="utf-8")
    return path


def write_full_calendar(all_weeks: list, research: dict,
                        week_starts: list, gen_date: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / "FULL_CALENDAR.txt"

    master_header = f"""
{THICK_DIVIDER}
  PROTEINER (@proteiner.kr) — FULL 4-WEEK INSTAGRAM REEL CALENDAR
  16 Videos — Production-Ready — Generated {gen_date}
{THICK_DIVIDER}

  Brand     : Proteiner (프로티너) — High-Protein Fast Food Seoul
  Instagram : @proteiner.kr
  Locations : Sinchon · Seongsu · Gangnam · Sinnonhyeon · Yeouido (7 locations)
  Audience  : Korean fitness community, ages 18–35
  Goal      : 100,000+ views per Reel

  CALENDAR OVERVIEW
  {DIVIDER}
  Week 1 — {week_starts[0].strftime('%b %d')} to {(week_starts[0]+timedelta(6)).strftime('%b %d')}  |  Videos 1–4
  Week 2 — {week_starts[1].strftime('%b %d')} to {(week_starts[1]+timedelta(6)).strftime('%b %d')}  |  Videos 5–8
  Week 3 — {week_starts[2].strftime('%b %d')} to {(week_starts[2]+timedelta(6)).strftime('%b %d')}  |  Videos 9–12
  Week 4 — {week_starts[3].strftime('%b %d')} to {(week_starts[3]+timedelta(6)).strftime('%b %d')}  |  Videos 13–16
  {DIVIDER}
"""

    sections = [master_header, research_summary_block(research)]
    for i, (content, ws) in enumerate(zip(all_weeks, week_starts), 1):
        sections.append(week_header(i, ws, gen_date))
        sections.append(content)
        we = ws + timedelta(6)
        sections.append(
            f"\n{DIVIDER}\n  END OF WEEK {i} — {ws.strftime('%b %d')} to {we.strftime('%b %d, %Y')}\n{DIVIDER}\n\n"
        )

    sections.append(f"\n{THICK_DIVIDER}\n  END OF FULL CALENDAR — ALL 16 VIDEOS\n{THICK_DIVIDER}\n")
    path.write_text("".join(sections), encoding="utf-8")
    return path


def write_research_file(research: dict, gen_date: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / "RESEARCH_FINDINGS.txt"
    header = (
        f"PROTEINER CONTENT RESEARCH FINDINGS\n"
        f"Generated : {gen_date}\n"
        f"{DIVIDER}\n\n"
    )
    path.write_text(
        header + json.dumps(research, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return path


# ── Main ──────────────────────────────────────────────────────────────────────

def print_banner():
    print(f"""
{THICK_DIVIDER}
  PROTEINER CONTENT CALENDAR GENERATOR
  @proteiner.kr — High-Protein Fast Food Seoul
  Building 16 Instagram Reel ideas across 4 weeks
{THICK_DIVIDER}
""")


def compute_week_starts() -> list:
    """Return 4 Monday dates starting from next Monday."""
    today = datetime.now()
    days_ahead = (7 - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7  # always start NEXT Monday, not today
    first_monday = today + timedelta(days=days_ahead)
    return [first_monday + timedelta(weeks=i) for i in range(4)]


def main():
    print_banner()

    # ── API key check ─────────────────────────────────────────────────────────
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY is not set.\n")
        print("How to fix:")
        print("  Windows CMD  : set ANTHROPIC_API_KEY=sk-ant-...")
        print("  Windows PS   : $env:ANTHROPIC_API_KEY='sk-ant-...'")
        print("  Or add it to the .env file in this folder.")
        print("\nGet your key at: https://console.anthropic.com/")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    gen_date   = datetime.now().strftime("%B %d, %Y at %H:%M")
    week_starts = compute_week_starts()

    print(f"  Output folder : {OUTPUT_DIR}/")
    print(f"  Week 1 starts : {week_starts[0].strftime('%A, %B %d, %Y')}")
    print(f"  Model         : {MODEL}\n")

    # ── Phase 1: Research ─────────────────────────────────────────────────────
    research = run_research_phase(client)
    rf_path  = write_research_file(research, gen_date)
    print(f"  Saved: {rf_path}")

    # ── Phase 2: Generate weeks ───────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print("  PHASE 2 — CONTENT GENERATION: 4 weeks × 4 videos = 16 Reels")
    print(DIVIDER)

    all_weeks = []
    for i in range(1, 5):
        content = generate_week(client, i, research, week_starts[i - 1])
        all_weeks.append(content)
        wf_path = write_week_file(i, content, week_starts[i - 1], gen_date)
        print(f"  Saved: {wf_path}")
        if i < 4:
            time.sleep(1)  # polite pause between requests

    # ── Master file ───────────────────────────────────────────────────────────
    print(f"\n  Writing master calendar...", end="", flush=True)
    fc_path = write_full_calendar(all_weeks, research, week_starts, gen_date)
    print(f" ✅\n  Saved: {fc_path}")

    # ── Done ──────────────────────────────────────────────────────────────────
    print(f"""
{THICK_DIVIDER}
  ✅  CONTENT CALENDAR COMPLETE
{THICK_DIVIDER}

  Files created inside  {OUTPUT_DIR}/
  ┌─────────────────────────────────────────────────────────────┐
  │  RESEARCH_FINDINGS.txt  —  Trending format research         │
  │  Week1.txt              —  Videos 1–4                       │
  │  Week2.txt              —  Videos 5–8                       │
  │  Week3.txt              —  Videos 9–12                      │
  │  Week4.txt              —  Videos 13–16                     │
  │  FULL_CALENDAR.txt      —  All 16 videos in one file        │
  └─────────────────────────────────────────────────────────────┘

  NEXT STEPS
  1. Open FULL_CALENDAR.txt for a complete overview
  2. Open each Week file when you are ready to film that week
  3. Film using the shot list in each WHAT TO FILM section
  4. Edit in CapCut following every numbered step
  5. Generate AI visuals with the Higgsfield JSON prompts
  6. Post at the exact KST time shown — timing is critical

  Run this script again anytime to regenerate with fresh research.

{THICK_DIVIDER}
""")


if __name__ == "__main__":
    main()
