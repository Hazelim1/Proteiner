# 🏋️ Proteiner Instagram Content Generator

**Automated content generation system for @proteiner.kr**
High-protein fast food brand · Seoul, South Korea · 강남 | 신촌 | 성수

---

## What This System Does

Generates a complete **4-week Instagram content calendar** (12 videos) with:

| Output | Description |
|--------|-------------|
| 📝 Korean Caption | Ready-to-post caption with hashtags in 한국어 |
| 🎨 Higgsfield AI Prompt | Image/video generation prompt for AI visuals |
| 🎬 CapCut Instructions | Step-by-step editing guide referencing your style pages |

Every piece of content is tailored to Proteiner's brand identity and draws from the editing/creation styles of:

**Editing References:**
- [@keanu.visuals](https://instagram.com/keanu.visuals) — Cinematic dark aesthetic
- [@learnwithkayo](https://instagram.com/learnwithkayo) — Educational text-heavy
- [@stevenwommack](https://instagram.com/stevenwommack) — Fitness lifestyle

**Video Creation References:**
- [@build.withcrystal](https://instagram.com/build.withcrystal) — 3-act storytelling
- [@thepostprotocol](https://instagram.com/thepostprotocol) — Performance-engineered content

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

Or create a `.env` file in this folder:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Run the generator

```bash
python proteiner_generator.py
```

Generation takes approximately **10–15 minutes** for all 12 videos (3 API calls per video × 12 videos = 36 calls).

---

## Output Structure

After running, a `Proteiner_Content_Calendar/` folder is created:

```
Proteiner_Content_Calendar/
│
├── CONTENT_CALENDAR_OVERVIEW.txt    ← Start here! Full 4-week schedule
├── PROTEINER_BRAND_SHEET.txt        ← Brand identity cheat sheet
├── REFERENCE_STYLE_ANALYSIS.txt     ← How to apply reference page styles
├── VIDEO_DOWNLOAD_GUIDE.txt         ← How to download reference videos
│
├── Week_1/
│   ├── Video_1_월요일/
│   │   ├── QUICK_REFERENCE.txt          ← Read this on set
│   │   ├── caption_KO.txt               ← Copy-paste Instagram caption
│   │   ├── higgsfield_ai_prompt.txt     ← Use on higgsfield.ai
│   │   └── capcut_editing_instructions.txt  ← CapCut guide
│   ├── Video_2_수요일/
│   └── Video_3_금요일/
│
├── Week_2/  [same structure]
├── Week_3/  [same structure]
└── Week_4/  [same structure]
```

---

## 4-Week Content Themes

| Week | Theme | Goal |
|------|-------|------|
| 1 | 브랜드 소개 & 첫인상 | New follower acquisition, brand recognition |
| 2 | 단백질 교육 & 신뢰 구축 | Establish expertise, build loyalty |
| 3 | 라이프스타일 통합 | Position Proteiner as part of fitness routine |
| 4 | 커뮤니티 & 행동 유도 | Drive store visits, launch challenge |

**Posting schedule:** Monday / Wednesday / Friday at **7–9 PM KST**

---

## Workflow Per Video

1. **Open** `QUICK_REFERENCE.txt` in the video folder
2. **Film** the shots listed in `capcut_editing_instructions.txt`
3. **Generate visuals** using `higgsfield_ai_prompt.txt` on [higgsfield.ai](https://higgsfield.ai)
4. **Edit** in CapCut following the step-by-step instructions
5. **Copy** the caption from `caption_KO.txt`
6. **Post** and engage for the first 60 minutes

---

## Files in This Repo

| File | Description |
|------|-------------|
| `proteiner_generator.py` | Main script — run this |
| `brand_identity.py` | Brand constants, themes, content pillars |
| `reference_styles.py` | Style analysis of all 5 reference pages |
| `requirements.txt` | Python dependencies |

---

## Studying Your Reference Pages

Read `VIDEO_DOWNLOAD_GUIDE.txt` for:
- How to download Instagram videos using **yt-dlp** (free, Windows)
- Online downloader alternatives
- What to analyze in each reference video
- How to organize your reference folder

---

## Getting an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an account or sign in
3. Navigate to **API Keys** → **Create Key**
4. Copy the key and set it as `ANTHROPIC_API_KEY`

**Cost estimate:** Running the full generator uses approximately 100K–150K tokens.
At Claude Opus 4.6 pricing ($5/1M input, $25/1M output), this costs roughly **$3–5 per full run**.

---

## Troubleshooting

**`ANTHROPIC_API_KEY not found`**
→ Make sure you set the environment variable before running the script

**Rate limit errors**
→ The script automatically retries with a 60-second wait. If it keeps failing, wait a few minutes and restart.

**Garbled Korean text on Windows**
→ Open the `.txt` files with Notepad++, VS Code, or set your system to UTF-8:
`Settings → Time & Language → Language → Administrative language settings → Change system locale → Beta: UTF-8`

---

*화이팅! 💪 @proteiner.kr*
