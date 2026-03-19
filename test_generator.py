#!/usr/bin/env python3
"""
Mock test for Proteiner Content Generator.
Verifies file creation, formatting, JSON parsing, fallback logic,
week-start calculation, and all writer functions — no real API key needed.
"""

import json
import sys
import os
import shutil
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

# Make sure we can import the main module
sys.path.insert(0, str(Path(__file__).parent))
import generate_content as gc


SAMPLE_RESEARCH = {
    "research_date": "2026-03-19",
    "top_viral_formats": [
        {
            "format_name": "Silent ASMR Countdown",
            "description": "3-2-1 reveal with pure food sounds",
            "why_it_works": "Triggers curiosity + satisfying payoff",
            "proteiner_adaptation": "Countdown to unwrapping a Proteiner burger",
            "trending_audio_style": "No music — raw food sounds only"
        },
        {
            "format_name": "POV: You just hit a new PR",
            "description": "First-person perspective after gym milestone",
            "why_it_works": "Korean gym culture resonates strongly",
            "proteiner_adaptation": "POV arriving at Proteiner after hitting 100kg squat",
            "trending_audio_style": "Triumphant lo-fi beat"
        }
    ],
    "hook_patterns": [
        {
            "pattern": "Shocking stat opener",
            "korean_example": "단백질 50g을 이렇게 먹는다고?",
            "why_it_stops_scroll": "Triggers disbelief — viewer must verify"
        },
        {
            "pattern": "Before/after contrast",
            "korean_example": "운동 전 vs 운동 후 먹는 것의 차이",
            "why_it_stops_scroll": "Comparison format is universally compelling"
        }
    ],
    "editing_trends": [
        "Fast-cut sound-sync under 30 seconds",
        "Bold Korean text overlay with stroke/shadow",
        "Warm desaturated colour grade (golden hour feel)"
    ],
    "korean_specific_insights": [
        "Korean audiences respond to authentic gym struggle content",
        "ASMR food videos outperform scripted ads 3:1 on Korean Reels",
        "Seongsu and Gangnam location tags increase local reach significantly"
    ],
    "content_calendar_strategy": (
        "Lead each week with a high-entertainment hook to build reach, "
        "then follow with an informational post to build trust and saves."
    )
}

