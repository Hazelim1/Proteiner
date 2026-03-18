"""
Reference Style Analysis
========================
Pre-analyzed editing and content creation styles from reference Instagram pages.
Used as creative direction input for content generation.
"""

EDIT_REFERENCES = {
    "keanu.visuals": {
        "handle": "@keanu.visuals",
        "style_category": "Cinematic / Dark Aesthetic",
        "analysis": {
            "hook_structure": (
                "Starts with a slow, moody establishing shot (0–1s). "
                "First text appears at 1.5s as a white bold caption. "
                "Quick cut to food close-up at 2s to spike visual interest."
            ),
            "editing_style": (
                "Heavy use of J-cuts and L-cuts. "
                "Slow-motion on food drops (0.3x speed). "
                "Color grade: deep shadows, warm highlights, crushed blacks. "
                "Transitions: whip pan, flash cut, zoom-in punch."
            ),
            "text_placement": (
                "Large white bold text centered OR bottom-third. "
                "Minimal text — 3–5 words max per frame. "
                "Fade-in text with slight blur effect."
            ),
            "pacing": (
                "0–3s: Hook (slow, atmospheric). "
                "3–10s: Content reveal (medium pace cuts every 1.5s). "
                "10–15s: Money shot + CTA (1–2 slow cuts)."
            ),
            "color_tone": "Desaturated with orange/amber push. Dark and premium.",
            "music_energy": "Lo-fi hip hop or dark trap. 80–100 BPM. Drops synced to visual cuts.",
            "apply_to_proteiner": (
                "Use for premium food close-up videos. "
                "Dark background, moody lighting on the burger/protein bowl. "
                "Match music drop to the first food reveal shot."
            ),
        },
    },

    "learnwithkayo": {
        "handle": "@learnwithkayo",
        "style_category": "Educational / Dynamic Text-Heavy",
        "analysis": {
            "hook_structure": (
                "Starts with a question or bold stat in text at 0s (before any visual). "
                "Creator appears on screen at 1s to validate the claim. "
                "Fast cut to supporting visual at 2s."
            ),
            "editing_style": (
                "Rapid cuts every 0.8–1.2s. "
                "Jump cuts within single clip (removes pauses). "
                "Text animations: pop-in, typewriter, emoji emphasis. "
                "B-roll cutaways timed to key words."
            ),
            "text_placement": (
                "Top third for the 'question hook'. "
                "Middle screen for data/stats in large bold. "
                "Bottom third for CTAs."
            ),
            "pacing": (
                "0–2s: Bold question/fact on screen. "
                "2–8s: Fast educational breakdown. "
                "8–12s: Actionable tip or punchline. "
                "12–15s: CTA (follow for more / save this)."
            ),
            "color_tone": "Bright, clean whites. Accent color text (yellow, orange). High contrast.",
            "music_energy": "Upbeat pop or phonk. 120–140 BPM. Energetic throughout.",
            "apply_to_proteiner": (
                "Use for protein education content (how much protein, macros, etc.). "
                "Start with a stat: '단백질 얼마나 먹어야 해?' as opening text. "
                "Fast cuts between infographic-style text cards and food shots."
            ),
        },
    },

    "stevenwommack": {
        "handle": "@stevenwommack",
        "style_category": "Fitness Lifestyle / Aspirational",
        "analysis": {
            "hook_structure": (
                "Opens mid-action (gym, running, eating) — no intro. "
                "Text hook appears within 0.5s: relatable pain point or bold claim. "
                "Immediate cut to 'the solution' at 2s."
            ),
            "editing_style": (
                "Handheld, slightly shaky cam for authenticity. "
                "Color grade: warm, golden hour tones, high saturation. "
                "Slow-motion on key moments (lifting, first bite). "
                "Transitions: match cuts, hard cuts, occasional glitch."
            ),
            "text_placement": (
                "All-caps bold text overlaid at center or lower third. "
                "Short punchy phrases (4–6 words). "
                "Occasional text with shadow/stroke for readability."
            ),
            "pacing": (
                "0–2s: Action hook. "
                "2–7s: Problem amplification. "
                "7–12s: Solution reveal (the food/brand). "
                "12–15s: Transformation or result + CTA."
            ),
            "color_tone": "Warm golden tones. High vibrancy. Skin tones look glowing.",
            "music_energy": "Motivational hip hop or hype trap. 110–130 BPM. Drop at solution reveal.",
            "apply_to_proteiner": (
                "Perfect for 'ounde-wan' (오운완) lifestyle content. "
                "Show real gym footage → cut to Proteiner meal. "
                "Make it feel like a natural next step in someone's fitness day."
            ),
        },
    },
}


