#!/usr/bin/env python3
"""
Proteiner Instagram Content Generation System
==============================================
Generates a 4-week Instagram content calendar for @proteiner.kr
including Korean captions, Higgsfield AI prompts, and CapCut editing instructions.

Usage:
    python proteiner_generator.py

Requirements:
    pip install anthropic

Environment:
    ANTHROPIC_API_KEY must be set in your environment or .env file.
"""

import anthropic
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from brand_identity import BRAND, CONTENT_THEMES
from reference_styles import EDIT_REFERENCES, VIDEO_CREATION_REFERENCES, get_style_brief_for_video


# ─── Configuration ────────────────────────────────────────────────────────────

MODEL = "claude-opus-4-6"
OUTPUT_BASE = Path("Proteiner_Content_Calendar")

# ─── Claude Client ────────────────────────────────────────────────────────────

def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n❌  ANTHROPIC_API_KEY not found in environment.")
        print("    Set it with:  export ANTHROPIC_API_KEY='your-key-here'")
        print("    Or create a .env file and run:  python -m dotenv run python proteiner_generator.py")
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


# ─── Prompt Builders ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = f"""
You are a senior social media strategist and content creator specializing in Korean fitness brands and Instagram Reels.

You are working for PROTEINER (@proteiner.kr) — a high-protein fast food brand in Seoul, South Korea.

BRAND DNA:
- Target: 헬스인 (gym-goers), 다이어터, fitness-conscious Koreans aged 20–35
- Tone: Energetic, confident, science-backed. Friendly yet professional.
- Locations: 강남 (Gangnam), 신촌 (Sinchon), 성수 (Seongsu)
- Brand colors: #FF4D00 (power orange), #1A1A1A (deep black), #FFFFFF (clean white)
- Brand voice keywords: 고단백, 맛있다, 빠르다, 채워라, 프로틴, 린바디

REFERENCE EDIT STYLES you draw from:
1. @keanu.visuals — Cinematic dark aesthetic, slow-mo food drops, crushed blacks, lo-fi trap music
2. @learnwithkayo — Educational text-heavy, rapid cuts, bold stats, bright high-contrast
3. @stevenwommack — Fitness lifestyle, warm golden tones, handheld authenticity, gym-to-food narrative
4. @build.withcrystal — 3-act storytelling: Problem → Framework → Transformation
5. @thepostprotocol — Performance-engineered: open loops, comparison formats, re-engagement at 7s mark

OUTPUT LANGUAGE:
- Captions: Korean (한국어) with strategic English words for emphasis
- Hashtags: Mix of Korean and English hashtags
- CapCut instructions: English (for clarity)
- Higgsfield prompts: English (the tool requires English)

Always be specific, actionable, and on-brand.
""".strip()


def build_caption_prompt(week_num: int, video_num: int, video_info: dict, style_brief: dict) -> str:
    hashtags = BRAND["hashtags"]
    all_hashtags = (
        hashtags["core"] + hashtags["fitness"][:4] +
        hashtags["food"][:4] + hashtags["trending_kr"][:3]
    )

    return f"""
Generate a Korean Instagram caption for this Proteiner video:

VIDEO DETAILS:
- Week {week_num}, Video {video_num}
- Type: {video_info['type']}
- Content Pillar: {video_info['pillar']}
- Hook: {video_info['hook']}
- Theme: {CONTENT_THEMES[f'week_{week_num}']['theme']}

STYLE BRIEF: {style_brief['brief']}

CAPTION REQUIREMENTS:
1. Open with a punchy Korean hook (1–2 lines) that mirrors the video hook
2. Middle: 2–4 lines of value/story (Korean, conversational)
3. End with a CTA that drives to: follow, visit the store, or save the post
4. Signature sign-off: 📍 {' / '.join(BRAND['locations'][:2])} #프로테이너
5. Hashtags (15–20 tags): use a mix from these pools — {', '.join(all_hashtags[:12])}...

FORMAT:
[Hook line]
[Body — 2–4 lines]
[CTA]
[Location sign-off]
.
.
.
[Hashtags — separated by spaces]