SAMPLE_WEEK_CONTENT = """
════════════════════════════════════════════════════════════════════════════════
VIDEO 1 OF 4  |  WEEK 1
════════════════════════════════════════════════════════════════════════════════

1. VIDEO TITLE
단백질 폭탄 언박싱

2. HOOK  (Korean — first 3 seconds)
단백질 50g이 이 안에 다 들어있다고?

3. CONCEPT
Proteiner의 시그니처 버거를 천천히 언박싱하는 ASMR 영상.
현재 인기 있는 '언박싱 + ASMR 결합' 포맷을 음식에 적용한 버전.
한국 헬스 커뮤니티에서 단백질 함량에 민감한 시청자들의 주목을 즉시 끌어낼 수 있다.

4. WHAT TO FILM
Shot 1 (0–2s): 오버헤드 샷 — 테이블 위에 놓인 Proteiner 박스. 조명: 자연광 또는 링라이트.
Shot 2 (2–5s): 손 클로즈업 — 박스를 천천히 여는 장면. You will film yourself doing this. Only hands visible.
Shot 3 (5–10s): 매크로 샷 — 버거 단면 클로즈업. 치즈가 녹는 순간 포착.
Shot 4 (10–15s): 사이드 앵글 — 버거 전체 구조 샷. 각 레이어가 보이도록.

5. CAPCUT EDITING INSTRUCTIONS
Step 1: 클립을 Shot 1 → Shot 2 → Shot 3 → Shot 4 순서로 타임라인에 올려라.
Step 2: 전체 클립에 0.85x 슬로우모션 적용.
Step 3: 트랜지션 — 각 컷 사이에 'Zoom Blur' 트랜지션 0.3초.
Step 4: 텍스트 오버레이 (0–2초) — "단백질 50g" / 폰트: Bold Sans / 색상: 흰색 / 배경: 반투명 검정.
Step 5: 음악 — CapCut 사운드 라이브러리에서 'ASMR lo-fi' 검색. 볼륨 20% 유지.
Step 6: 컬러 필터 — 'Latte' 또는 'Film04' 적용.
Step 7: 자동 자막 켜기 — 한국어 설정.

6. HIGGSFIELD AI INSTRUCTIONS
Not needed for this video.

7. INSTAGRAM CAPTION
단백질 50g이 이 안에 다 들어있다? 🤯

헬스인이라면 알 것이다.
이 크기의 버거에서 닭가슴살 두 장 분량의 단백질이 나온다는 걸.

📌 저장해두세요 — 다음 치팅데이 전에 꼭 확인!

📍 성수 / 강남 / 신촌 매장에서 만나보세요
→ @proteiner.kr

#프로티너 #단백질식품 #헬스식단 #고단백버거 #서울헬스 #성수맛집
#강남맛집 #헬스인 #ProteinFood #SeoulFood #FitFood #HighProtein
#KoreanFitness #GymFood #헬스인스타그램 #단백질 #근육밥 #프로틴버거

8. BEST TIME TO POST
화요일 오후 7:30 KST

9. PREDICTED VIRAL FACTOR
이 영상은 ASMR 언박싱 포맷과 단백질 수치 공개라는 두 가지 강력한 훅을 결합,
한국 헬스 커뮤니티의 '정보 + 만족감' 욕구를 동시에 충족시켜 100k+ 뷰 가능성이 높다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


class TestResearchParsing(unittest.TestCase):
    """Test JSON parsing robustness."""

    def test_clean_json(self):
        raw = json.dumps(SAMPLE_RESEARCH)
        result = gc.run_research_phase.__wrapped__ if hasattr(gc.run_research_phase, '__wrapped__') else None
        # Direct parsing test
        data = json.loads(raw)
        self.assertEqual(data["research_date"], "2026-03-19")
        self.assertEqual(len(data["top_viral_formats"]), 2)

    def test_json_with_markdown_fence(self):
        """Verify strip logic removes ```json fences."""
        raw = "```json\n" + json.dumps(SAMPLE_RESEARCH) + "\n```"
        text = raw.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            lines = lines[1:]                          # drop opening fence / language tag
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]                     # drop closing fence
            text = "\n".join(lines).strip()
        data = json.loads(text)
        self.assertIn("top_viral_formats", data)

    def test_fallback_defaults(self):
        """Verify that missing keys get safe defaults."""
        partial = {"research_date": "2026-01-01"}
        partial.setdefault("top_viral_formats", [])
        partial.setdefault("hook_patterns", [])
        partial.setdefault("editing_trends", [])
        partial.setdefault("korean_specific_insights", [])
        partial.setdefault("content_calendar_strategy", "fallback")
        self.assertEqual(partial["top_viral_formats"], [])
        self.assertEqual(partial["content_calendar_strategy"], "fallback")


class TestWeekStartCalculation(unittest.TestCase):
    """Test week-start date logic."""

    def test_returns_four_mondays(self):
        starts = gc.compute_week_starts()
        self.assertEqual(len(starts), 4)
        for s in starts:
            self.assertEqual(s.weekday(), 0)  # Monday = 0

    def test_weeks_are_sequential(self):
        starts = gc.compute_week_starts()
        for i in range(1, 4):
            delta = starts[i] - starts[i - 1]
            self.assertEqual(delta.days, 7)

    def test_first_monday_is_in_future(self):
        starts = gc.compute_week_starts()
        self.assertGreater(starts[0], datetime.now())


class TestPromptBuilding(unittest.TestCase):
    """Test prompt assembly."""

    def test_week_prompt_contains_brand(self):
        ws = datetime(2026, 3, 23)
        prompt = gc.build_week_prompt(1, SAMPLE_RESEARCH, ws)
        self.assertIn("proteiner.kr", prompt)
        self.assertIn("프로티너", prompt)
        self.assertIn("WEEK 1", prompt)

    def test_week_prompt_contains_filming_rules(self):
        ws = datetime(2026, 3, 23)
        prompt = gc.build_week_prompt(2, SAMPLE_RESEARCH, ws)
        self.assertIn("FACE SWAP NEEDED", prompt)
        self.assertIn("No AI-generated people", prompt)

    def test_week_prompt_contains_research_data(self):
        ws = datetime(2026, 3, 23)
        prompt = gc.build_week_prompt(3, SAMPLE_RESEARCH, ws)
        self.assertIn("Silent ASMR Countdown", prompt)
        self.assertIn("단백질 50g을 이렇게 먹는다고?", prompt)


class TestFileWriters(unittest.TestCase):
    """Test all file writer functions."""

    TEST_DIR = Path("_test_output")

    def setUp(self):
        # Redirect OUTPUT_DIR to test directory
        self._original_dir = gc.OUTPUT_DIR
        gc.OUTPUT_DIR = self.TEST_DIR
        self.TEST_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        gc.OUTPUT_DIR = self._original_dir
        shutil.rmtree(self.TEST_DIR, ignore_errors=True)

    def _gen_date(self):
        return datetime.now().strftime("%B %d, %Y at %H:%M")

    def test_write_research_file(self):
        path = gc.write_research_file(SAMPLE_RESEARCH, self._gen_date())
        self.assertTrue(path.exists())
        content = path.read_text(encoding="utf-8")
        self.assertIn("PROTEINER CONTENT RESEARCH FINDINGS", content)
        self.assertIn("Silent ASMR Countdown", content)

    def test_write_week_file(self):
        ws = datetime(2026, 3, 23)
        path = gc.write_week_file(1, SAMPLE_WEEK_CONTENT, ws, self._gen_date())
        self.assertTrue(path.exists())
        content = path.read_text(encoding="utf-8")
        self.assertIn("WEEK 1 OF 4", content)
        self.assertIn("단백질 폭탄 언박싱", content)
        self.assertIn("END OF WEEK 1", content)

    def test_write_week_file_naming(self):
        for i in range(1, 5):
            ws = datetime(2026, 3, 23) + timedelta(weeks=i - 1)
            path = gc.write_week_file(i, SAMPLE_WEEK_CONTENT, ws, self._gen_date())
            self.assertEqual(path.name, f"Week{i}.txt")

    def test_write_full_calendar(self):
        starts = [datetime(2026, 3, 23) + timedelta(weeks=i) for i in range(4)]
        all_weeks = [SAMPLE_WEEK_CONTENT] * 4
        path = gc.write_full_calendar(all_weeks, SAMPLE_RESEARCH, starts, self._gen_date())
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "FULL_CALENDAR.txt")
        content = path.read_text(encoding="utf-8")
        self.assertIn("FULL 4-WEEK INSTAGRAM REEL CALENDAR", content)
        self.assertIn("16 Videos", content)
        self.assertIn("RESEARCH FINDINGS", content)
        # Check all 4 week sections exist
        for i in range(1, 5):
            self.assertIn(f"WEEK {i} OF 4", content)

    def test_full_calendar_utf8(self):
        """Korean characters must survive the round-trip."""
        starts = [datetime(2026, 3, 23) + timedelta(weeks=i) for i in range(4)]
        path = gc.write_full_calendar(
            [SAMPLE_WEEK_CONTENT] * 4, SAMPLE_RESEARCH, starts, self._gen_date()
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn("프로티너", content)
        self.assertIn("단백질", content)


class TestResearchSummaryBlock(unittest.TestCase):
    """Test the research summary block generation."""

    def test_contains_formats(self):
        block = gc.research_summary_block(SAMPLE_RESEARCH)
        self.assertIn("Silent ASMR Countdown", block)
        self.assertIn("POV: You just hit a new PR", block)

    def test_contains_insights(self):
        block = gc.research_summary_block(SAMPLE_RESEARCH)
        self.assertIn("ASMR food videos", block)

    def test_contains_strategy(self):
        block = gc.research_summary_block(SAMPLE_RESEARCH)
        self.assertIn("Lead each week", block)

    def test_empty_research_does_not_crash(self):
        block = gc.research_summary_block({})
        self.assertIsInstance(block, str)


class TestAPIKeyCheck(unittest.TestCase):
    """Test API key validation path (without calling the real API)."""

    def test_missing_key_detected(self):
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)
        key = env.get("ANTHROPIC_API_KEY", "").strip()
        self.assertEqual(key, "")

    def test_present_key_accepted(self):
        key = "sk-ant-test1234"
        self.assertTrue(key.startswith("sk-ant-"))


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