VIDEO_CREATION_REFERENCES = {
    "build.withcrystal": {
        "handle": "@build.withcrystal",
        "style_category": "Motivational Brand Building / Personal Brand",
        "analysis": {
            "content_structure": (
                "Every video has 3 acts: Problem → Framework → Transformation. "
                "Opens with relatable frustration. "
                "Delivers a clean, actionable insight in the middle. "
                "Ends with inspiring outcome or direct CTA."
            ),
            "storytelling": (
                "Uses personal narrative to build trust. "
                "Addresses viewer directly ('you' language). "
                "Shows vulnerability before showing success."
            ),
            "visual_approach": (
                "Talking head + B-roll intercutting. "
                "Whiteboard/text animation for frameworks. "
                "Real behind-the-scenes footage to build authenticity."
            ),
            "apply_to_proteiner": (
                "Use the 3-act structure for brand story content: "
                "'Post-workout, you're starving but everything is unhealthy → "
                "We built Proteiner to fix that → Here's what a meal looks like.'"
            ),
        },
    },

    "thepostprotocol": {
        "handle": "@thepostprotocol",
        "style_category": "Social Media Strategy / High-Performance Content",
        "analysis": {
            "content_structure": (
                "Every video optimizes for the 3-second hold AND the 15-second watch time. "
                "Hook is engineered: visual interrupt + text pattern interrupt simultaneously. "
                "Middle 60% is dense value delivery. "
                "End cap always directs to action."
            ),
            "video_types": [
                "POV-style (immersive, first-person experience)",
                "Side-by-side comparison (before/after or this vs that)",
                "Listicle reveal (3 reasons, 5 things, etc.)",
                "Reaction/response to trending content",
            ],
            "retention_tactics": (
                "Open loops ('I'll show you X... but first'). "
                "Text teasers at top: 'wait for it'. "
                "Zoom in at 7–8s mark to re-engage droppers. "
                "Music energy shift at midpoint."
            ),
            "apply_to_proteiner": (
                "Apply open-loop hooks: '강남에서 이거 먹고 5kg 뺐다... 근데 이게 뭔지 알아?' "
                "Use comparison format: 일반 버거 칼로리 vs 프로테이너 칼로리/단백질. "
                "Engineer every 7s to have a re-engagement moment (zoom, text pop, music shift)."
            ),
        },
    },
}


def get_style_brief_for_video(video_type: str) -> dict:
    """
    Returns the most relevant style combination for a given video type.
    Maps Proteiner content types to reference creator styles.
    """
    style_map = {
        "FOOD PORN": {
            "primary_edit_ref": "keanu.visuals",
            "secondary_edit_ref": "stevenwommack",
            "creation_ref": "thepostprotocol",
            "brief": "Dark, cinematic close-ups. Slow-motion food drops. Music drop on reveal.",
        },
        "EDUCATION": {
            "primary_edit_ref": "learnwithkayo",
            "secondary_edit_ref": "thepostprotocol",
            "creation_ref": "build.withcrystal",
            "brief": "Bold question hook. Fast educational cuts. Infographic-style text cards.",
        },
        "TRANSFORMATION": {
            "primary_edit_ref": "stevenwommack",
            "secondary_edit_ref": "keanu.visuals",
            "creation_ref": "build.withcrystal",
            "brief": "Gym footage → food reveal. Warm golden tones. Aspirational narrative arc.",
        },
        "BEHIND THE SCENES": {
            "primary_edit_ref": "stevenwommack",
            "secondary_edit_ref": "learnwithkayo",
            "creation_ref": "thepostprotocol",
            "brief": "Handheld authenticity. Fast cuts. POV-style immersion.",
        },
        "COMMUNITY": {
            "primary_edit_ref": "learnwithkayo",
            "secondary_edit_ref": "stevenwommack",
            "creation_ref": "thepostprotocol",
            "brief": "Reaction-style. User content integration. High energy + relatable pain points.",
        },
        "LOCATION": {
            "primary_edit_ref": "keanu.visuals",
            "secondary_edit_ref": "stevenwommack",
            "creation_ref": "build.withcrystal",
            "brief": "Cinematic location establishing shots. Map/text graphics. Lifestyle integration.",
        },
    }

    for key in style_map:
        if key.upper() in video_type.upper():
            return style_map[key]

    # Default
    return style_map["FOOD PORN"]