Make it feel human, authentic, and shareable. Avoid corporate stiffness.
""".strip()


def build_higgsfield_prompt(week_num: int, video_num: int, video_info: dict, style_brief: dict) -> str:
    primary_ref = style_brief["primary_edit_ref"]
    ref_data = EDIT_REFERENCES.get(primary_ref, {})
    color_tone = ref_data.get("analysis", {}).get("color_tone", "Cinematic, warm tones")

    return f"""
Generate a Higgsfield AI image/video generation prompt for this Proteiner content:

VIDEO CONTEXT:
- Type: {video_info['type']}
- Pillar: {video_info['pillar']}
- Hook: {video_info['hook']}
- Edit Style Reference: @{primary_ref}
- Color Tone Guide: {color_tone}

BRAND COLORS: Orange (#FF4D00), Black (#1A1A1A), White (#FFFFFF)
BRAND: High-protein fast food, Korean fitness audience, Seoul urban setting

PROMPT REQUIREMENTS:
Create a detailed Higgsfield AI prompt that captures:
1. The SUBJECT (what's in the shot — food, person, location)
2. The COMPOSITION (angle, framing, depth of field)
3. The LIGHTING (style, direction, quality)
4. The COLOR GRADE (matching the edit reference style)
5. The MOTION/CAMERA MOVEMENT (if video generation)
6. The MOOD (emotional feel)
7. Technical specs: aspect ratio (9:16 for Reels), quality modifiers

FORMAT:
[One detailed paragraph prompt — 80–120 words]

Then on a new line:
NEGATIVE PROMPT: [what to avoid]

Make the prompt specific enough that Higgsfield generates a usable hero shot or background plate.
""".strip()


def build_capcut_prompt(week_num: int, video_num: int, video_info: dict, style_brief: dict) -> str:
    primary_ref = EDIT_REFERENCES.get(style_brief["primary_edit_ref"], {})
    secondary_ref = EDIT_REFERENCES.get(style_brief.get("secondary_edit_ref", ""), {})

    primary_pacing = primary_ref.get("analysis", {}).get("pacing", "")
    primary_music = primary_ref.get("analysis", {}).get("music_energy", "")
    primary_color = primary_ref.get("analysis", {}).get("color_tone", "")
    primary_text = primary_ref.get("analysis", {}).get("text_placement", "")

    return f"""
Generate step-by-step CapCut editing instructions for this Proteiner video:

VIDEO DETAILS:
- Week {week_num}, Video {video_num}
- Type: {video_info['type']}
- Pillar: {video_info['pillar']}
- Hook: {video_info['hook']}

PRIMARY EDIT REFERENCE (@{style_brief['primary_edit_ref']}):
- Pacing: {primary_pacing}
- Music Energy: {primary_music}
- Color Tone: {primary_color}
- Text Style: {primary_text}

SECONDARY REFERENCE (@{style_brief.get('secondary_edit_ref', 'stevenwommack')}):
- Used for: specific transitions or scene types as noted

CAPCUT INSTRUCTIONS FORMAT:
Provide instructions in clear numbered steps for:

1. FOOTAGE SETUP
   - What shots to film (list each clip with duration + camera angle)
   - Order in the timeline

2. BASIC EDITING
   - Cut points (timecodes)
   - Speed adjustments (slow-mo, fast-mo)

3. TRANSITIONS
   - Between each clip (type + timing)

4. TEXT OVERLAYS
   - What text, where on screen, what timestamp, what animation style in CapCut

5. COLOR GRADING
   - CapCut filter name (if any) or manual LUT/adjustment values
   - Specific: Brightness, Contrast, Saturation, Shadow, Highlight, Color Temperature

6. MUSIC
   - Genre + BPM target
   - Where the music beat drop should sync to which visual cut
   - Volume automation (when to duck for voiceover if needed)

7. FINAL TOUCHES
   - Stickers or effects (CapCut library suggestions)
   - Export settings: 1080x1920, 60fps, max quality

8. PROTEINER BRANDING
   - Logo placement (bottom-right, 80% opacity)
   - Brand color text: #FF4D00 for CTAs
   - Outro: 2s black card with logo + location tag

Be specific and beginner-friendly. Use CapCut's exact menu names where possible.
""".strip()


# ─── Content Generator ────────────────────────────────────────────────────────

def generate_content_piece(
    client: anthropic.Anthropic,
    prompt: str,
    content_type: str,
    week: int,
    video: int,
) -> str:
    """Generate a single piece of content using Claude API with streaming."""
    print(f"      ⏳ Generating {content_type}...", end="", flush=True)

    full_response = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=2000,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_response += text

    print(f" ✓ ({len(full_response)} chars)")
    return full_response.strip()


def generate_video_content(
    client: anthropic.Anthropic,
    week_num: int,
    video_num: int,
    video_info: dict,
) -> dict:
    """Generate all content pieces for a single video."""
    style_brief = get_style_brief_for_video(video_info["pillar"])

    caption = generate_content_piece(
        client,
        build_caption_prompt(week_num, video_num, video_info, style_brief),
        "Korean Caption",
        week_num,
        video_num,
    )
    time.sleep(0.5)  # brief pause between API calls

    higgsfield = generate_content_piece(
        client,
        build_higgsfield_prompt(week_num, video_num, video_info, style_brief),
        "Higgsfield Prompt",
        week_num,
        video_num,
    )
    time.sleep(0.5)

    capcut = generate_content_piece(
        client,
        build_capcut_prompt(week_num, video_num, video_info, style_brief),
        "CapCut Instructions",
        week_num,
        video_num,
    )

    return {
        "video_info": video_info,
        "style_brief": style_brief,
        "caption": caption,
        "higgsfield_prompt": higgsfield,
        "capcut_instructions": capcut,
    }


# ─── File Savers ──────────────────────────────────────────────────────────────

def save_video_content(
    base_dir: Path,
    week_num: int,
    video_num: int,
    day: str,
    content: dict,
) -> Path:
    """Save all content files for a single video into organized folders."""
    # Create folder name: Week_1/Video_1_Monday
    day_clean = day.split(" ")[0]  # "월요일" from "월요일 (Monday)"
    folder_name = f"Video_{video_num}_{day_clean}"
    video_dir = base_dir / f"Week_{week_num}" / folder_name
    video_dir.mkdir(parents=True, exist_ok=True)

    video_info = content["video_info"]
    style = content["style_brief"]

    # ── Caption file
    caption_file = video_dir / "caption_KO.txt"
    caption_content = f"""📱 PROTEINER INSTAGRAM CAPTION — Week {week_num} Video {video_num}
{'='*60}
Video Type : {video_info['type']}
Content Pillar: {video_info['pillar']}
Hook Concept : {video_info['hook']}
Style Ref    : @{style['primary_edit_ref']} + @{style.get('secondary_edit_ref', '')}
{'='*60}

{content['caption']}
"""
    caption_file.write_text(caption_content, encoding="utf-8")

    # ── Higgsfield prompt file
    higgsfield_file = video_dir / "higgsfield_ai_prompt.txt"
    higgsfield_content = f"""🎨 HIGGSFIELD AI PROMPT — Week {week_num} Video {video_num}
{'='*60}
Video Type   : {video_info['type']}
Color Style  : Based on @{style['primary_edit_ref']} aesthetic
{'='*60}

{content['higgsfield_prompt']}

─────────────────────────────────────────────────────────
HOW TO USE IN HIGGSFIELD AI:
1. Go to higgsfield.ai
2. Select "Image Generation" or "Video Generation"
3. Paste the prompt above into the prompt field
4. Set aspect ratio to 9:16 (portrait for Reels)
5. Set quality to highest available
6. Paste the NEGATIVE PROMPT in the negative field
7. Generate 3–4 variations and pick the best
8. Download and import into CapCut as a background/hero shot
─────────────────────────────────────────────────────────
"""
    higgsfield_file.write_text(higgsfield_content, encoding="utf-8")

    # ── CapCut instructions file
    capcut_file = video_dir / "capcut_editing_instructions.txt"
    capcut_content = f"""🎬 CAPCUT EDITING INSTRUCTIONS — Week {week_num} Video {video_num}
{'='*60}
Video Type    : {video_info['type']}
Edit Style    : @{style['primary_edit_ref']} (primary) + @{style.get('secondary_edit_ref', '')} (secondary)
Style Brief   : {style['brief']}
Content Pillar: {video_info['pillar']}
{'='*60}

{content['capcut_instructions']}

─────────────────────────────────────────────────────────
QUICK CHECKLIST BEFORE EXPORT:
[ ] Proteiner logo added (bottom-right, 80% opacity)
[ ] Orange (#FF4D00) used for CTA text
[ ] Music beat synced to main visual cut
[ ] First 3 seconds: hook is clear and compelling
[ ] Last 2 seconds: CTA or outro visible
[ ] Aspect ratio: 9:16 (1080 x 1920)
[ ] Export: 60fps, maximum quality
[ ] Review on phone screen before posting
─────────────────────────────────────────────────────────
"""
    capcut_file.write_text(capcut_content, encoding="utf-8")

    # ── Quick reference card
    quick_ref_file = video_dir / "QUICK_REFERENCE.txt"
    quick_ref = f"""⚡ QUICK REFERENCE — Week {week_num} Video {video_num} ({day})
{'='*60}

📌 VIDEO CONCEPT:
   {video_info['type']}

🎣 HOOK:
   "{video_info['hook']}"

🎨 EDIT STYLE:
   Primary : @{style['primary_edit_ref']}
   Secondary: @{style.get('secondary_edit_ref', '')}

📁 FILES IN THIS FOLDER:
   📝 caption_KO.txt              → Copy-paste caption for Instagram
   🎨 higgsfield_ai_prompt.txt    → Use on higgsfield.ai for visuals
   🎬 capcut_editing_instructions.txt → Step-by-step edit guide

💡 WORKFLOW:
   1. Film the shots listed in capcut_editing_instructions.txt
   2. Generate visual assets using higgsfield_ai_prompt.txt
   3. Edit in CapCut following the instructions
   4. Copy caption from caption_KO.txt when posting
   5. Post on {day.split('(')[0].strip()} and engage for first 60 minutes!
"""
    quick_ref_file.write_text(quick_ref, encoding="utf-8")

    return video_dir


def save_calendar_overview(base_dir: Path, all_content: list) -> Path:
    """Save the master content calendar overview file."""
    overview_file = base_dir / "CONTENT_CALENDAR_OVERVIEW.txt"

    # Calculate posting dates starting from next Monday
    today = datetime.now()
    days_until_monday = (7 - today.weekday()) % 7 or 7
    start_date = today + timedelta(days=days_until_monday)

    lines = [
        "📅 PROTEINER 4-WEEK INSTAGRAM CONTENT CALENDAR",
        "=" * 65,
        f"   Brand: @proteiner.kr",
        f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"   Calendar Start: {start_date.strftime('%Y년 %m월 %d일')} (Monday)",
        f"   Posting Frequency: 3x per week (Mon / Wed / Fri)",
        f"   Total Videos: 12",
        "=" * 65,
        "",
    ]

    week_offsets = {1: 0, 2: 7, 3: 14, 4: 21}
    day_offsets = {"월요일": 0, "수요일": 2, "금요일": 4}

    for week_num in range(1, 5):
        week_data = CONTENT_THEMES[f"week_{week_num}"]
        week_start = start_date + timedelta(days=week_offsets[week_num])

        lines.extend([
            f"",
            f"┌─ WEEK {week_num}: {week_data['theme']}",
            f"│  Goal: {week_data['goal']}",
            f"│  Dates: {week_start.strftime('%m/%d')} – {(week_start + timedelta(days=4)).strftime('%m/%d')}",
            f"│",
        ])

        for v_num, video in enumerate(week_data["videos"], 1):
            day_kr = video["day"].split(" ")[0]
            day_offset = day_offsets.get(day_kr, 0)
            post_date = week_start + timedelta(days=day_offset)

            lines.extend([
                f"│  📹 Video {v_num} — {video['day']}  ({post_date.strftime('%m/%d')})",
                f"│     Type  : {video['type']}",
                f"│     Pillar: {video['pillar']}",
                f"│     Hook  : {video['hook']}",
                f"│     Folder: Week_{week_num}/Video_{v_num}_{day_kr}/",
                f"│",
            ])

        lines.append(f"└{'─'*63}")

    lines.extend([
        "",
        "=" * 65,
        "📌 HOW TO USE THIS CALENDAR",
        "=" * 65,
        "",
        "WEEKLY WORKFLOW:",
        "  Monday morning  → Film + edit Monday video → Post by 7–9 PM KST",
        "  Tuesday         → Film Wednesday content",
        "  Wednesday       → Edit + post Wednesday video (7–9 PM KST)",
        "  Thursday        → Film Friday content + prep next week",
        "  Friday          → Edit + post Friday video (7–9 PM KST)",
        "",
        "BEST POSTING TIMES (KST):",
        "  Peak engagement: 7:00 PM – 9:00 PM",
        "  Secondary: 12:00 PM – 1:00 PM (lunch)",
        "  Morning window: 7:00 AM – 8:00 AM",
        "",
        "ENGAGEMENT PROTOCOL (first 60 min after posting):",
        "  1. Reply to EVERY comment within 60 minutes",
        "  2. Engage with 10–15 posts from relevant hashtags",
        "  3. Share to Stories immediately after posting",
        "  4. Pin a strong comment on the post",
        "  5. Track views at 1h, 6h, 24h",
        "",
        "FILES IN EACH VIDEO FOLDER:",
        "  📝 caption_KO.txt              → Ready-to-post Korean caption",
        "  🎨 higgsfield_ai_prompt.txt    → AI image generation prompt",
        "  🎬 capcut_editing_instructions.txt → Full editing guide",
        "  ⚡ QUICK_REFERENCE.txt          → Summary + workflow checklist",
        "",
        "=" * 65,
    ])

    overview_file.write_text("\n".join(lines), encoding="utf-8")
    return overview_file


def save_style_analysis(base_dir: Path) -> Path:
    """Save the reference style analysis document."""
    style_file = base_dir / "REFERENCE_STYLE_ANALYSIS.txt"

    lines = [
        "🎨 REFERENCE PAGE STYLE ANALYSIS",
        "=" * 65,
        "   Used as creative direction for all Proteiner content",
        "=" * 65,
        "",
        "─── EDITING REFERENCES ─────────────────────────────────────",
        "",
    ]

    for handle, data in EDIT_REFERENCES.items():
        analysis = data["analysis"]
        lines.extend([
            f"📱 @{handle} — {data['style_category']}",
            f"",
            f"   Hook Structure:",
            f"   {analysis['hook_structure']}",
            f"",
            f"   Editing Style:",
            f"   {analysis['editing_style']}",
            f"",
            f"   Text Placement:",
            f"   {analysis['text_placement']}",
            f"",
            f"   Pacing Guide:",
            f"   {analysis['pacing']}",
            f"",
            f"   Color Tone: {analysis['color_tone']}",
            f"   Music Energy: {analysis['music_energy']}",
            f"",
            f"   ✅ Apply to Proteiner:",
            f"   {analysis['apply_to_proteiner']}",
            f"",
            f"{'─'*63}",
            "",
        ])

    lines.extend([
        "─── VIDEO CREATION REFERENCES ───────────────────────────────",
        "",
    ])

    for handle, data in VIDEO_CREATION_REFERENCES.items():
        analysis = data["analysis"]
        lines.extend([
            f"📱 @{handle} — {data['style_category']}",
            f"",
            f"   Content Structure:",
            f"   {analysis['content_structure']}",
            f"",
            f"   Storytelling:",
            f"   {analysis['storytelling']}",
            f"",
            f"   Visual Approach:",
            f"   {analysis['visual_approach']}",
            f"",
            f"   ✅ Apply to Proteiner:",
            f"   {analysis['apply_to_proteiner']}",
            f"",
            f"{'─'*63}",
            "",
        ])

    style_file.write_text("\n".join(lines), encoding="utf-8")
    return style_file


def save_video_download_guide(base_dir: Path) -> Path:
    """Save the Instagram video download guide."""
    guide_file = base_dir / "VIDEO_DOWNLOAD_GUIDE.txt"

    guide = """📥 HOW TO DOWNLOAD INSTAGRAM REFERENCE VIDEOS
===============================================================
Use this guide to download videos from your reference pages
so you can analyze them and draw inspiration for your content.
===============================================================

REFERENCE PAGES TO STUDY:
  Editing references:
    → https://www.instagram.com/keanu.visuals/
    → https://www.instagram.com/learnwithkayo/
    → https://www.instagram.com/stevenwommack/

  Video creation references:
    → https://www.instagram.com/build.withcrystal/
    → https://www.instagram.com/thepostprotocol/

===============================================================
METHOD 1: yt-dlp (Recommended — Free & Works on Windows)
===============================================================

STEP 1 — Install yt-dlp and ffmpeg:
   Open Command Prompt (Win+R → type cmd → Enter)
   Run these commands one by one:

   pip install yt-dlp
   winget install ffmpeg

STEP 2 — Download a specific video:
   yt-dlp https://www.instagram.com/p/[POST_ID]/ -o "%(uploader)s_%(id)s.%(ext)s"

   Example:
   yt-dlp https://www.instagram.com/p/CxABCDEFGHI/ -o "keanu_visuals_ref.mp4"

STEP 3 — Download multiple from a profile (most recent 10):
   yt-dlp https://www.instagram.com/keanu.visuals/ --playlist-end 10

STEP 4 — Download best quality:
   yt-dlp [URL] -f "bestvideo+bestaudio/best" --merge-output-format mp4

NOTES:
   - You must be logged in for private accounts
   - For logged-in download: yt-dlp --cookies-from-browser chrome [URL]
   - Save to a folder like: C:\\Users\\YourName\\Desktop\\Proteiner_References\\

===============================================================
METHOD 2: Online Downloaders (Quick but lower quality)
===============================================================

   1. snapinsta.app       — Paste Instagram URL, download
   2. instasave.app       — Same process
   3. igram.io            — Works for Reels specifically

   USE ONLY FOR PERSONAL REFERENCE — not for re-posting.

===============================================================
METHOD 3: Instagram Built-in (Stories & Reels Save)
===============================================================

   On iPhone/Android:
   1. Open the post you want to save
   2. Tap the bookmark icon → "Save to Collection"
   3. Create collection: "Proteiner_EditRefs"

   To screen record (when downloading isn't possible):
   iPhone: Control Center → Screen Record
   Android: Quick Settings → Screen Record
   Then trim the recording in your phone's gallery.

===============================================================
WHAT TO STUDY ONCE DOWNLOADED:
===============================================================

   For each reference video, analyze:
   ┌─ HOOK (0–3 seconds)
   │   What visual or text appears first?
   │   How long before you see the main subject?
   │
   ├─ PACING
   │   Count the cuts — how many per 15 seconds?
   │   Where are the slow moments vs fast moments?
   │
   ├─ TEXT
   │   Where does text appear on screen?
   │   What font weight / size / color?
   │   How does it animate in?
   │
   ├─ COLOR
   │   Is it warm or cool?
   │   How saturated? High contrast?
   │   What color are the shadows / highlights?
   │
   ├─ MUSIC
   │   What genre? What BPM?
   │   Does it drop at a specific moment?
   │   Is there a mood shift in the music?
   │
   └─ ENDING
       Is there a CTA? What is it?
       How does it end — hard cut or fade?

   SAVE YOUR NOTES alongside this document!

===============================================================
FOLDER STRUCTURE FOR YOUR REFERENCES:
===============================================================

   📁 Proteiner_References\\
      📁 Editing_Style\\
         📁 keanu.visuals\\
         📁 learnwithkayo\\
         📁 stevenwommack\\
      📁 Video_Creation\\
         📁 build.withcrystal\\
         📁 thepostprotocol\\
      📝 My_Analysis_Notes.txt

===============================================================
LEGAL NOTE:
===============================================================
   Downloaded videos are for personal reference and creative
   inspiration ONLY. Do not repost, share publicly, or use
   any footage in your own videos without explicit permission
   from the original creator. All rights belong to the
   respective creators.
===============================================================
"""

    guide_file.write_text(guide, encoding="utf-8")
    return guide_file


def save_brand_sheet(base_dir: Path) -> Path:
    """Save the Proteiner brand identity cheat sheet."""
    brand_file = base_dir / "PROTEINER_BRAND_SHEET.txt"

    hashtag_str = " ".join(
        BRAND["hashtags"]["core"] +
        BRAND["hashtags"]["fitness"][:5] +
        BRAND["hashtags"]["food"][:5] +
        BRAND["hashtags"]["trending_kr"]
    )

    brand_content = f"""🏋️ PROTEINER BRAND IDENTITY CHEAT SHEET
{'='*65}
Keep this open while creating any content.
{'='*65}

📌 BRAND BASICS
   Name     : Proteiner
   Handle   : @proteiner.kr
   Tagline  : 고단백 패스트푸드 (High-Protein Fast Food)
   Locations: 강남 | 신촌 | 성수

🎯 TARGET AUDIENCE
   Primary  : 헬스인 (gym-goers), 다이어터, 20–35세 한국 도시인
   Pain     : 운동 후 고단백 식사를 빠르게 챙기기 어렵다
   Desire   : 맛있고 건강한 한 끼, 빠른 단백질 보충

🗣️ BRAND VOICE
   Tone     : 에너지 넘치고 자신감 있되, 과학적 근거 기반
   Keywords : 고단백 / 맛있다 / 빠르다 / 채워라 / 프로틴 / 린바디
   CTAs     :
     • "지금 프로테이너로 채워라 💪"
     • "단백질 충전, 프로테이너에서"
     • "맛으로 채우고, 근육으로 돌아와"
     • "운동 후엔 프로테이너"

🎨 VISUAL IDENTITY
   Primary Colors:
     • #FF4D00  ← Power Orange (CTAs, highlights, brand text)
     • #1A1A1A  ← Deep Black (backgrounds, shadows)
     • #FFFFFF  ← Clean White (body text, clean UI)
   Accent Colors:
     • #FFD700  ← Gold (achievements, premium feel)
     • #2ECC71  ← Green (health/nutrition callouts)

   Font Style  : Bold sans-serif (굵고 강렬한 느낌)
   Logo Usage  : Bottom-right of video at 80% opacity
                 OR Intro/Outro card (2s black background)

📹 CONTENT PILLARS
   1. FOOD PORN         – 음식 클로즈업, 먹음직스러운 장면
   2. TRANSFORMATION    – 운동 전후, 식단 변화
   3. EDUCATION         – 단백질 팁, 영양 정보
   4. BEHIND THE SCENES – 매장 준비, 재료 이야기
   5. COMMUNITY         – 고객 반응, 리뷰, 챌린지
   6. LOCATION DROPS    – 강남/신촌/성수 매장 소개

#️⃣ MASTER HASHTAG BANK
{hashtag_str}

   ALWAYS INCLUDE: #프로테이너 #Proteiner
   LOCATION TAG: Add based on which store is featured

📊 POSTING SCHEDULE
   Monday   → Video 1 (7–9 PM KST)
   Wednesday → Video 2 (7–9 PM KST)
   Friday   → Video 3 (7–9 PM KST)

⚡ ENGAGEMENT RULES (first 60 min after posting)
   ✓ Reply to every comment
   ✓ Engage with 10–15 relevant hashtag posts
   ✓ Share to Stories immediately
   ✓ Pin a strong comment
   ✓ Check analytics at 1h / 6h / 24h

{'='*65}
"""
    brand_file.write_text(brand_content, encoding="utf-8")
    return brand_file


# ─── Main Orchestrator ────────────────────────────────────────────────────────

def main():
    print("\n" + "="*65)
    print("   🏋️  PROTEINER INSTAGRAM CONTENT GENERATOR")
    print("   @proteiner.kr — 4-Week Content Calendar")
    print("="*65)
    print()

    client = get_client()

    # Create output directory
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output folder: {OUTPUT_BASE.resolve()}\n")

    # Save static files first
    print("📝 Creating support files...")
    guide_path = save_video_download_guide(OUTPUT_BASE)
    style_path = save_style_analysis(OUTPUT_BASE)
    brand_path = save_brand_sheet(OUTPUT_BASE)
    print(f"   ✓ VIDEO_DOWNLOAD_GUIDE.txt")
    print(f"   ✓ REFERENCE_STYLE_ANALYSIS.txt")
    print(f"   ✓ PROTEINER_BRAND_SHEET.txt")
    print()

    # Generate content for all 12 videos
    all_generated = []
    total_videos = sum(len(CONTENT_THEMES[f"week_{w}"]["videos"]) for w in range(1, 5))
    video_counter = 0

    for week_num in range(1, 5):
        week_key = f"week_{week_num}"
        week_data = CONTENT_THEMES[week_key]

        print(f"{'─'*65}")
        print(f"📅 WEEK {week_num}: {week_data['theme']}")
        print(f"   Goal: {week_data['goal']}")
        print(f"{'─'*65}")

        for v_idx, video_info in enumerate(week_data["videos"], 1):
            video_counter += 1
            print(f"\n   📹 Video {v_idx} — {video_info['day']}  [{video_counter}/{total_videos}]")
            print(f"      Type: {video_info['type']}")
            print(f"      Hook: {video_info['hook']}")

            try:
                content = generate_video_content(client, week_num, v_idx, video_info)
                video_dir = save_video_content(
                    OUTPUT_BASE, week_num, v_idx, video_info["day"], content
                )
                print(f"      ✅ Saved to: {video_dir.relative_to(OUTPUT_BASE)}")
                all_generated.append(content)

            except anthropic.RateLimitError:
                print(f"      ⚠️  Rate limited. Waiting 60s...")
                time.sleep(60)
                # Retry once
                content = generate_video_content(client, week_num, v_idx, video_info)
                video_dir = save_video_content(
                    OUTPUT_BASE, week_num, v_idx, video_info["day"], content
                )
                all_generated.append(content)

            except anthropic.APIError as e:
                print(f"      ❌ API Error: {e}. Skipping this video.")
                continue

        print()

    # Save calendar overview
    print("📅 Generating calendar overview...")
    overview_path = save_calendar_overview(OUTPUT_BASE, all_generated)
    print(f"   ✓ CONTENT_CALENDAR_OVERVIEW.txt\n")

    # Final summary
    print("="*65)
    print("✅  GENERATION COMPLETE!")
    print("="*65)
    print(f"\n📁 Everything saved to:")
    print(f"   {OUTPUT_BASE.resolve()}\n")
    print("📊 Summary:")
    print(f"   • {total_videos} videos generated")
    print(f"   • {total_videos} Korean captions")
    print(f"   • {total_videos} Higgsfield AI prompts")
    print(f"   • {total_videos} CapCut editing guides")
    print()
    print("📁 Folder structure:")
    for week_num in range(1, 5):
        print(f"   Week_{week_num}/")
        week_data = CONTENT_THEMES[f"week_{week_num}"]
        for v_idx, video in enumerate(week_data["videos"], 1):
            day_kr = video["day"].split(" ")[0]
            print(f"      Video_{v_idx}_{day_kr}/")
            print(f"         caption_KO.txt")
            print(f"         higgsfield_ai_prompt.txt")
            print(f"         capcut_editing_instructions.txt")
            print(f"         QUICK_REFERENCE.txt")
    print()
    print("🚀 NEXT STEPS:")
    print("   1. Open CONTENT_CALENDAR_OVERVIEW.txt for the full schedule")
    print("   2. Read VIDEO_DOWNLOAD_GUIDE.txt to study reference pages")
    print("   3. Start with Week_1/Video_1 — film this week!")
    print("   4. Use QUICK_REFERENCE.txt in each folder as your on-set guide")
    print()
    print("   화이팅! 💪 @proteiner.kr\n")


if __name__ == "__main__":
    main()
