"""
Proteiner Brand Identity
========================
Core brand constants used throughout content generation.
"""

BRAND = {
    "name": "Proteiner",
    "handle": "@proteiner.kr",
    "tagline": "고단백 패스트푸드 (High-Protein Fast Food)",
    "language": "Korean (caption) + English (hooks/text overlays)",

    "locations": [
        "강남 (Gangnam)",
        "신촌 (Sinchon)",
        "성수 (Seongsu)",
    ],

    "audience": {
        "primary": "헬스인 (gym-goers), 다이어터, 20–35세 한국 도시인",
        "secondary": "건강한 식사를 원하는 바쁜 직장인",
        "pain_points": [
            "운동 후 고단백 식사를 빠르게 챙기기 어렵다",
            "맛있으면서 건강한 음식을 찾기 힘들다",
            "식단 관리와 맛 사이에서 타협해야 한다",
        ],
        "desires": [
            "맛있고 건강한 한 끼",
            "운동 후 빠른 단백질 보충",
            "식단 관리를 포기하지 않아도 되는 선택지",
        ],
    },

    "menu_pillars": [
        "고단백 버거",
        "닭가슴살 메뉴",
        "프로틴 볼 & 샐러드",
        "단백질 음료",
        "벌크업 세트",
    ],

    "brand_voice": {
        "tone": "에너지 넘치고 자신감 있되, 과학적 근거 기반. 친근하지만 전문적.",
        "keywords": ["고단백", "맛있다", "빠르다", "채워라", "프로틴", "린바디", "벌크", "클린"],
        "cta_phrases": [
            "지금 프로테이너로 채워라 💪",
            "단백질 충전, 프로테이너에서",
            "맛으로 채우고, 근육으로 돌아와",
            "운동 후엔 프로테이너",
        ],
    },

    "visual_identity": {
        "primary_colors": ["#FF4D00 (파워 오렌지)", "#1A1A1A (딥 블랙)", "#FFFFFF (클린 화이트)"],
        "accent_colors": ["#FFD700 (골드 하이라이트)", "#2ECC71 (그린 – 건강 강조)"],
        "font_style": "Bold sans-serif (굵고 강렬한 느낌), 한글+영문 혼용",
        "logo_usage": "로고는 항상 영상 우하단 or 인트로/아웃트로에 삽입",
    },

    "content_pillars": [
        "FOOD PORN – 음식 클로즈업, 먹음직스러운 장면",
        "TRANSFORMATION – 운동 전후, 식단 변화",
        "EDUCATION – 단백질 팁, 영양 정보",
        "BEHIND THE SCENES – 매장 준비, 재료 이야기",
        "COMMUNITY – 고객 반응, 리뷰, 챌린지",
        "LOCATION DROPS – 강남/신촌/성수 매장 소개",
    ],

    "hashtags": {
        "core": ["#프로테이너", "#Proteiner", "#고단백패스트푸드", "#단백질밥집"],
        "fitness": ["#헬스", "#운동", "#프로틴", "#헬스인", "#다이어트", "#린바디", "#벌크업", "#헬창"],
        "food": ["#맛집", "#강남맛집", "#신촌맛집", "#성수맛집", "#건강식", "#고단백", "#먹스타그램"],
        "lifestyle": ["#운동후식사", "#식단관리", "#단백질충전", "#헬시푸드", "#클린이팅"],
        "trending_kr": ["#오운완", "#헬스타그램", "#바디프로필", "#몸만들기"],
    },
}


CONTENT_THEMES = {
    "week_1": {
        "theme": "브랜드 소개 & 첫인상 (Brand Intro & First Impression)",
        "goal": "신규 팔로워 유입, 브랜드 각인",
        "videos": [
            {
                "day": "월요일 (Monday)",
                "type": "훅 영상 – '운동 후 뭐 먹어?' 문제 제기",
                "pillar": "EDUCATION + FOOD PORN",
                "hook": "운동 다 했는데 먹을 게 없다? (You just finished your workout... now what?)",
            },
            {
                "day": "수요일 (Wednesday)",
                "type": "메뉴 쇼케이스 – 버거 클로즈업 시네마틱",
                "pillar": "FOOD PORN",
                "hook": "이게 다이어트 음식이라고? (This is diet food?!)",
            },
            {
                "day": "금요일 (Friday)",
                "type": "매장 비하인드 – 성수점 오픈 비하인드씬",
                "pillar": "BEHIND THE SCENES + LOCATION",
                "hook": "성수에 뭔가 생겼다 👀",
            },
        ],
    },
    "week_2": {
        "theme": "단백질 교육 & 신뢰 구축 (Protein Education & Trust Building)",
        "goal": "전문성 강조, 팔로워 충성도 높이기",
        "videos": [
            {
                "day": "월요일 (Monday)",
                "type": "인포그래픽 영상 – 하루 단백질 목표량",
                "pillar": "EDUCATION",
                "hook": "하루에 단백질 몇 g 먹어야 해? (How much protein do you actually need per day?)",
            },
            {
                "day": "수요일 (Wednesday)",
                "type": "고객 리뷰 + 음식 반응",
                "pillar": "COMMUNITY",
                "hook": "강남 헬창들이 줄 서는 이유 💪",
            },
            {
                "day": "금요일 (Friday)",
                "type": "메뉴 비교 – 프로테이너 vs 일반 패스트푸드",
                "pillar": "EDUCATION + FOOD PORN",
                "hook": "같은 칼로리, 단백질은 3배",
            },
        ],
    },
    "week_3": {
        "theme": "라이프스타일 통합 (Lifestyle Integration)",
        "goal": "브랜드를 운동 루틴의 일부로 포지셔닝",
        "videos": [
            {
                "day": "월요일 (Monday)",
                "type": "하루 루틴 영상 – 운동 → 프로테이너 → 일상",
                "pillar": "TRANSFORMATION + LIFESTYLE",
                "hook": "오운완 후 필수 코스 🔥",
            },
            {
                "day": "수요일 (Wednesday)",
                "type": "신촌점 소개 + 대학생 타겟",
                "pillar": "LOCATION + COMMUNITY",
                "hook": "신촌 대학생들 다 어디 가? (Sinchon students, where are you eating?)",
            },
            {
                "day": "금요일 (Friday)",
                "type": "세트 메뉴 스타일링 영상 (고급 푸드 영상)",
                "pillar": "FOOD PORN",
                "hook": "이 조합 실화냐 (This combo is actually insane)",
            },
        ],
    },
    "week_4": {
        "theme": "커뮤니티 & 행동 유도 (Community & CTA)",
        "goal": "직접 방문 유도, 챌린지 런칭",
        "videos": [
            {
                "day": "월요일 (Monday)",
                "type": "챌린지 런칭 – '30일 프로틴 챌린지'",
                "pillar": "COMMUNITY",
                "hook": "30일 동안 단백질 목표 달성하면? 🎁",
            },
            {
                "day": "수요일 (Wednesday)",
                "type": "강남점 러시아워 비하인드씬",
                "pillar": "BEHIND THE SCENES",
                "hook": "점심시간 강남점 현실 (Gangnam store at lunch rush — real footage)",
            },
            {
                "day": "금요일 (Friday)",
                "type": "월간 마무리 – 브랜드 스토리 감성 영상",
                "pillar": "TRANSFORMATION + BRAND",
                "hook": "프로테이너가 만들어진 이유 (Why Proteiner exists)",
            },
        ],
    },
}
