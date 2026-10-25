#!/usr/bin/env python3
"""
PROJECT: THE EYE WITHIN WORDS — Python Generative Typography Animation
======================================================================
A full-screen generative typography artwork for macOS in which 100% of the screen
is filled edge-to-edge with readable meaningful words, quotes, and poetic sentences
that collectively form the illusion of ONE enormous, living, blinking human eye,
accompanied by a continuous cinematic camera zoom between wide and close-up views.

Controls:
  SPACE : Trigger an immediate blink
  B     : Enable or disable automatic blinking
  Z     : Toggle automatic camera zooming
  C     : Change the color palette
  R     : Regenerate a new arrangement of meaningful quotes
  H     : Show or hide keyboard instructions
  ESC   : Close the animation safely
  Mouse : Subtly influences the gaze and camera focus
"""

import argparse
import math
import os
import random
import sys
import time
import warnings
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Suppress Pygame greeting banner and benign Python 3.12/3.14 pygame.threads warning
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*threads.*")

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pygame


# ============================================================================
# 1. GENERATING MEANINGFUL QUOTES & POETIC VOCABULARY
# ============================================================================

SIGNATURE_QUOTES = [
    "we are made of stars",
    "look beyond what you see",
    "every thought leaves a trace",
    "the universe lives within us",
    "beauty exists in the details",
    "we become what we believe",
    "silence has its own language",
    "nothing is ever truly invisible",
    "your perception creates your world",
    "the truth hides between the lines",
    "every ending begins somewhere",
    "consciousness observing itself",
    "there is more than meets the eye",
    "even darkness carries meaning",
    "wonder is a form of intelligence",
    "the world is written in patterns",
    "what you seek is seeking you",
    "everything is connected",
    "look closer",
    "stay curious",
]

ADDITIONAL_POETIC_QUOTES = [
    "light remembers where it has been",
    "every question opens an unseen door",
    "we are the universe becoming aware",
    "in stillness the hidden becomes clear",
    "meaning blooms where attention rests",
    "time is a river of quiet revelations",
    "beneath every surface lies another sky",
    "words are the architecture of thought",
    "to truly see is to be transformed",
    "infinite worlds inside a single glance",
    "memory is starlight traveling through mind",
    "the observer and the observed are one",
    "clarity arrives when the mind grows quiet",
    "every heartbeat echoes across eternity",
    "dreams are letters from the unseen self",
    "curiosity is the compass of the soul",
    "shadows only prove the presence of light",
    "vision begins where certainty ends",
    "all things are woven from the same light",
    "listen to the quiet between your thoughts",
    "awareness is the canvas of existence",
    "every moment contains the whole of time",
    "the eye reads what the heart remembers",
    "patterns of light become living thought",
    "seek the poetry hidden in plain sight",
    "nothing seen is ever separate from you",
    "thought is the brushstroke of reality",
    "within the finite dwells the infinite",
    "each breath is a quiet beginning",
    "truth shines brightest in the dark",
]

MEANINGFUL_SHORT_WORDS = [
    "existence", "perception", "eternity", "wonder", "look closer",
    "stay curious", "consciousness", "clarity", "horizon", "infinity",
    "presence", "silence", "radiance", "reflection", "insight",
    "empathy", "mystery", "serenity", "awakening", "harmony",
    "cosmos", "memory", "origin", "vision", "truth", "light",
    "dream", "spirit", "essence", "timeless", "intimate", "witness",
    "observer", "vivid", "lucid", "transcend", "illuminate", "connect",
    "breathe", "imagine", "perceive", "discover", "believe", "focus",
]

PUPIL_DARK_WORDS = [
    "within", "silence", "origin", "eternity", "mystery", "depth",
    "unseen", "essence", "center", "stillness", "cosmos", "infinite",
    "shadow", "secret", "truth", "existence", "source", "soul",
    "awareness", "void", "core", "unknown", "singularity", "intimate",
]

PUPIL_SIGNAL_FRAGMENTS = [
    "observer", "you see", "remember", "awareness", "before", "after",
    "infinite", "becoming", "why", "who observes", "eternity", "return",
    "the source", "presence", "awakening", "the unseen",
]

HIGHLIGHT_WORDS = [
    "light", "clarity", "wonder", "truth", "shine", "vision",
    "lucid", "spark", "pure", "awake", "vivid", "radiance",
    "star", "clear", "see", "glow", "illuminate",
]

FIBER_MICRO_WORDS = [
    "truth", "light", "thought", "memory", "vision", "spirit",
    "source", "essence", "cosmos", "lucid", "awake", "eternal",
    "wonder", "pure", "origin", "core", "infinite", "presence",
    "becoming", "seeing", "knowing", "clarity", "harmony",
]

RADIAL_SENTENCE_FIBERS = [
    "awareness is the canvas of existence",
    "what you seek is seeking you",
    "we are made of stars",
    "the truth hides between the lines",
    "memory is starlight traveling through mind",
    "every ending begins somewhere",
    "within the finite dwells the infinite",
    "the observer and the observed are one",
    "thought is the brushstroke of reality",
    "all things are woven from the same light",
    "patterns of light become living thought",
    "the eye reads what the heart remembers",
    "in stillness the hidden becomes clear",
]

THOUGHT_BIRTH_WORDS = [
    "thought", "spark", "origin", "idea", "wake", "aware",
    "lucid", "perceive", "bloom", "born", "presence", "light",
]

SOLITARY_THOUGHTS = [
    "you are looking. but something is looking back.",
    "the observer and the observed are one.",
    "in stillness the hidden becomes clear.",
    "within the finite dwells the infinite.",
    "light remembers where it has been.",
    "we are the universe becoming aware of itself.",
    "look within. the abyss is looking back.",
    "consciousness observing itself across eternity.",
]

HIDDEN_REVELATIONS = [
    "I SEE YOU",
    "THE OBSERVER IS THE OBSERVED",
    "CONSCIOUSNESS",
    "SINGULARITY",
    "LOOK WITHIN",
    "THE UNIVERSE WITHIN",
]


def generate_meaningful_quotes(rng: random.Random, mode: str = "quote") -> str:
    """
    Return a genuine, correctly spelled quote, philosophical sentence, or word.
    Modes: 'quote', 'mixed', 'short', 'pupil', 'highlight', 'fiber', 'radial_fiber', 'signal'.
    """
    if mode == "highlight":
        return rng.choice(HIGHLIGHT_WORDS)
    if mode == "pupil":
        return rng.choice(PUPIL_DARK_WORDS)
    if mode == "signal":
        return rng.choice(PUPIL_SIGNAL_FRAGMENTS)
    if mode == "fiber":
        return rng.choice(FIBER_MICRO_WORDS)
    if mode == "radial_fiber":
        return rng.choice(RADIAL_SENTENCE_FIBERS)
    if mode == "short":
        return rng.choice(MEANINGFUL_SHORT_WORDS)
    if mode == "quote":
        if rng.random() < 0.48:
            return rng.choice(SIGNATURE_QUOTES)
        return rng.choice(ADDITIONAL_POETIC_QUOTES)

    r = rng.random()
    if r < 0.40:
        return rng.choice(SIGNATURE_QUOTES)
    elif r < 0.76:
        return rng.choice(ADDITIONAL_POETIC_QUOTES)
    else:
        return rng.choice(MEANINGFUL_SHORT_WORDS)


# ============================================================================
# 2. COLOR PALETTES & ATMOSPHERIC THEMES
# ============================================================================

@dataclass
class TypographyPalette:
    name: str
    canvas_bg: Tuple[int, int, int]
    bg_field_dark: List[Tuple[int, int, int]]      # Deep obsidian shadows for outer field
    bg_field_orbital: List[Tuple[int, int, int]]   # Orbital brow/cheekbone tones
    sclera_colors: List[Tuple[int, int, int]]      # Porcelain, ivory, cool pale blue & warm peach
    iris_outer: List[Tuple[int, int, int]]         # Limbal ring & deep borders
    iris_mid: List[Tuple[int, int, int]]           # Vibrant glowing iris body
    iris_inner: List[Tuple[int, int, int]]         # Collarette glowing ring
    iris_alt: List[Tuple[int, int, int]]           # Dynamic breathing phase-shift
    pupil_words: List[Tuple[int, int, int]]        # Deep abyss text
    highlight_words: List[Tuple[int, int, int]]    # Blinding specular reflections
    eyelid_rim: List[Tuple[int, int, int]]         # Luminous lid margin
    eyelid_sheet: List[Tuple[int, int, int]]       # Eyelid fold tones
    accent_tint: Tuple[int, int, int]              # Primary glowing color
    ember_color: Tuple[int, int, int] = (255, 35, 75)  # Floating ember glow


PALETTES: List[TypographyPalette] = [
    TypographyPalette(
        name="Crimson Requiem — Anime Blood Ruby & Obsidian",
        canvas_bg=(2, 2, 6),
        bg_field_dark=[
            (32, 8, 16), (42, 10, 22), (24, 6, 14),
            (48, 12, 26), (28, 8, 20), (18, 5, 12),
        ],
        bg_field_orbital=[
            (76, 18, 36), (92, 22, 44), (64, 14, 30), (108, 26, 52),
        ],
        sclera_colors=[
            (255, 245, 248), (245, 238, 242), (255, 222, 215),
            (230, 236, 250), (255, 192, 180),
        ],
        iris_outer=[
            (52, 4, 14), (82, 8, 22), (115, 10, 28), (42, 3, 10),
        ],
        iris_mid=[
            (255, 18, 56), (255, 38, 76), (235, 12, 48),
            (255, 68, 102), (218, 6, 40), (255, 88, 122),
        ],
        iris_inner=[
            (255, 142, 172), (255, 195, 218), (255, 92, 132), (255, 220, 232),
        ],
        iris_alt=[
            (255, 26, 78), (240, 14, 46), (255, 62, 112), (225, 8, 38),
        ],
        pupil_words=[
            (38, 5, 14), (48, 6, 18), (28, 3, 10), (58, 8, 22),
        ],
        highlight_words=[
            (255, 255, 255), (255, 235, 244), (255, 192, 218),
        ],
        eyelid_rim=[
            (255, 228, 238), (255, 172, 192), (245, 88, 118), (255, 138, 168),
        ],
        eyelid_sheet=[
            (112, 18, 38), (90, 14, 30), (135, 24, 48), (78, 12, 26),
        ],
        accent_tint=(255, 28, 70),
        ember_color=(255, 40, 80),
    ),
    TypographyPalette(
        name="Midnight Eclipse — Neon Cyan, Electric Blue & Void",
        canvas_bg=(2, 4, 10),
        bg_field_dark=[
            (18, 32, 60), (24, 40, 72), (28, 34, 62),
            (20, 36, 68), (32, 48, 84),
        ],
        bg_field_orbital=[
            (52, 82, 136), (62, 74, 132), (48, 76, 126), (72, 98, 152),
        ],
        sclera_colors=[
            (244, 248, 255), (242, 236, 224), (208, 224, 244),
            (184, 212, 242), (228, 236, 248),
        ],
        iris_outer=[
            (18, 48, 125), (42, 32, 128), (14, 78, 138), (52, 38, 142),
        ],
        iris_mid=[
            (0, 225, 255), (20, 240, 220), (45, 160, 255),
            (120, 85, 255), (0, 205, 220), (70, 200, 255),
        ],
        iris_inner=[
            (140, 252, 255), (90, 238, 255), (190, 248, 255), (165, 142, 255),
        ],
        iris_alt=[
            (145, 82, 255), (0, 245, 220), (50, 182, 255), (180, 110, 255),
        ],
        pupil_words=[
            (18, 28, 54), (24, 36, 65), (28, 26, 58), (16, 26, 48),
        ],
        highlight_words=[
            (255, 255, 255), (225, 250, 255), (195, 242, 255),
        ],
        eyelid_rim=[
            (235, 246, 255), (200, 225, 252), (175, 210, 248), (220, 235, 255),
        ],
        eyelid_sheet=[
            (82, 118, 172), (92, 84, 152), (72, 102, 152), (108, 138, 188),
        ],
        accent_tint=(0, 210, 255),
        ember_color=(0, 220, 255),
    ),
    TypographyPalette(
        name="Bioluminescent Monarch — Emerald, Turquoise & Abyssal Jade",
        canvas_bg=(2, 6, 8),
        bg_field_dark=[
            (16, 42, 50), (22, 52, 60), (14, 38, 48), (26, 58, 66),
        ],
        bg_field_orbital=[
            (42, 88, 98), (50, 98, 108), (36, 78, 92),
        ],
        sclera_colors=[
            (242, 252, 248), (238, 236, 226), (205, 232, 228), (182, 220, 224),
        ],
        iris_outer=[
            (10, 68, 72), (16, 54, 98), (8, 82, 64), (26, 46, 102),
        ],
        iris_mid=[
            (0, 235, 188), (20, 245, 216), (38, 192, 242), (16, 215, 156),
        ],
        iris_inner=[
            (145, 255, 230), (100, 250, 244), (185, 255, 240), (85, 242, 202),
        ],
        iris_alt=[
            (0, 205, 250), (55, 252, 172), (28, 228, 222), (115, 255, 208),
        ],
        pupil_words=[
            (14, 32, 38), (18, 38, 48), (18, 28, 44),
        ],
        highlight_words=[
            (255, 255, 255), (225, 255, 250), (190, 250, 242),
        ],
        eyelid_rim=[
            (228, 250, 246), (192, 232, 226), (168, 216, 212),
        ],
        eyelid_sheet=[
            (72, 130, 136), (62, 108, 124), (88, 146, 150),
        ],
        accent_tint=(0, 225, 180),
        ember_color=(0, 245, 190),
    ),
    TypographyPalette(
        name="Astral Sovereign — Amethyst, Royal Purple & Starlight",
        canvas_bg=(4, 3, 10),
        bg_field_dark=[
            (32, 26, 60), (38, 32, 70), (28, 36, 65), (44, 36, 78),
        ],
        bg_field_orbital=[
            (68, 58, 118), (60, 70, 122), (78, 66, 132),
        ],
        sclera_colors=[
            (248, 245, 255), (242, 236, 230), (218, 214, 242), (195, 208, 245),
        ],
        iris_outer=[
            (55, 26, 115), (78, 22, 105), (34, 38, 120), (66, 24, 94),
        ],
        iris_mid=[
            (185, 95, 255), (135, 118, 255), (228, 92, 238), (80, 182, 255),
        ],
        iris_inner=[
            (240, 195, 255), (202, 228, 255), (252, 210, 255), (170, 145, 255),
        ],
        iris_alt=[
            (98, 188, 255), (238, 115, 255), (160, 130, 255), (248, 150, 240),
        ],
        pupil_words=[
            (26, 18, 50), (32, 22, 58), (22, 26, 52),
        ],
        highlight_words=[
            (255, 255, 255), (248, 240, 255), (222, 245, 255),
        ],
        eyelid_rim=[
            (245, 235, 255), (215, 202, 248), (192, 210, 252),
        ],
        eyelid_sheet=[
            (108, 90, 165), (88, 102, 155), (124, 105, 175),
        ],
        accent_tint=(185, 105, 255),
        ember_color=(205, 120, 255),
    ),
    TypographyPalette(
        name="Solar Flare — Molten Gold, Incandescent Amber & Sunburst",
        canvas_bg=(6, 4, 2),
        bg_field_dark=[
            (45, 26, 12), (55, 32, 16), (38, 20, 10), (62, 38, 18),
        ],
        bg_field_orbital=[
            (92, 58, 28), (112, 70, 34), (80, 48, 22), (128, 80, 40),
        ],
        sclera_colors=[
            (255, 250, 242), (252, 244, 230), (255, 232, 208), (245, 236, 220),
        ],
        iris_outer=[
            (85, 38, 10), (115, 48, 14), (68, 28, 8), (135, 58, 18),
        ],
        iris_mid=[
            (255, 165, 0), (255, 195, 30), (255, 130, 10), (255, 215, 60),
        ],
        iris_inner=[
            (255, 235, 160), (255, 248, 200), (255, 215, 120), (255, 255, 220),
        ],
        iris_alt=[
            (255, 140, 20), (255, 185, 45), (255, 110, 0), (255, 225, 80),
        ],
        pupil_words=[
            (42, 22, 8), (52, 28, 10), (32, 16, 6),
        ],
        highlight_words=[
            (255, 255, 255), (255, 250, 230), (255, 240, 205),
        ],
        eyelid_rim=[
            (255, 242, 220), (255, 215, 160), (245, 180, 100),
        ],
        eyelid_sheet=[
            (145, 88, 38), (120, 72, 30), (168, 102, 45),
        ],
        accent_tint=(255, 180, 25),
        ember_color=(255, 190, 40),
    ),
]


# ============================================================================
# 3. FONT MANAGEMENT & SHARP TYPOGRAPHY RENDERING
# ============================================================================

class FontManager:
    """Loads clean, highly legible system fonts (Regular & Bold weights) and caches them."""

    FONT_CANDIDATES = [
        ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        ("/System/Library/Fonts/Optima.ttc", 0, 1),
        ("/System/Library/Fonts/HelveticaNeue.ttc", 0, 1),
        ("/System/Library/Fonts/Avenir Next.ttc", 7, 2),
        ("/Library/Fonts/Arial.ttf", 0, 0),
    ]

    def __init__(self) -> None:
        self.font_path: Optional[str] = None
        self.bold_path: Optional[str] = None
        self.reg_index: int = 0
        self.bold_index: int = 0
        for cand in self.FONT_CANDIDATES:
            if len(cand) == 2:
                reg_p, bold_p = cand
                if os.path.exists(reg_p):
                    self.font_path = reg_p
                    self.bold_path = bold_p if os.path.exists(bold_p) else reg_p
                    self.reg_index = 0
                    self.bold_index = 0
                    break
            elif len(cand) == 3:
                path, r_idx, b_idx = cand
                if os.path.exists(path):
                    self.font_path = path
                    self.bold_path = path
                    self.reg_index = r_idx
                    self.bold_index = b_idx
                    break
        self.pil_cache: Dict[Tuple[int, bool], ImageFont.FreeTypeFont] = {}

    def get_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        size = max(7, int(size))
        key = (size, bold)
        if key not in self.pil_cache:
            if self.font_path:
                try:
                    target_path = self.bold_path if (bold and self.bold_path) else self.font_path
                    idx = self.bold_index if bold else self.reg_index
                    self.pil_cache[key] = ImageFont.truetype(target_path, size, index=idx)
                except Exception:
                    self.pil_cache[key] = ImageFont.load_default()
            else:
                self.pil_cache[key] = ImageFont.load_default()
        return self.pil_cache[key]

    def measure(self, text: str, size: int, bold: bool = False) -> Tuple[float, float]:
        font = self.get_font(size, bold=bold)
        bbox = font.getbbox(text)
        return float(max(4, bbox[2] - bbox[0])), float(max(4, bbox[3] - bbox[1]))


def pil_to_pygame(pil_img: Image.Image) -> pygame.Surface:
    """Convert an RGBA PIL image to a hardware-accelerated alpha Pygame surface."""
    if pil_img.mode != "RGBA":
        pil_img = pil_img.convert("RGBA")
    from_fn = getattr(pygame.image, "frombytes", None) or getattr(pygame.image, "fromstring")
    return from_fn(pil_img.tobytes(), pil_img.size, "RGBA").convert_alpha()


def draw_word_pil(
    target_img: Image.Image,
    font_mgr: FontManager,
    text: str,
    cx: float,
    cy: float,
    font_size: int,
    angle_deg: float,
    color_rgba: Tuple[int, int, int, int],
    bold: bool = False,
) -> None:
    """Render an anti-aliased word/quote centered at `(cx, cy)` rotated by `angle_deg`."""
    font = font_mgr.get_font(font_size, bold=bold)
    bbox = font.getbbox(text)
    tw = max(1, bbox[2] - bbox[0] + 4)
    th = max(1, bbox[3] - bbox[1] + 4)

    if abs(angle_deg) <= 0.45:
        draw = ImageDraw.Draw(target_img)
        tx = int(round(cx - tw / 2.0 + 2 - bbox[0]))
        ty = int(round(cy - th / 2.0 + 2 - bbox[1]))
        draw.text((tx, ty), text, font=font, fill=color_rgba)
        return

    txt_img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_img)
    draw.text((2 - bbox[0], 2 - bbox[1]), text, font=font, fill=color_rgba)
    txt_img = txt_img.rotate(angle_deg, resample=Image.BICUBIC, expand=True)

    px = int(round(cx - txt_img.width / 2.0))
    py = int(round(cy - txt_img.height / 2.0))

    if px >= target_img.width or py >= target_img.height:
        return
    if px + txt_img.width <= 0 or py + txt_img.height <= 0:
        return

    src_x = max(0, -px)
    src_y = max(0, -py)
    dst_x = max(0, px)
    dst_y = max(0, py)

    if (
        src_x > 0
        or src_y > 0
        or dst_x + txt_img.width > target_img.width
        or dst_y + txt_img.height > target_img.height
    ):
        crop_w = min(txt_img.width - src_x, target_img.width - dst_x)
        crop_h = min(txt_img.height - src_y, target_img.height - dst_y)
        if crop_w <= 0 or crop_h <= 0:
            return
        txt_img = txt_img.crop((src_x, src_y, src_x + crop_w, src_y + crop_h))

    target_img.alpha_composite(txt_img, (dst_x, dst_y))


def create_word_sprite(
    font_mgr: FontManager,
    text: str,
    font_size: int,
    angle_deg: float,
    color_rgba: Tuple[int, int, int, int],
    bold: bool = False,
) -> pygame.Surface:
    font = font_mgr.get_font(font_size, bold=bold)
    bbox = font.getbbox(text)
    tw = max(1, bbox[2] - bbox[0] + 4)
    th = max(1, bbox[3] - bbox[1] + 4)
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((2 - bbox[0], 2 - bbox[1]), text, font=font, fill=color_rgba)
    if abs(angle_deg) > 0.45:
        img = img.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    return pil_to_pygame(img)


# ============================================================================
# 4. CALCULATING THE EYE'S SPATIAL AND COLOR PATTERNS
# ============================================================================

@dataclass
class EyeCanvasGeometry:
    """
    Defines both the physical screen resolution and the larger high-resolution
    virtual typography canvas so zooming in/out is always razor-sharp and never
    exposes blank edges.
    """
    screen_w: int
    screen_h: int
    canvas_w: int
    canvas_h: int
    center_x: int
    center_y: int
    eye_half_w: float
    eye_half_h: float
    iris_radius: float
    pupil_radius: float
    scale: float


def calculate_eye_spatial_and_color_patterns(
    screen_w: int, screen_h: int
) -> EyeCanvasGeometry:
    """
    Create a virtual typography canvas 1.55x larger than the physical screen.
    In the wide camera view (zoom=1.0), the viewport shows the central ~82% of the
    virtual canvas where the giant eye fills ~90% of the screen width.
    """
    canvas_mult = 1.55
    canvas_w = int(round(screen_w * canvas_mult))
    canvas_h = int(round(screen_h * canvas_mult))
    if canvas_w % 2 == 1:
        canvas_w += 1
    if canvas_h % 2 == 1:
        canvas_h += 1

    center_x = canvas_w // 2
    center_y = canvas_h // 2

    scale = min(screen_w / 1512.0, screen_h / 982.0) * 1.18

    wide_view_w = canvas_w * 0.82
    wide_view_h = canvas_h * 0.82
    eye_half_w = wide_view_w * 0.455
    eye_half_h = wide_view_h * 0.285

    iris_radius = eye_half_h * 1.02
    pupil_radius = iris_radius * 0.34

    return EyeCanvasGeometry(
        screen_w=screen_w,
        screen_h=screen_h,
        canvas_w=canvas_w,
        canvas_h=canvas_h,
        center_x=center_x,
        center_y=center_y,
        eye_half_w=eye_half_w,
        eye_half_h=eye_half_h,
        iris_radius=iris_radius,
        pupil_radius=pupil_radius,
        scale=scale,
    )


def eval_eyelid_curves(
    u: np.ndarray,
    openness: float,
    geom: EyeCanvasGeometry,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Evaluate upper and lower eyelid vertical offsets y_upper(u), y_lower(u)
    relative to `geom.center_y` (+y is downward on screen).
    `u` in [-1.0, +1.0] spans from inner medial corner (-1) to outer lateral corner (+1).
    """
    u_clamped = np.clip(u, -1.0, 1.0)
    env = np.power(np.maximum(0.0, 1.0 - u_clamped * u_clamped), 0.76)

    upper_arch = 1.0 - 0.11 * u_clamped - 0.06 * (u_clamped ** 2)
    lower_arch = 1.0 + 0.13 * u_clamped - 0.05 * (u_clamped ** 2)

    y_upper_open = -geom.eye_half_h * 1.04 * env * upper_arch
    y_lower_open = +geom.eye_half_h * 0.88 * env * lower_arch

    medial_dip = 0.09 * geom.eye_half_h * np.exp(-((u_clamped + 0.89) / 0.20) ** 2)
    lateral_sweep = -0.06 * geom.eye_half_h * np.exp(-((u_clamped - 0.86) / 0.25) ** 2)
    corner_line = medial_dip + lateral_sweep

    y_upper_open += corner_line
    y_lower_open += corner_line

    # Closed eye curve: gentle downward-sloping sleeping curve
    y_closed = geom.eye_half_h * 0.16 * env + corner_line

    t = float(np.clip(openness, 0.0, 1.0))
    y_upper = y_closed * (1.0 - t) + y_upper_open * t
    y_lower = y_closed * (1.0 - t) + y_lower_open * t
    return y_upper, y_lower


def eval_field_streamline_y(
    x_arr: np.ndarray,
    base_y_offset: float,
    geom: EyeCanvasGeometry,
) -> np.ndarray:
    """
    Smooth, continuous streamline function across the entire virtual canvas.
    Wait: notice that `arch_push` is proportional to `base_y_offset`, so as
    `base_y_offset -> 0`, `arch_push -> 0` smoothly with ZERO discontinuity or gaps!
    Every row of poetry is continuous and evenly spaced across 100% of the canvas.
    """
    u = (x_arr - geom.center_x) / geom.eye_half_w
    gaussian_bell = np.exp(-0.5 * (u / 0.76) ** 2)
    norm_y = abs(base_y_offset) / max(1.0, geom.eye_half_h)
    dist_atten = np.exp(-norm_y / 1.85)
    arch_push = base_y_offset * 0.42 * gaussian_bell * dist_atten
    return geom.center_y + base_y_offset + arch_push


# ============================================================================
# 5. LAYING OUT READABLE TEXT ACROSS THE ENTIRE VIRTUAL CANVAS
# ============================================================================

def layout_full_canvas_typography(
    geom: EyeCanvasGeometry,
    font_mgr: FontManager,
    palette: TypographyPalette,
    rng: random.Random,
) -> Tuple[pygame.Surface, pygame.Surface, pygame.Surface]:
    """
    Populate 100% of the virtual canvas with non-overlapping, readable quotes and words:
      1. `full_field_surf`: Covers 100% of `(canvas_w, canvas_h)` from edge to edge and
         corner to corner with zero gaps.
         - Outside the eye contour: shaded in midnight navy, slate blue, and orbital indigo.
         - Along the eyelid folds and inside the eye footprint (revealed during a blink!):
           shaded in luminous eyelid-sheet and eyelid-rim typography, including a bright
           curved horizontal band of words along the closed-eyelid seam!
      2. `sclera_surf`: Bright ivory, silver-white, and icy-blue readable quotes filling
         the eyeball interior with 3D spherical shading.
      3. `iris_cutout_mask`: Circular cutout so sclera quotes do not bleed behind the iris.
    """
    # ------------------------------------------------------------------------
    # A. FULL-CANVAS WALL OF POETRY (100% Edge-to-Edge Coverage, Zero Blank Areas)
    # ------------------------------------------------------------------------
    field_pil = Image.new("RGBA", (geom.canvas_w, geom.canvas_h), (*palette.canvas_bg, 255))

    row_spacing = max(16.0, 18.0 * geom.scale)
    max_y_extent = geom.canvas_h * 0.54
    y_offsets = np.arange(-max_y_extent, max_y_extent + row_spacing, row_spacing)

    for r_idx, base_y_off in enumerate(y_offsets):
        if r_idx % 4 == 0:
            fsize = max(10, int(12.8 * geom.scale))
        elif r_idx % 2 == 0:
            fsize = max(9, int(11.4 * geom.scale))
        else:
            fsize = max(8, int(10.2 * geom.scale))

        x_cursor = 6.0 + rng.uniform(0.0, 18.0)
        while x_cursor < geom.canvas_w - 8.0:
            text = generate_meaningful_quotes(rng, "mixed")
            is_bold = (r_idx % 5 == 0)
            w_px, _ = font_mgr.measure(text, fsize, bold=is_bold)
            gap_px = max(10.0, 12.0 * geom.scale)
            wx = x_cursor + w_px * 0.5

            if wx - w_px * 0.5 > geom.canvas_w:
                break

            x_sample = np.array([wx - 12.0, wx, wx + 12.0])
            y_sample = eval_field_streamline_y(x_sample, float(base_y_off), geom)
            wy = float(y_sample[1])

            if -20.0 <= wy <= geom.canvas_h + 20.0:
                slope = float(y_sample[2] - y_sample[0]) / 24.0
                angle = -math.degrees(math.atan(slope))

                u_rel = (wx - geom.center_x) / geom.eye_half_w
                v_rel = (wy - geom.center_y) / geom.eye_half_h
                elliptical_dist = math.hypot(u_rel * 0.88, v_rel * 0.78)

                # Evaluate open & closed eyelid curves at u_rel to sculpt the eyelid & brow anatomy
                yu_arr, yl_arr = eval_eyelid_curves(np.array([u_rel]), 1.0, geom)
                yc_arr, _ = eval_eyelid_curves(np.array([u_rel]), 0.0, geom)
                yu_open = float(yu_arr[0])
                yl_open = float(yl_arr[0])
                y_closed = float(yc_arr[0])
                dy_from_center = wy - geom.center_y

                if abs(u_rel) <= 1.03 and (yu_open - 46.0 * geom.scale) <= dy_from_center <= (yl_open + 42.0 * geom.scale):
                    # Inside the Eyelid / Palpebral Region (including what is revealed when the eye closes!)
                    dist_to_closed_seam = abs(dy_from_center - y_closed)
                    dist_to_upper_open = abs(dy_from_center - yu_open)
                    dist_to_lower_open = abs(dy_from_center - yl_open)

                    if dist_to_closed_seam < 15.0 * geom.scale:
                        # Luminous narrow curved line of words at complete eyelid closure!
                        col = rng.choice(palette.eyelid_rim)
                        shade = 1.0
                        alpha = 252
                        is_bold = True
                    elif dist_to_upper_open < 24.0 * geom.scale or dist_to_lower_open < 22.0 * geom.scale:
                        # Bright upper & lower eyelid contour bands framing the eye
                        col = rng.choice(palette.eyelid_rim)
                        shade = 0.92
                        alpha = rng.randint(225, 250)
                        is_bold = True
                    else:
                        # Eyelid fold typography (visible as the upper eyelid descends during blinks)
                        col = rng.choice(palette.eyelid_sheet)
                        shade = max(0.68, 1.0 - 0.25 * abs(u_rel))
                        alpha = rng.randint(205, 240)
                elif elliptical_dist < 1.58:
                    # Surrounding orbital brow & cheekbone typography
                    col = rng.choice(palette.bg_field_orbital)
                    t_halo = max(0.0, (elliptical_dist - 1.0) / 0.58)
                    shade = 1.0 - 0.24 * t_halo
                    alpha = rng.randint(205, 240)
                else:
                    # Outer full-screen typography field extending to all 4 corners
                    col = rng.choice(palette.bg_field_dark)
                    wave = 0.88 + 0.12 * math.sin(u_rel * 2.0 + v_rel * 1.6)
                    shade = wave
                    alpha = rng.randint(200, 238)

                r = int(min(255, col[0] * shade))
                g = int(min(255, col[1] * shade))
                b = int(min(255, col[2] * shade))
                draw_word_pil(
                    field_pil, font_mgr, text, wx, wy, fsize, angle, (r, g, b, alpha), bold=is_bold
                )

                # Micro-text plane: tiny philosophical fragments hidden between rows (revealed on zoom!)
                if rng.random() < 0.32 and elliptical_dist > 1.12:
                    m_word = generate_meaningful_quotes(rng, "short")
                    m_fsize = max(5, int(5.8 * geom.scale))
                    m_wy = wy - row_spacing * 0.44
                    if 10.0 < m_wy < geom.canvas_h - 10.0:
                        m_col = (int(col[0] * 0.58), int(col[1] * 0.58), int(col[2] * 0.58), rng.randint(80, 135))
                        draw_word_pil(field_pil, font_mgr, m_word, wx, m_wy, m_fsize, angle * 0.6, m_col)

            x_cursor += w_px + gap_px

    # ------------------------------------------------------------------------
    # B. SCLERA TYPOGRAPHY (Dramatic Anime Lighting, Specular Beads & Quotes)
    # ------------------------------------------------------------------------
    sclera_pil = Image.new("RGBA", (geom.canvas_w, geom.canvas_h), (0, 0, 0, 0))
    sclera_bg_draw = ImageDraw.Draw(sclera_pil)
    u_poly = np.linspace(-1.0, 1.0, 120)
    yu_p, yl_p = eval_eyelid_curves(u_poly, 1.0, geom)
    xp = geom.center_x + u_poly * geom.eye_half_w
    pts_open = list(zip(xp.tolist(), (geom.center_y + yu_p).tolist())) + list(
        zip(xp[::-1].tolist(), (geom.center_y + yl_p[::-1]).tolist())
    )
    # Base porcelain tone
    sclera_bg_draw.polygon(pts_open, fill=(244, 240, 248, 255))

    # Upper eyelid deep cast shadow (dramatic cinematic anime shading)
    shadow_img = Image.new("RGBA", (geom.canvas_w, geom.canvas_h), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow_img)
    sh_draw.polygon(pts_open, fill=(8, 10, 24, 240))
    grad_mask = Image.new("L", (geom.canvas_w, geom.canvas_h), 0)
    gm_draw = ImageDraw.Draw(grad_mask)
    y_min_bound = int(geom.center_y - geom.eye_half_h * 1.3)
    y_fade_bound = int(geom.center_y + geom.eye_half_h * 0.12)
    gm_draw.rectangle(
        (0, y_min_bound, geom.canvas_w, y_fade_bound),
        fill=255,
    )
    grad_mask = grad_mask.filter(ImageFilter.GaussianBlur(radius=max(4, int(22 * geom.scale))))
    shadow_img.putalpha(Image.composite(shadow_img.getchannel("A"), Image.new("L", (geom.canvas_w, geom.canvas_h), 0), grad_mask))
    sclera_pil.alpha_composite(shadow_img)

    # Warm amber / peach subsurface lighting near medial & lateral corners
    glow_corner = Image.new("RGBA", (geom.canvas_w, geom.canvas_h), (0, 0, 0, 0))
    gc_draw = ImageDraw.Draw(glow_corner)
    ew_px = int(geom.eye_half_w)
    eh_px = int(geom.eye_half_h)
    gc_draw.ellipse(
        (geom.center_x - int(ew_px * 0.98), geom.center_y - int(eh_px * 0.25),
         geom.center_x - int(ew_px * 0.38), geom.center_y + int(eh_px * 0.45)),
        fill=(255, 175, 140, 130),
    )
    gc_draw.ellipse(
        (geom.center_x + int(ew_px * 0.38), geom.center_y - int(eh_px * 0.25),
         geom.center_x + int(ew_px * 0.98), geom.center_y + int(eh_px * 0.45)),
        fill=(255, 160, 130, 95),
    )
    glow_corner = glow_corner.filter(ImageFilter.GaussianBlur(radius=max(4, int(18 * geom.scale))))
    sclera_pil.alpha_composite(glow_corner)

    n_sclera_rows = 28
    for row_idx in range(n_sclera_rows):
        v_frac = (row_idx + 0.5) / n_sclera_rows
        fsize = max(9, int((10.2 + 3.6 * math.sin(v_frac * math.pi)) * geom.scale))
        u_cursor = -0.97 + rng.uniform(0.0, 0.025)

        while u_cursor < 0.97:
            mode = "short" if abs(u_cursor) > 0.74 else "mixed"
            quote = generate_meaningful_quotes(rng, mode)
            is_bold = (row_idx % 4 == 0)
            w_px, _ = font_mgr.measure(quote, fsize, bold=is_bold)
            du = (w_px + 8.0 * geom.scale) / geom.eye_half_w
            u_mid = u_cursor + du * 0.5
            if u_mid > 0.97:
                break

            y_u_arr, y_l_arr = eval_eyelid_curves(
                np.array([u_mid - 0.025, u_mid, u_mid + 0.025]), 1.0, geom
            )
            yu, yl = float(y_u_arr[1]), float(y_l_arr[1])
            if yl - yu < fsize * 0.75:
                u_cursor += du * 0.65
                continue

            wy_rel = yu + v_frac * (yl - yu)
            wx_rel = u_mid * geom.eye_half_w

            y0 = float(y_u_arr[0] + v_frac * (y_l_arr[0] - y_u_arr[0]))
            y2 = float(y_u_arr[2] + v_frac * (y_l_arr[2] - y_u_arr[2]))
            slope = (y2 - y0) / (0.05 * geom.eye_half_w)
            angle = -math.degrees(math.atan(slope))

            dist_x = abs(u_mid)
            dist_y = abs(v_frac - 0.52) * 1.7
            sphere_shade = max(
                0.38,
                min(1.0, 1.16 - 0.62 * (dist_x ** 1.55) - 0.22 * (dist_y ** 1.5)),
            )
            lid_shadow = min(1.0, 0.56 + 0.70 * v_frac)
            brightness = sphere_shade * lid_shadow

            base_col = rng.choice(palette.sclera_colors)
            r = int(min(255, base_col[0] * brightness))
            g = int(min(255, base_col[1] * brightness))
            b = int(min(255, base_col[2] * brightness))
            alpha = int(min(255, 205 + 50 * brightness))

            wx = geom.center_x + wx_rel
            wy = geom.center_y + wy_rel
            draw_word_pil(
                sclera_pil, font_mgr, quote, wx, wy, fsize, angle, (r, g, b, alpha), bold=is_bold
            )
            u_cursor += du

    # Glossy vertical specular beads on the lower sclera surface (anime wet glass reflections)
    sclera_draw = ImageDraw.Draw(sclera_pil)
    bead_specs = [
        (0.44, 0.42, 6, 14, (255, 255, 255, 245)),
        (0.50, 0.46, 5, 11, (220, 205, 255, 220)),
        (0.56, 0.38, 4, 8, (255, 240, 250, 210)),
        (-0.52, 0.40, 5, 12, (255, 255, 255, 235)),
        (-0.46, 0.45, 4, 9, (215, 225, 255, 215)),
    ]
    for bx_f, by_f, bw_b, bh_b, b_col in bead_specs:
        bx_c = geom.center_x + int(bx_f * geom.eye_half_w)
        by_c = geom.center_y + int(by_f * geom.eye_half_h)
        bw_s = max(2, int(bw_b * geom.scale))
        bh_s = max(4, int(bh_b * geom.scale))
        sclera_draw.ellipse((bx_c - bw_s, by_c - bh_s, bx_c + bw_s, by_c + bh_s), fill=b_col)

    # Circular cutout mask so sclera quotes don't bleed behind the iris & pupil
    cutout_dim = int(geom.iris_radius * 2.25)
    cutout_pil = Image.new("RGBA", (cutout_dim, cutout_dim), (255, 255, 255, 255))
    c_draw = ImageDraw.Draw(cutout_pil)
    cr = int(geom.iris_radius * 0.97)
    cc = cutout_dim // 2
    c_draw.ellipse((cc - cr, cc - cr, cc + cr, cc + cr), fill=(0, 0, 0, 10))
    cutout_pil = cutout_pil.filter(ImageFilter.GaussianBlur(radius=max(3, int(7 * geom.scale))))

    return (
        pil_to_pygame(field_pil),
        pil_to_pygame(sclera_pil),
        pil_to_pygame(cutout_pil),
    )


# ============================================================================
# 6. CREATING THE IRIS, PUPIL & HIGHLIGHTS FROM TYPOGRAPHY
# ============================================================================

def create_iris_and_pupil_typography(
    geom: EyeCanvasGeometry,
    font_mgr: FontManager,
    palette: TypographyPalette,
    rng: random.Random,
) -> Dict[str, pygame.Surface]:
    """
    Build the giant Iris, Pupil, and Highlights using the 6-Layer Architecture:
      Layer 1 — Outer Iris: Subtle dark atmospheric ring establishing silhouette & volumetric shading.
      Layer 2 — Structural Fibers: 240 thin organic radial fibers with Bezier curvature and branching.
      Layer 3 — Fine Micro-Fibers: 360 thinner secondary fibers creating microscopic zoom complexity.
      Layer 4 — Radial Grooves: 72 subtle dark grooves between brighter structures giving depth.
      Layer 5 — Inner Iris: Dense collarette colonnade and radiating spikes near pupil.
      Layer 6 — Outer Ring: Subtle limbal ring defined with soft edge and organic stepped notches.
    Plus living infinite pupil with starlight horizons and translucent volumetric corneal highlights.
    """
    dim = int(geom.iris_radius * 2.38)
    if dim % 2 == 1:
        dim += 1
    icx, icy = dim // 2, dim // 2
    r_iris = int(geom.iris_radius)
    r_pupil = int(geom.pupil_radius)

    iris_pil = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(iris_pil)

    c_out = palette.iris_outer[0]
    c_mid = palette.iris_mid[0]
    c_in = palette.iris_inner[0]
    c_acc = palette.accent_tint

    # =========================================================================
    # LAYER 1: OUTER IRIS SILHOUETTE & BASE VOLUMETRIC GRADIENT
    # =========================================================================
    for r in range(r_iris, 0, -2):
        t = r / float(r_iris)
        if t > 0.88:
            ft = (t - 0.88) / 0.12
            col = (
                int(c_out[0] * (1.0 - 0.5 * ft)),
                int(c_out[1] * (1.0 - 0.5 * ft)),
                int(c_out[2] * (1.0 - 0.5 * ft)),
                255,
            )
        elif t > 0.44:
            ft = (t - 0.44) / (0.88 - 0.44)
            col = (
                int(c_in[0] * (1.0 - ft) + c_mid[0] * ft),
                int(c_in[1] * (1.0 - ft) + c_mid[1] * ft),
                int(c_in[2] * (1.0 - ft) + c_mid[2] * ft),
                255,
            )
        else:
            ft = t / 0.44
            col = (
                int(255 * (1.0 - ft * 0.10)),
                int(c_in[1] * ft + c_acc[1] * (1.0 - ft)),
                int(c_in[2] * ft + c_acc[2] * (1.0 - ft)),
                255,
            )
        draw.ellipse((icx - r, icy - r, icx + r, icy + r), fill=col)

    # Volumetric Directional Shading: Upper Lid Cast Shadow & Lower Internal Bounce
    shade_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shade_img)
    for sy in range(icy - r_iris, icy + int(r_iris * 0.18), 2):
        y_frac = (sy - (icy - r_iris)) / (r_iris * 1.18)
        alpha = int(210 * (1.0 - y_frac ** 1.3))
        s_draw.line((icx - r_iris, sy, icx + r_iris, sy), fill=(8, 1, 4, alpha), width=2)
    mask_disc = Image.new("L", (dim, dim), 0)
    m_draw = ImageDraw.Draw(mask_disc)
    m_draw.ellipse((icx - r_iris, icy - r_iris, icx + r_iris, icy + r_iris), fill=255)
    shade_img.putalpha(Image.composite(shade_img.getchannel("A"), Image.new("L", (dim, dim), 0), mask_disc))
    iris_pil.alpha_composite(shade_img)

    # Lower internal fiery bounce light (incandescent ruby reflection in lower half)
    bounce_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(bounce_img)
    b_cx = icx
    b_cy = icy + int(r_iris * 0.46)
    b_rx = int(r_iris * 0.70)
    b_ry = int(r_iris * 0.40)
    b_draw.ellipse((b_cx - b_rx, b_cy - b_ry, b_cx + b_rx, b_cy + b_ry), fill=(*c_acc, 170))
    bounce_img = bounce_img.filter(ImageFilter.GaussianBlur(radius=max(4, int(20 * geom.scale))))
    bounce_img.putalpha(Image.composite(bounce_img.getchannel("A"), Image.new("L", (dim, dim), 0), mask_disc))
    iris_pil.alpha_composite(bounce_img)

    # =========================================================================
    # LAYER 4: RADIAL GROOVES (Deep dark valleys between structural fibers)
    # =========================================================================
    grooves_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grooves_img)
    n_grooves = 72
    for gi in range(n_grooves):
        theta = (gi / float(n_grooves)) * math.tau + rng.uniform(-0.015, 0.015)
        r0 = r_pupil * rng.uniform(0.95, 1.10)
        r1 = r_iris * rng.uniform(0.82, 0.94)
        gx1 = icx + r0 * math.cos(theta)
        gy1 = icy + r0 * math.sin(theta)
        gx2 = icx + r1 * math.cos(theta)
        gy2 = icy + r1 * math.sin(theta)
        g_width = max(1, int(rng.choice([1.5, 2.5]) * geom.scale))
        g_draw.line((gx1, gy1, gx2, gy2), fill=(12, 1, 4, 185), width=g_width)
    grooves_img = grooves_img.filter(ImageFilter.GaussianBlur(radius=max(1.0, 1.5 * geom.scale)))
    iris_pil.alpha_composite(grooves_img)

    # =========================================================================
    # LAYER 2: THE 5 IRIS FIBER ARCHETYPES (THE IRIS IS CONSTRUCTED FROM WORDS)
    # Archetype A: Organic Structural Curved Fibers (smooth Bezier with branches)
    # Archetype B: Repeated Micro-Word Streams (radial words forming biological fibers)
    # Archetype C: Radial Sentence Streams (complete philosophy radiating outward)
    # Archetype D: Broken Ancient Glyphs & Crypt Valleys (lacunae & age)
    # Archetype E: Radiant Laser Light Rays (white-hot & electric crimson filaments)
    # =========================================================================
    fibers_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(fibers_img)

    # Archetype A: 160 Organic Structural Bezier Fibers
    n_fibers = 160
    for fi in range(n_fibers):
        theta = (fi / float(n_fibers)) * math.tau + rng.uniform(-0.008, 0.008)
        r_start = r_pupil * rng.uniform(0.98, 1.15)
        r_end = r_iris * rng.uniform(0.78, 0.92)
        curv = rng.uniform(-0.04, 0.04)

        r_mid = (r_start + r_end) * 0.5
        theta_mid = theta + curv

        p0 = (icx + r_start * math.cos(theta), icy + r_start * math.sin(theta))
        p1 = (icx + r_mid * math.cos(theta_mid), icy + r_mid * math.sin(theta_mid))
        p2 = (icx + r_end * math.cos(theta + curv * 0.5), icy + r_end * math.sin(theta + curv * 0.5))

        if fi % 12 == 0:
            fib_col = (255, 245, 250, 230)
            f_w = max(1, int(1.8 * geom.scale))
        elif fi % 4 == 0:
            fib_col = (*c_acc, 210)
            f_w = max(1, int(1.3 * geom.scale))
        else:
            fib_col = (int(c_in[0] * 0.95), int(c_in[1] * 0.95), int(c_in[2] * 0.95), rng.randint(140, 200))
            f_w = 1

        t_steps = 6
        pts_c = []
        for step in range(t_steps + 1):
            st = step / float(t_steps)
            bx = (1 - st) ** 2 * p0[0] + 2 * (1 - st) * st * p1[0] + st ** 2 * p2[0]
            by = (1 - st) ** 2 * p0[1] + 2 * (1 - st) * st * p1[1] + st ** 2 * p2[1]
            pts_c.append((bx, by))
        f_draw.line(pts_c, fill=fib_col, width=f_w)

        if rng.random() < 0.35:
            b_start = pts_c[len(pts_c) // 2]
            b_theta = theta + rng.uniform(-0.06, 0.06)
            b_r_end = r_end * rng.uniform(0.85, 1.05)
            b_end = (icx + b_r_end * math.cos(b_theta), icy + b_r_end * math.sin(b_theta))
            f_draw.line([b_start, b_end], fill=(fib_col[0], fib_col[1], fib_col[2], int(fib_col[3] * 0.65)), width=1)

    # Archetype B: 84 Repeated Micro-Word Streams (Words become biological striations!)
    micro_fsize = max(5, int(5.6 * geom.scale))
    n_word_fibers = 84
    for wfi in range(n_word_fibers):
        theta = (wfi / float(n_word_fibers)) * math.tau + rng.uniform(-0.012, 0.012)
        curv = rng.uniform(-0.03, 0.03)
        r_curr = r_pupil * rng.uniform(1.02, 1.12)
        r_max = r_iris * rng.uniform(0.78, 0.90)

        while r_curr < r_max:
            w_fib = generate_meaningful_quotes(rng, "fiber")
            w_len_px, _ = font_mgr.measure(w_fib, micro_fsize)
            r_mid = r_curr + w_len_px * 0.5
            if r_mid > r_max:
                break
            th_w = theta + curv * ((r_mid - r_pupil) / max(1.0, r_iris - r_pupil))
            wx = icx + r_mid * math.cos(th_w)
            wy = icy + r_mid * math.sin(th_w)
            deg_rad = -math.degrees(th_w)
            if 90 < (deg_rad % 360) < 270:
                deg_rad += 180.0

            f_col = rng.choice(palette.iris_inner if r_mid < r_iris * 0.62 else palette.iris_mid)
            f_alpha = rng.randint(145, 235)
            draw_word_pil(fibers_img, font_mgr, w_fib, wx, wy, micro_fsize, deg_rad, (*f_col, f_alpha))
            r_curr += w_len_px + 3.0 * geom.scale

    # Archetype C: 32 Radial Sentence Streams (Sentences radiating outward like cosmic laws)
    sent_fsize = max(6, int(6.8 * geom.scale))
    n_sent_fibers = 32
    for sfi in range(n_sent_fibers):
        theta = (sfi / float(n_sent_fibers)) * math.tau + rng.uniform(-0.015, 0.015)
        sentence = generate_meaningful_quotes(rng, "radial_fiber")
        r_curr = r_pupil * 1.08
        words = sentence.split()
        for sword in words:
            sw_px, _ = font_mgr.measure(sword, sent_fsize)
            r_mid = r_curr + sw_px * 0.5
            if r_mid > r_iris * 0.88:
                break
            wx = icx + r_mid * math.cos(theta)
            wy = icy + r_mid * math.sin(theta)
            deg_rad = -math.degrees(theta)
            if 90 < (deg_rad % 360) < 270:
                deg_rad += 180.0

            scol = (255, 238, 245) if sfi % 4 == 0 else palette.accent_tint
            salpha = rng.randint(160, 240)
            draw_word_pil(fibers_img, font_mgr, sword, wx, wy, sent_fsize, deg_rad, (*scol, salpha), bold=(sfi % 8 == 0))
            r_curr += sw_px + 4.5 * geom.scale

    # Archetype D: 48 Broken Ancient Glyphs & Crypt Imperfections
    for bfi in range(48):
        theta = rng.uniform(0, math.tau)
        bword = generate_meaningful_quotes(rng, "fiber")
        r_mid = r_pupil * 1.15 + rng.uniform(0.0, (r_iris - r_pupil) * 0.7)
        wx = icx + r_mid * math.cos(theta)
        wy = icy + r_mid * math.sin(theta)
        deg_rad = -math.degrees(theta)
        if 90 < (deg_rad % 360) < 270:
            deg_rad += 180.0
        draw_word_pil(fibers_img, font_mgr, bword, wx, wy, micro_fsize, deg_rad, (160, 18, 42, rng.randint(55, 110)))

    # Archetype E: 36 Radiant Laser Light Filaments
    for lfi in range(36):
        theta = (lfi / 36.0) * math.tau + rng.uniform(-0.02, 0.02)
        r0 = r_pupil * rng.uniform(0.98, 1.05)
        r1 = r_iris * rng.uniform(0.85, 0.94)
        lx1 = icx + r0 * math.cos(theta)
        ly1 = icy + r0 * math.sin(theta)
        lx2 = icx + r1 * math.cos(theta)
        ly2 = icy + r1 * math.sin(theta)
        l_col = (255, 255, 255, 245) if lfi % 6 == 0 else (*c_acc, 215)
        f_draw.line((lx1, ly1, lx2, ly2), fill=l_col, width=max(1, int(1.4 * geom.scale)))

    iris_pil.alpha_composite(fibers_img)

    # =========================================================================
    # LAYER 3: FINE MICRO-FIBERS (Microscopic complexity when zoomed in)
    # =========================================================================
    micro_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    mf_draw = ImageDraw.Draw(micro_img)
    n_micro = 320
    for mi in range(n_micro):
        theta = (mi / float(n_micro)) * math.tau + rng.uniform(-0.005, 0.005)
        r_start = r_pupil * rng.uniform(1.05, 1.45)
        r_end = r_iris * rng.uniform(0.65, 0.86)
        mx1 = icx + r_start * math.cos(theta)
        my1 = icy + r_start * math.sin(theta)
        mx2 = icx + r_end * math.cos(theta)
        my2 = icy + r_end * math.sin(theta)
        mf_alpha = rng.randint(55, 120)
        mf_draw.line((mx1, my1, mx2, my2), fill=(255, 225, 238, mf_alpha), width=1)
    iris_pil.alpha_composite(micro_img)

    # =========================================================================
    # LAYER 5: INNER IRIS COLLARETTE COLONNADE & COLLARETTE WORD-TEETH
    # =========================================================================
    coll_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    col_draw = ImageDraw.Draw(coll_img)
    for c_deg in range(0, 360, 2):
        rad = math.radians(c_deg)
        c_len = rng.choice([8, 14, 22, 34]) * geom.scale
        cx1 = icx + (r_pupil * 0.98) * math.cos(rad)
        cy1 = icy + (r_pupil * 0.98) * math.sin(rad)
        cx2 = icx + (r_pupil * 0.98 + c_len) * math.cos(rad)
        cy2 = icy + (r_pupil * 0.98 + c_len) * math.sin(rad)
        col_draw.line((cx1, cy1, cx2, cy2), fill=(*c_acc, rng.randint(180, 245)), width=max(1, int(1.4 * geom.scale)))

        # Collarette micro-word teeth at 12-degree intervals
        if c_deg % 12 == 0:
            c_word = rng.choice(["observe", "witness", "awake", "pure", "origin", "vision"])
            tx = icx + (r_pupil * 1.05 + c_len * 0.6) * math.cos(rad)
            ty = icy + (r_pupil * 1.05 + c_len * 0.6) * math.sin(rad)
            t_deg = -math.degrees(rad)
            if 90 < (t_deg % 360) < 270:
                t_deg += 180.0
            draw_word_pil(coll_img, font_mgr, c_word, tx, ty, max(5, int(5.5 * geom.scale)), t_deg, (*c_acc, 200))
    iris_pil.alpha_composite(coll_img)

    # =========================================================================
    # CONCENTRIC WORD TRACKS & CYBER RUNE CHANNELS
    # =========================================================================
    channel_fracs = [0.84, 0.76, 0.68, 0.60, 0.52, 0.44, 0.38]
    for ch_idx, frac in enumerate(channel_fracs):
        cr = int(r_iris * frac)
        draw.ellipse((icx - cr, icy - cr, icx + cr, icy + cr), outline=(14, 1, 5, 210), width=max(2, int(2.5 * geom.scale)))
        draw.ellipse((icx - cr, icy - cr, icx + cr, icy + cr), outline=(*c_acc, 195), width=1)
        step_deg = 8 if ch_idx % 2 == 0 else 12
        for deg in range(0, 360, step_deg):
            rad = math.radians(deg)
            nw = 4.0 * geom.scale
            nx1 = icx + (cr - nw) * math.cos(rad)
            ny1 = icy + (cr - nw) * math.sin(rad)
            nx2 = icx + (cr + nw) * math.cos(rad)
            ny2 = icy + (cr + nw) * math.sin(rad)
            draw.line((nx1, ny1, nx2, ny2), fill=(255, 235, 245, 210), width=1)

    for r_idx, r_frac in enumerate(channel_fracs):
        rad = r_iris * r_frac
        fsize = max(8, int((8.6 + (1.0 - r_frac) * 4.2) * geom.scale))
        is_bold = (r_idx % 2 == 0)
        theta_cur = rng.uniform(0, math.tau)
        theta_end = theta_cur + math.tau - 0.04

        while theta_cur < theta_end:
            word = generate_meaningful_quotes(rng, "short" if r_frac < 0.60 else "mixed")
            if len(word) > 20:
                word = generate_meaningful_quotes(rng, "short")
            w_px, _ = font_mgr.measure(word, fsize, bold=is_bold)
            d_theta = (w_px + 7.5 * geom.scale) / max(24.0, rad)
            theta_mid = theta_cur + d_theta * 0.5
            if theta_mid > theta_end:
                break

            wx = icx + rad * math.cos(theta_mid)
            wy = icy + rad * math.sin(theta_mid)

            deg_tangent = -math.degrees(theta_mid) - 90.0
            if 90 < (deg_tangent % 360) < 270:
                deg_tangent += 180.0

            rel_y = (wy - icy) / float(r_iris)
            if rel_y < -0.15:
                alpha = 230
                col = rng.choice(palette.iris_inner)
            else:
                alpha = 255
                col = (255, 255, 255) if is_bold else rng.choice(palette.iris_inner)

            draw_word_pil(iris_pil, font_mgr, word, wx, wy, fsize, deg_tangent, (*col, alpha), bold=is_bold)
            theta_cur += d_theta

    # =========================================================================
    # LAYER 6: SUBTLE OUTER LIMBAL RING & CIRCUMSCRIBED OUTER QUOTE RING
    # =========================================================================
    limbal_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    l_draw = ImageDraw.Draw(limbal_img)
    limbal_w = int(r_iris * 0.12)
    l_draw.ellipse(
        (icx - r_iris, icy - r_iris, icx + r_iris, icy + r_iris),
        outline=(10, 1, 4, 255),
        width=limbal_w,
    )
    r_limbal_inner = r_iris - limbal_w
    for deg in range(0, 360, 4):
        rad = math.radians(deg)
        t_len = rng.choice([8, 14, 22, 36]) * geom.scale
        x1 = icx + r_limbal_inner * math.cos(rad)
        y1 = icy + r_limbal_inner * math.sin(rad)
        x2 = icx + (r_limbal_inner - t_len) * math.cos(rad)
        y2 = icy + (r_limbal_inner - t_len) * math.sin(rad)
        l_draw.line((x1, y1, x2, y2), fill=(10, 1, 4, 235), width=max(1, int(1.8 * geom.scale)))
    limbal_img = limbal_img.filter(ImageFilter.GaussianBlur(radius=max(1.0, 1.8 * geom.scale)))
    iris_pil.alpha_composite(limbal_img)

    # Circumscribed outer limbal quote stream
    limbal_th = rng.uniform(0, math.tau)
    limbal_end = limbal_th + math.tau - 0.05
    l_fsize = max(7, int(8.2 * geom.scale))
    while limbal_th < limbal_end:
        l_word = generate_meaningful_quotes(rng, "short")
        lw_px, _ = font_mgr.measure(l_word, l_fsize)
        d_th = (lw_px + 6.0 * geom.scale) / float(r_limbal_inner)
        th_m = limbal_th + d_th * 0.5
        if th_m > limbal_end:
            break
        lx = icx + r_limbal_inner * math.cos(th_m)
        ly = icy + r_limbal_inner * math.sin(th_m)
        l_deg = -math.degrees(th_m) - 90.0
        if 90 < (l_deg % 360) < 270:
            l_deg += 180.0
        draw_word_pil(iris_pil, font_mgr, l_word, lx, ly, l_fsize, l_deg, (240, 245, 255, 175))
        limbal_th += d_th

    # Pupil cutout
    p_cut = Image.new("L", (dim, dim), 255)
    pc_draw = ImageDraw.Draw(p_cut)
    pr_clear = int(r_pupil * 0.98)
    pc_draw.ellipse((icx - pr_clear, icy - pr_clear, icx + pr_clear, icy + pr_clear), fill=0)
    p_cut = p_cut.filter(ImageFilter.GaussianBlur(radius=max(2, int(3 * geom.scale))))
    iris_pil.putalpha(Image.composite(iris_pil.getchannel("A"), Image.new("L", (dim, dim), 0), p_cut))

    glow_pil = iris_pil.filter(ImageFilter.GaussianBlur(radius=max(4, int(15 * geom.scale))))

    # =========================================================================
    # THE ALIVE, INFINITE PUPIL (Deep Abyss Void + Distant Signals + Celestial Core)
    # =========================================================================
    pupil_dim = int(r_pupil * 2.5)
    if pupil_dim % 2 == 1:
        pupil_dim += 1
    pcx, pcy = pupil_dim // 2, pupil_dim // 2
    pupil_pil = Image.new("RGBA", (pupil_dim, pupil_dim), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(pupil_pil)

    # Velvety obsidian void
    p_draw.ellipse((pcx - r_pupil, pcy - r_pupil, pcx + r_pupil, pcy + r_pupil), fill=(2, 1, 5, 255))
    p_draw.ellipse((pcx - r_pupil, pcy - r_pupil, pcx + r_pupil, pcy + r_pupil), outline=(*c_acc, 255), width=max(2, int(3 * geom.scale)))
    p_draw.ellipse((pcx - r_pupil - 2, pcy - r_pupil - 2, pcx + r_pupil + 2, pcy + r_pupil + 2), outline=(255, 120, 160, 175), width=max(1, int(2 * geom.scale)))

    for p_frac in (0.78, 0.60, 0.44, 0.28):
        pr = int(r_pupil * p_frac)
        p_draw.ellipse((pcx - pr, pcy - pr, pcx + pr, pcy + pr), outline=(38, 4, 14, 215), width=1)
        for p_deg in range(0, 360, 24):
            rad = math.radians(p_deg)
            p_draw.ellipse((pcx + pr * math.cos(rad) - 1, pcy + pr * math.sin(rad) - 1,
                            pcx + pr * math.cos(rad) + 1, pcy + pr * math.sin(rad) + 1),
                           fill=(*c_acc, 200))
        th_cur = rng.uniform(0, math.tau)
        th_end = th_cur + math.tau - 0.08
        fsize = max(7, int((7.8 + (1.0 - p_frac) * 1.6) * geom.scale))
        while th_cur < th_end:
            p_word = generate_meaningful_quotes(rng, "pupil")
            pw_px, _ = font_mgr.measure(p_word, fsize)
            dth = max(0.32, (pw_px + 4.0 * geom.scale) / max(10.0, pr))
            th_m = th_cur + dth * 0.5
            if th_m > th_end:
                break
            wx = pcx + pr * math.cos(th_m)
            wy = pcy + pr * math.sin(th_m)
            deg = -math.degrees(th_m) - 90.0
            if 90 < (deg % 360) < 270:
                deg += 180.0
            p_col = (min(255, c_out[0] + 60), min(255, c_out[1] + 18), min(255, c_out[2] + 28))
            draw_word_pil(pupil_pil, font_mgr, p_word, wx, wy, fsize, deg, (*p_col, 255))
            th_cur += dth

    # DISTANT SIGNAL FRAGMENTS (Faint whispers floating in the deep singularity abyss)
    for sig_idx in range(10):
        sig_word = generate_meaningful_quotes(rng, "signal")
        sig_r = int(r_pupil * rng.uniform(0.36, 0.88))
        sig_theta = rng.uniform(0, math.tau)
        sig_x = pcx + sig_r * math.cos(sig_theta)
        sig_y = pcy + sig_r * math.sin(sig_theta)
        sig_fsize = max(6, int(6.6 * geom.scale))
        sig_deg = -math.degrees(sig_theta) - 90.0
        if 90 < (sig_deg % 360) < 270:
            sig_deg += 180.0
        sig_alpha = rng.randint(70, 130)
        draw_word_pil(pupil_pil, font_mgr, sig_word, sig_x, sig_y, sig_fsize, sig_deg, (215, 65, 110, sig_alpha))

    # =========================================================================
    # FRACTAL RECURSIVE CELESTIAL EYE MOTIF (Deepest layer of consciousness)
    # =========================================================================
    r_nebula = int(r_pupil * 0.22)
    p_draw.ellipse((pcx - r_nebula, pcy - r_nebula, pcx + r_nebula, pcy + r_nebula), outline=(180, 35, 75, 140), width=1)
    for rec_deg in range(0, 360, 15):
        r_rad = math.radians(rec_deg)
        rx1 = pcx + int(r_nebula * 0.35 * math.cos(r_rad))
        ry1 = pcy + int(r_nebula * 0.35 * math.sin(r_rad))
        rx2 = pcx + int(r_nebula * 0.95 * math.cos(r_rad))
        ry2 = pcy + int(r_nebula * 0.95 * math.sin(r_rad))
        p_draw.line((rx1, ry1, rx2, ry2), fill=(*c_acc, 130), width=1)
    r_core = max(2, int(r_nebula * 0.32))
    p_draw.ellipse((pcx - r_core, pcy - r_core, pcx + r_core, pcy + r_core), fill=(1, 0, 3, 255))
    p_draw.ellipse((pcx - 1, pcy - 1, pcx + 1, pcy + 1), fill=(255, 255, 255, 255))

    sing_word = rng.choice(["singularity", "consciousness", "eternity", "infinite void", "look within"])
    draw_word_pil(pupil_pil, font_mgr, sing_word, pcx, pcy - int(r_pupil * 0.09), max(8, int(9.6 * geom.scale)), 0.0, (*c_acc, 255), bold=True)
    rec_word = "the observer and the observed are one"
    draw_word_pil(pupil_pil, font_mgr, rec_word, pcx, pcy + int(r_pupil * 0.09), max(6, int(7.0 * geom.scale)), 0.0, (255, 215, 235, 185))

    # =========================================================================
    # TRANSLUCENT VOLUMETRIC CORNEAL HIGHLIGHTS & REFLECTED WORDS
    # =========================================================================
    hl_pil = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    ir = r_iris

    glow_refract = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    gr_draw = ImageDraw.Draw(glow_refract)
    g_cx = icx - int(ir * 0.45)
    g_cy = icy + int(ir * 0.50)
    g_rx = int(ir * 0.42)
    g_ry = int(ir * 0.28)

    for r in range(g_rx, 0, -3):
        t = r / float(g_rx)
        alpha = int(140 * (1.0 - t) ** 2.0)
        col = (
            int(255 * (1.0 - 0.2 * t)),
            int(110 * (1.0 - t) + 30 * t),
            int(160 * (1.0 - t) + 70 * t),
            alpha,
        )
        ry_cur = int(r * (g_ry / float(g_rx)))
        gr_draw.ellipse((g_cx - r, g_cy - ry_cur, g_cx + r, g_cy + ry_cur), fill=col)

    glow_refract = glow_refract.filter(ImageFilter.GaussianBlur(radius=max(4, int(16 * geom.scale))))
    hl_pil.alpha_composite(glow_refract)

    # Soft translucent facet
    facet_img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(facet_img)
    p1 = (icx - int(ir * 0.78), icy + int(ir * 0.28))
    p2 = (icx - int(ir * 0.26), icy + int(ir * 0.76))
    p3 = (icx - int(ir * 0.42), icy + int(ir * 0.84))
    p4 = (icx - int(ir * 0.84), icy + int(ir * 0.42))
    f_draw.polygon([p1, p2, p3, p4], fill=(255, 235, 245, 70))
    facet_img = facet_img.filter(ImageFilter.GaussianBlur(radius=max(2, int(4 * geom.scale))))
    hl_pil.alpha_composite(facet_img)

    hl_draw = ImageDraw.Draw(hl_pil)
    hl_draw.line(
        (icx - int(ir * 0.86), icy + int(ir * 0.36), icx - int(ir * 0.28), icy + int(ir * 0.82)),
        fill=(255, 240, 250, 160),
        width=max(1, int(1.8 * geom.scale)),
    )
    hl_draw.line(
        (icx - int(ir * 0.76), icy + int(ir * 0.22), icx - int(ir * 0.36), icy + int(ir * 0.72)),
        fill=(255, 210, 235, 120),
        width=1,
    )

    g_quote = "light remembers where it has been"
    draw_word_pil(
        hl_pil, font_mgr, g_quote,
        icx - int(ir * 0.50), icy + int(ir * 0.56),
        max(8, int(10.0 * geom.scale)), -40.0, (255, 245, 250, 220), bold=True,
    )

    # Upper corneal rim reflection with inverted reflected philosophy
    ref_quote = "memory is light traveling through thought"
    draw_word_pil(
        hl_pil, font_mgr, ref_quote,
        icx + int(ir * 0.36), icy - int(ir * 0.52),
        max(7, int(8.2 * geom.scale)), 22.0, (255, 235, 245, 110),
    )

    # Corneal catchlight bead
    cp_x = icx - int(r_pupil * 0.80)
    cp_y = icy - int(r_pupil * 0.52)
    b_rad = int(8 * geom.scale)
    hl_draw.ellipse((cp_x - b_rad * 2, cp_y - b_rad * 2, cp_x + b_rad * 2, cp_y + b_rad * 2), fill=(*c_acc, 65))
    hl_draw.ellipse((cp_x - int(b_rad * 1.3), cp_y - int(b_rad * 1.3), cp_x + int(b_rad * 1.3), cp_y + int(b_rad * 1.3)), fill=(255, 180, 210, 140))
    hl_draw.ellipse((cp_x - b_rad, cp_y - b_rad, cp_x + b_rad, cp_y + b_rad), fill=(255, 255, 255, 245))

    # Curved corneal rim reflection along upper-right margin
    rim_pts = []
    for arc_deg in range(-65, -8, 2):
        arc_rad = math.radians(arc_deg)
        ax = icx + int(ir * 0.84 * math.cos(arc_rad))
        ay = icy + int(ir * 0.84 * math.sin(arc_rad))
        rim_pts.append((ax, ay))
    if len(rim_pts) >= 2:
        hl_draw.line(rim_pts, fill=(255, 235, 245, 150), width=max(2, int(3 * geom.scale)))

    mask_iris_disc = Image.new("L", (dim, dim), 0)
    mi_draw = ImageDraw.Draw(mask_iris_disc)
    mi_draw.ellipse(
        (icx - int(r_iris * 0.93), icy - int(r_iris * 0.93),
         icx + int(r_iris * 0.93), icy + int(r_iris * 0.93)),
        fill=255,
    )
    hl_pil.putalpha(Image.composite(hl_pil.getchannel("A"), Image.new("L", (dim, dim), 0), mask_iris_disc))

    return {
        "iris": pil_to_pygame(iris_pil),
        "glow": pil_to_pygame(glow_pil),
        "pupil": pil_to_pygame(pupil_pil),
        "highlights": pil_to_pygame(hl_pil),
        "rings_a": pil_to_pygame(iris_pil),
        "rings_b": pil_to_pygame(iris_pil),
        "radial_a": pil_to_pygame(iris_pil),
        "radial_b": pil_to_pygame(iris_pil),
    }


# ============================================================================
# 7. CREATING ANIMATED EYELIDS, ANIME EYELASHES AND BLINK MASKS
# ============================================================================

@dataclass
class EyelidRimWord:
    """A single crisp word or eyelash blade along the moving upper or lower eyelid rim."""
    u: float
    v_offset: float
    is_upper: bool
    surfaces: List[pygame.Surface]  # [closed_angle_surf, mid_angle_surf, open_angle_surf]


def create_anime_lash_sprite(
    font_mgr: FontManager,
    length: float,
    base_w: float,
    angle_deg: float,
    is_upper: bool,
    tip_glow_col: Optional[Tuple[int, int, int]],
    quote_text: str,
    geom: EyeCanvasGeometry,
    sweep_dir: float = 1.0,
) -> pygame.Surface:
    """Create a single sharp, tapered curved anime eyelash blade with optional glowing tip."""
    pad = max(8, int(12 * geom.scale))
    sw = int(abs(length) * 1.5 + base_w * 2.0 + pad * 2)
    sh = int(abs(length) * 1.4 + base_w * 2.0 + pad * 2)
    sw = max(24, sw)
    sh = max(24, sh)
    cx_s = sw // 2
    cy_s = sh // 2

    lash_pil = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    l_draw = ImageDraw.Draw(lash_pil)

    root_x = float(cx_s)
    root_y = float(cy_s)
    dy = -length if is_upper else length
    dx = sweep_dir * length * 0.38
    tip_x = root_x + dx
    tip_y = root_y + dy
    ctrl_x = root_x + dx * 0.40
    ctrl_y = root_y + dy * 0.45

    blade_pts = [
        (root_x - base_w * 0.5, root_y),
        (ctrl_x - base_w * 0.28, ctrl_y),
        (tip_x, tip_y),
        (ctrl_x + base_w * 0.28, ctrl_y),
        (root_x + base_w * 0.5, root_y),
    ]
    # Deep obsidian blade body
    l_draw.polygon(blade_pts, fill=(2, 1, 6, 255))
    l_draw.line(
        [(root_x - base_w * 0.5, root_y), (ctrl_x - base_w * 0.28, ctrl_y), (tip_x, tip_y)],
        fill=(55, 12, 22, 210),
        width=1,
    )

    # Glowing tip ember spark (matching red petal/ember highlights in reference!)
    if tip_glow_col is not None:
        tr = max(2, int(3.2 * geom.scale))
        l_draw.ellipse(
            (tip_x - tr * 1.8, tip_y - tr * 1.8, tip_x + tr * 1.8, tip_y + tr * 1.8),
            fill=(*tip_glow_col, 110),
        )
        l_draw.ellipse(
            (tip_x - tr, tip_y - tr, tip_x + tr, tip_y + tr),
            fill=(*tip_glow_col, 245),
        )
        l_draw.ellipse(
            (tip_x - tr * 0.4, tip_y - tr * 0.4, tip_x + tr * 0.4, tip_y + tr * 0.4),
            fill=(255, 255, 255, 255),
        )

    # Real micro-quote etched along the spine of the lash blade
    if quote_text and length > 45 * geom.scale:
        fsize = max(7, int(8.2 * geom.scale))
        blade_ang = -math.degrees(math.atan2(tip_y - root_y, tip_x - root_x))
        if 90 < (blade_ang % 360) < 270:
            blade_ang += 180.0
        draw_word_pil(
            lash_pil, font_mgr, quote_text,
            (root_x + tip_x) * 0.5, (root_y + tip_y) * 0.5,
            fsize, blade_ang, (190, 28, 55, 220), bold=True
        )

    if abs(angle_deg) > 0.45:
        lash_pil = lash_pil.rotate(angle_deg, resample=Image.BICUBIC, expand=True)

    return pil_to_pygame(lash_pil)


def create_animated_eyelids_and_masks(
    geom: EyeCanvasGeometry,
    font_mgr: FontManager,
    palette: TypographyPalette,
    rng: random.Random,
) -> List[EyelidRimWord]:
    """
    Create dramatic anime eyelashes (sweeping dagger blades, wing lashes, glowing ember tips)
    and clean non-overlapping eyelid rim streams that travel along the moving eyelid edges.
    """
    rim_words: List[EyelidRimWord] = []

    u_grid = np.linspace(-1.02, 1.02, 160)
    dx_grid = (u_grid[1] - u_grid[0]) * geom.eye_half_w
    yu_open, yl_open = eval_eyelid_curves(u_grid, 1.0, geom)
    yu_mid, yl_mid = eval_eyelid_curves(u_grid, 0.45, geom)
    yu_closed, yl_closed = eval_eyelid_curves(u_grid, 0.0, geom)

    slope_u_open = np.gradient(yu_open, dx_grid)
    slope_u_mid = np.gradient(yu_mid, dx_grid)
    slope_u_closed = np.gradient(yu_closed, dx_grid)

    slope_l_open = np.gradient(yl_open, dx_grid)
    slope_l_mid = np.gradient(yl_mid, dx_grid)
    slope_l_closed = np.gradient(yl_closed, dx_grid)

    # 1. DRAMATIC UPPER ANIME EYELASH DAGGER BLADES (24 sweeping curved blades)
    for idx, u_val in enumerate(np.linspace(-0.92, 0.92, 24)):
        g_idx = int(np.clip(((u_val + 1.02) / 2.04) * (len(u_grid) - 1), 0, len(u_grid) - 1))
        ang_o = -math.degrees(math.atan(float(slope_u_open[g_idx])))
        ang_m = -math.degrees(math.atan(float(slope_u_mid[g_idx])))
        ang_c = -math.degrees(math.atan(float(slope_u_closed[g_idx])))

        # Length sweeps longer towards lateral (right) wing lash
        rel_wing = (u_val + 1.0) * 0.5
        lash_len = (32.0 + 75.0 * (rel_wing ** 1.35)) * geom.scale
        base_w = (7.0 + 9.0 * (rel_wing ** 1.2)) * geom.scale
        sweep = 1.0 if u_val > -0.25 else -1.0
        has_glow = (idx % 3 == 0) or (u_val > 0.55)
        glow_col = palette.ember_color if has_glow else None

        micro_q = generate_meaningful_quotes(rng, "short") if lash_len > 48 * geom.scale else ""
        surfs = [
            create_anime_lash_sprite(font_mgr, lash_len, base_w, ang_c, True, glow_col, micro_q, geom, sweep),
            create_anime_lash_sprite(font_mgr, lash_len, base_w, ang_m, True, glow_col, micro_q, geom, sweep),
            create_anime_lash_sprite(font_mgr, lash_len, base_w, ang_o, True, glow_col, micro_q, geom, sweep),
        ]
        rim_words.append(
            EyelidRimWord(
                u=float(u_val),
                v_offset=0.0,
                is_upper=True,
                surfaces=surfs,
            )
        )

    # 2. DRAMATIC LOWER ANIME NEEDLE LASHES (16 delicate needle spikes)
    for idx, u_val in enumerate(np.linspace(-0.84, 0.84, 16)):
        g_idx = int(np.clip(((u_val + 1.02) / 2.04) * (len(u_grid) - 1), 0, len(u_grid) - 1))
        ang_o = -math.degrees(math.atan(float(slope_l_open[g_idx])))
        ang_m = -math.degrees(math.atan(float(slope_l_mid[g_idx])))
        ang_c = -math.degrees(math.atan(float(slope_l_closed[g_idx])))

        lash_len = (20.0 + 26.0 * (abs(u_val) ** 1.3)) * geom.scale
        base_w = (4.0 + 4.5 * abs(u_val)) * geom.scale
        sweep = 1.0 if u_val >= 0 else -1.0
        surfs = [
            create_anime_lash_sprite(font_mgr, lash_len, base_w, ang_c, False, None, "", geom, sweep),
            create_anime_lash_sprite(font_mgr, lash_len, base_w, ang_m, False, None, "", geom, sweep),
            create_anime_lash_sprite(font_mgr, lash_len, base_w, ang_o, False, None, "", geom, sweep),
        ]
        rim_words.append(
            EyelidRimWord(
                u=float(u_val),
                v_offset=0.0,
                is_upper=False,
                surfaces=surfs,
            )
        )

    # 3. EYELID RIM WORD STREAMS (Fine glowing quotes along the eyelid margin)
    def build_clean_rim_stream(is_upper: bool, v_off: float, fsize: int) -> None:
        u_cur = -0.98 + rng.uniform(0.0, 0.02)
        while u_cur < 0.98:
            phrase = generate_meaningful_quotes(rng, "short" if abs(u_cur) > 0.65 else "mixed")
            if len(phrase) > 22:
                phrase = generate_meaningful_quotes(rng, "short")
            w_px, _ = font_mgr.measure(phrase, fsize, bold=True)

            idx_est = int(np.clip(((u_cur + 1.02) / 2.04) * (len(u_grid) - 1), 0, len(u_grid) - 1))
            local_slope = float(slope_u_open[idx_est] if is_upper else slope_l_open[idx_est])
            cos_theta = 1.0 / math.sqrt(1.0 + local_slope * local_slope)
            du = ((w_px + 12.0 * geom.scale) * max(0.65, cos_theta)) / geom.eye_half_w
            u_mid = u_cur + du * 0.5
            if u_mid > 0.98:
                break

            idx = int(np.clip(((u_mid + 1.02) / 2.04) * (len(u_grid) - 1), 0, len(u_grid) - 1))
            if is_upper:
                ang_open = -math.degrees(math.atan(float(slope_u_open[idx])))
                ang_mid = -math.degrees(math.atan(float(slope_u_mid[idx])))
                ang_closed = -math.degrees(math.atan(float(slope_u_closed[idx])))
            else:
                ang_open = -math.degrees(math.atan(float(slope_l_open[idx])))
                ang_mid = -math.degrees(math.atan(float(slope_l_mid[idx])))
                ang_closed = -math.degrees(math.atan(float(slope_l_closed[idx])))

            col = rng.choice(palette.eyelid_rim)
            edge_atten = max(0.45, 1.0 - 0.50 * (abs(u_mid) ** 2.4))
            alpha = int(250 * edge_atten)

            surfs = [
                create_word_sprite(font_mgr, phrase, fsize, ang_closed, (*col, alpha), bold=True),
                create_word_sprite(font_mgr, phrase, fsize, ang_mid, (*col, alpha), bold=True),
                create_word_sprite(font_mgr, phrase, fsize, ang_open, (*col, alpha), bold=True),
            ]
            rim_words.append(
                EyelidRimWord(
                    u=u_mid,
                    v_offset=v_off,
                    is_upper=is_upper,
                    surfaces=surfs,
                )
            )
            u_cur += du

    build_clean_rim_stream(True, -10.0 * geom.scale, max(10, int(12.2 * geom.scale)))
    build_clean_rim_stream(False, +10.0 * geom.scale, max(10, int(11.6 * geom.scale)))

    return rim_words


def create_shaded_particle_sprites(
    geom: EyeCanvasGeometry, palette: TypographyPalette
) -> List[Tuple[str, pygame.Surface]]:
    """
    Generate a library of realistically shaded, atmospheric anime petals and embers.
    Each sprite is shaded with directional lighting, velvety shadow falloff,
    and soft atmospheric bokeh - NO hard-edged neon balls!
    """
    sprites = []
    c_acc = palette.accent_tint
    c_out = palette.iris_outer[0]
    c_mid = palette.iris_mid[0]
    c_emb = palette.ember_color

    # 0 = Small realistic ember spark: smooth glowing core with natural inverse-square falloff
    dim = max(24, int(32 * geom.scale))
    img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = dim // 2, dim // 2
    r_max = dim // 2 - 2
    for r in range(r_max, 0, -1):
        t = r / float(r_max)
        alpha = int(140 * (1.0 - t) ** 1.8)
        red = int(c_emb[0] * (1.0 - 0.25 * t) + 255 * (0.25 * (1.0 - t)))
        green = int(c_emb[1] * (1.0 - t) + 110 * (1.0 - t) ** 2)
        blue = int(c_emb[2] * (1.0 - t) + 140 * (1.0 - t) ** 2)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(red, green, blue, alpha))
    sprites.append(("spark", pil_to_pygame(img)))

    # 1 = Crisp drifting petal: elegant curved petal with 3D directional light & shadow
    dim = max(32, int(46 * geom.scale))
    img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w2 = dim // 2
    pts = [
        (w2, int(dim * 0.12)),
        (int(dim * 0.72), int(dim * 0.38)),
        (int(dim * 0.65), int(dim * 0.76)),
        (w2, int(dim * 0.88)),
        (int(dim * 0.35), int(dim * 0.76)),
        (int(dim * 0.28), int(dim * 0.38)),
    ]
    draw.polygon(pts, fill=(c_out[0] + 30, c_out[1] + 5, c_out[2] + 10, 225))
    hl_pts = [
        (w2, int(dim * 0.12)),
        (int(dim * 0.72), int(dim * 0.38)),
        (int(dim * 0.65), int(dim * 0.76)),
        (int(dim * 0.52), int(dim * 0.80)),
        (w2, int(dim * 0.42)),
    ]
    draw.polygon(hl_pts, fill=(c_mid[0], c_mid[1] + 10, c_mid[2] + 25, 205))
    draw.line([(w2, int(dim * 0.12)), (int(dim * 0.72), int(dim * 0.38)), (int(dim * 0.65), int(dim * 0.76))],
              fill=(255, 185, 210, 185), width=max(1, int(1.2 * geom.scale)))
    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    sprites.append(("petal_crisp", pil_to_pygame(img)))

    # 2 = Large soft bokeh petal (smooth out-of-focus atmospheric blur)
    dim = max(48, int(68 * geom.scale))
    img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = dim // 2, dim // 2
    r_max = dim // 2 - 4
    for r in range(r_max, 0, -2):
        t = r / float(r_max)
        alpha = int(90 * (1.0 - t) ** 1.4)
        col = (
            int(c_mid[0] * (1.0 - 0.4 * t)),
            int(c_mid[1] * (1.0 - 0.4 * t)),
            int(c_mid[2] * (1.0 - 0.4 * t)),
            alpha
        )
        draw.ellipse((cx - int(r * 1.3), cy - r, cx + int(r * 1.3), cy + r), fill=col)
    img = img.filter(ImageFilter.GaussianBlur(radius=max(2.5, 3.5 * geom.scale)))
    sprites.append(("petal_bokeh", pil_to_pygame(img)))

    # 3 = Micro luminous dust mote
    dim = max(12, int(16 * geom.scale))
    img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = dim // 2, dim // 2
    draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(*c_acc, 160))
    draw.ellipse((cx - 1, cy - 1, cx + 1, cy + 1), fill=(255, 240, 245, 220))
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    sprites.append(("micro_mote", pil_to_pygame(img)))

    return sprites


class BlinkController:
    """
    Natural biological blink controller (every 3-6 seconds with occasional double blinks).
    """

    def __init__(self) -> None:
        self.auto_blink: bool = True
        self.is_blinking: bool = False
        self.blink_start: float = 0.0
        self.close_dur: float = 0.125
        self.hold_dur: float = 0.045
        self.open_dur: float = 0.225
        self.queued_double: bool = False
        self.next_blink_time: float = time.perf_counter() + random.uniform(2.5, 4.5)

    def trigger_blink(self, now: Optional[float] = None, allow_double: bool = True) -> None:
        if now is None:
            now = time.perf_counter()
        self.is_blinking = True
        self.blink_start = now
        self.close_dur = random.uniform(0.115, 0.140)
        self.hold_dur = random.uniform(0.038, 0.058)
        self.open_dur = random.uniform(0.200, 0.260)
        self.queued_double = allow_double and (random.random() < 0.24)
        self.next_blink_time = now + random.uniform(3.0, 6.0)

    def update(self, now: float) -> float:
        if self.auto_blink and not self.is_blinking and now >= self.next_blink_time:
            self.trigger_blink(now, allow_double=True)

        if not self.is_blinking:
            return 1.0

        elapsed = now - self.blink_start
        total = self.close_dur + self.hold_dur + self.open_dur

        if elapsed < 0.0:
            return 1.0
        if elapsed < self.close_dur:
            u = elapsed / self.close_dur
            ease = 3.0 * (u ** 2) - 2.0 * (u ** 3)
            return max(0.0, 1.0 - ease)
        elif elapsed < self.close_dur + self.hold_dur:
            return 0.0
        elif elapsed < total:
            u = (elapsed - self.close_dur - self.hold_dur) / self.open_dur
            ease = 1.0 - (1.0 - u) ** 2.6
            return min(1.0, ease)
        else:
            if self.queued_double:
                self.queued_double = False
                self.trigger_blink(now + 0.045, allow_double=False)
            else:
                self.is_blinking = False
            return 1.0


# ============================================================================
# 8. MANAGING CINEMATIC ZOOM AND CAMERA MOVEMENT
# ============================================================================

# ============================================================================
# 8. MANAGING CINEMATIC ZOOM AND CAMERA MOVEMENT
# ============================================================================

class CinematicCamera:
    """
    Manages continuous, smooth camera zoom and gentle panning between:
      - Wide View (zoom = 1.0): The entire giant eye emerges from the edge-to-edge wall of typography.
      - Close-Up View (zoom up to 2.55x): Zooms deeply into the typography to reveal
        individual readable quotes and words without ever exposing blank edges.
    Features:
      - Cognitive Gaze Delay: ~240ms biological latency before tracking mouse movement,
        preventing robotic cursor chasing and creating authentic sentient personality.
      - Smooth biological saccadic easing and micro-accommodation pulse.
    """

    def __init__(self) -> None:
        self.auto_zoom: bool = True
        self.zoom: float = 1.0
        self.phase: float = 0.0
        self.pan_x: float = 0.0
        self.pan_y: float = 0.0
        self.gaze_x: float = 0.0
        self.gaze_y: float = 0.0
        self.target_gx: float = 0.0
        self.target_gy: float = 0.0
        self.last_mouse_pos: Tuple[int, int] = (-999, -999)
        self.last_mouse_move_time: float = time.perf_counter()
        self.attention_engaged: bool = False
        self.accommodation_pulse: float = 0.0  # pupil focus pulse when gaze locks
        self.viewer_attentiveness: float = 0.5  # observer interaction energy

    def manage_zoom_and_camera(
        self,
        geom: EyeCanvasGeometry,
        now: float,
        dt: float,
        override_zoom: Optional[float] = None,
        freeze_camera: bool = False,
    ) -> Tuple[pygame.Rect, float, float]:
        if freeze_camera:
            # During "Impossible Moment" or special focus, lock gaze dead-center on viewer
            self.gaze_x += (0.0 - self.gaze_x) * min(1.0, dt * 6.0)
            self.gaze_y += (0.0 - self.gaze_y) * min(1.0, dt * 6.0)
            base_vw = geom.canvas_w * 0.82
            base_vh = geom.canvas_h * 0.82
            cur_z = override_zoom if override_zoom is not None else self.zoom
            view_w = int(round(base_vw / cur_z))
            view_h = int(round(base_vh / cur_z))
            left = max(0, min(geom.canvas_w - view_w, geom.center_x - view_w // 2))
            top = max(0, min(geom.canvas_h - view_h, geom.center_y - view_h // 2))
            return pygame.Rect(left, top, view_w, view_h), self.gaze_x, self.gaze_y

        mx, my = pygame.mouse.get_pos()
        dist_m = math.hypot(mx - self.last_mouse_pos[0], my - self.last_mouse_pos[1])
        if dist_m > 1.2:
            self.last_mouse_pos = (mx, my)
            self.last_mouse_move_time = now
            self.attention_engaged = True
            self.viewer_attentiveness = min(1.0, self.viewer_attentiveness + dt * 2.5)
        else:
            self.viewer_attentiveness = max(0.0, self.viewer_attentiveness - dt * 0.15)

        # Natural, expressive ocular travel range across the eye socket
        # Scaled directly to the biological anatomy of the eye opening
        max_gx = geom.eye_half_w * 0.22
        max_gy = geom.eye_half_h * 0.20

        # Check if cursor is inside window or was recently active
        is_focused = pygame.mouse.get_focused() if hasattr(pygame.mouse, "get_focused") else True
        time_since_move = now - self.last_mouse_move_time

        if (time_since_move < 16.0 or self.attention_engaged) and is_focused:
            # Map mouse window position to normalized coordinates [-1.0, 1.0]
            nx = (mx - geom.screen_w * 0.5) / max(1.0, geom.screen_w * 0.5)
            ny = (my - geom.screen_h * 0.5) / max(1.0, geom.screen_h * 0.5)
            nx = float(np.clip(nx, -1.0, 1.0))
            ny = float(np.clip(ny, -1.0, 1.0))

            # Non-linear sensitivity: sensitive and responsive near center, smooth near periphery
            eased_nx = math.copysign(abs(nx) ** 0.86, nx)
            eased_ny = math.copysign(abs(ny) ** 0.86, ny)

            # Subtle living micro-tremor (living ocular muscle fixation)
            micro_x = (math.sin(now * 5.7) * 1.5 + math.sin(now * 11.3) * 0.7) * geom.scale
            micro_y = (math.cos(now * 4.9) * 1.2 + math.cos(now * 9.7) * 0.5) * geom.scale

            self.target_gx = eased_nx * max_gx + micro_x
            self.target_gy = eased_ny * max_gy + micro_y
            self.accommodation_pulse = min(1.0, self.accommodation_pulse + dt * 4.0)
        else:
            self.attention_engaged = False
            # Autonomous meditative wandering gaze (gentle Lissajous curves) when idle for 16+ seconds
            self.target_gx = math.sin(now * 0.45) * math.cos(now * 0.21) * (max_gx * 0.45)
            self.target_gy = math.sin(now * 0.32 + 1.1) * (max_gy * 0.40)
            self.accommodation_pulse = max(0.0, self.accommodation_pulse - dt * 2.0)

        # Smooth biological S-curve easing: fast, decisive ocular movement (~110ms) with mass
        smooth = min(1.0, dt * 8.5)
        self.gaze_x += (self.target_gx - self.gaze_x) * smooth
        self.gaze_y += (self.target_gy - self.gaze_y) * smooth

        if override_zoom is not None:
            self.zoom = override_zoom
        elif self.auto_zoom:
            speed_mod = 0.30 + 0.06 * math.sin(now * 0.15)
            self.phase += dt * speed_mod
            raw_wave = 0.5 - 0.5 * math.cos(self.phase)
            eased = raw_wave * raw_wave * (3.0 - 2.0 * raw_wave)
            self.zoom = 1.0 + eased * 1.55
        else:
            self.zoom += (1.0 - self.zoom) * min(1.0, dt * 4.0)

        base_vw = geom.canvas_w * 0.82
        base_vh = geom.canvas_h * 0.82

        view_w = int(round(base_vw / self.zoom))
        view_h = int(round(base_vh / self.zoom))
        view_w = max(320, min(geom.canvas_w, view_w))
        view_h = max(200, min(geom.canvas_h, view_h))

        zoom_factor = (self.zoom - 1.0) / 1.55
        drift_radius_x = geom.eye_half_w * 0.30 * zoom_factor
        drift_radius_y = geom.eye_half_h * 0.25 * zoom_factor

        # Camera viewport only follows subtly when zoomed in (never cancels out the eyeball's on-screen travel)
        target_px = math.sin(now * 0.23) * drift_radius_x + self.gaze_x * 0.25 * zoom_factor
        target_py = math.cos(now * 0.19) * drift_radius_y + self.gaze_y * 0.25 * zoom_factor
        self.pan_x += (target_px - self.pan_x) * min(1.0, dt * 3.5)
        self.pan_y += (target_py - self.pan_y) * min(1.0, dt * 3.5)

        cam_cx = int(round(geom.center_x + self.pan_x))
        cam_cy = int(round(geom.center_y + self.pan_y))

        left = max(0, min(geom.canvas_w - view_w, cam_cx - view_w // 2))
        top = max(0, min(geom.canvas_h - view_h, cam_cy - view_h // 2))

        return pygame.Rect(left, top, view_w, view_h), self.gaze_x, self.gaze_y


# ============================================================================
# 8.5 CONSCIOUSNESS ENGINE (Internal Cognitive State & Emotional Cycles)
# ============================================================================

class MindState:
    AWARENESS = "Awareness"     # Crimson / ruby, vigilant, rhythmic breathing
    CURIOSITY = "Curiosity"     # Magenta / rose, searching gaze, pupil expands
    DREAMING  = "Dreaming"      # Violet / amethyst, slow breathing, heavy eyelids
    SILENCE   = "Silence"       # Near-black monochrome, text dims to 15%, solitary thought
    CLARITY   = "Clarity"       # Luminous warm gold / white, razor sharp contrast


class ConsciousnessEngine:
    """
    Simulates an internal nervous system and cognitive state for the living eye.
    Drives continuous, non-repeating variations in:
      - Pupil dilation & thought micro-tremors
      - Iris fiber radiance & breathing cycles
      - Text field presence (from solitary thought in silence to full illumination)
      - Emotional color moods and saturation shifts
      - Visual breathing room and color draining/re-ignition
      - The 'Impossible Moment' 9-Phase sacred journey (13.5s)
    """

    def __init__(self) -> None:
        self.state: str = MindState.AWARENESS
        self.state_start: float = time.perf_counter()
        self.state_duration: float = random.uniform(22.0, 34.0)
        self.cycle = [
            MindState.AWARENESS,
            MindState.CURIOSITY,
            MindState.SILENCE,
            MindState.CLARITY,
            MindState.DREAMING,
        ]
        self.cycle_idx: int = 0

        # Dynamic thought modulations
        self.pupil_dilation: float = 1.0
        self.iris_luminance: float = 1.0
        self.text_dimming: float = 1.0
        self.color_drain: float = 0.0  # 0.0 = full color, 1.0 = monochrome silence
        self.solitary_thought: str = random.choice(SOLITARY_THOUGHTS)

        # The Impossible Moment (9-Phase Sacred Journey)
        self.impossible_active: bool = False
        self.impossible_start: float = 0.0
        self.impossible_dur: float = 13.5
        self.next_impossible_time: float = time.perf_counter() + random.uniform(80.0, 125.0)
        self.revelation_text: str = random.choice(HIDDEN_REVELATIONS)

    def trigger_impossible_moment(self, now: float) -> None:
        self.impossible_active = True
        self.impossible_start = now
        self.revelation_text = random.choice(HIDDEN_REVELATIONS)
        self.next_impossible_time = now + random.uniform(90.0, 140.0)

    def update(self, now: float, dt: float) -> None:
        # Check automatic Impossible Moment
        if not self.impossible_active and now >= self.next_impossible_time:
            self.trigger_impossible_moment(now)

        if self.impossible_active:
            imp_t = now - self.impossible_start
            if imp_t >= self.impossible_dur:
                self.impossible_active = False
            return

        # Advance Mind State cycle
        elapsed = now - self.state_start
        if elapsed >= self.state_duration:
            self.cycle_idx = (self.cycle_idx + 1) % len(self.cycle)
            self.state = self.cycle[self.cycle_idx]
            self.state_start = now
            self.state_duration = random.uniform(20.0, 36.0)
            self.solitary_thought = random.choice(SOLITARY_THOUGHTS)

        # Target parameters based on current Mind State
        target_dilation = 1.0
        target_luminance = 1.0
        target_text_dim = 1.0
        target_drain = 0.0

        if self.state == MindState.AWARENESS:
            target_dilation = 1.0 + 0.03 * math.sin(now * 1.2)
            target_luminance = 1.05
            target_text_dim = 1.0
            target_drain = 0.0
        elif self.state == MindState.CURIOSITY:
            target_dilation = 1.14 + 0.04 * math.sin(now * 0.9)
            target_luminance = 1.12
            target_text_dim = 0.90
            target_drain = 0.0
        elif self.state == MindState.DREAMING:
            target_dilation = 0.92 + 0.03 * math.sin(now * 0.6)
            target_luminance = 0.88
            target_text_dim = 0.65
            target_drain = 0.25
        elif self.state == MindState.SILENCE:
            target_dilation = 0.86
            target_luminance = 0.75
            target_text_dim = 0.18
            target_drain = 0.82
        elif self.state == MindState.CLARITY:
            target_dilation = 1.05
            target_luminance = 1.25
            target_text_dim = 1.0
            target_drain = 0.0

        blend_spd = dt * 1.5
        self.pupil_dilation += (target_dilation - self.pupil_dilation) * min(1.0, blend_spd)
        self.iris_luminance += (target_luminance - self.iris_luminance) * min(1.0, blend_spd)
        self.text_dimming += (target_text_dim - self.text_dimming) * min(1.0, blend_spd)
        self.color_drain += (target_drain - self.color_drain) * min(1.0, blend_spd)


# ============================================================================
# 9. RENDERING THE FINAL FULL-SCREEN COMPOSITION
# ============================================================================

class EyeWithinWordsApp:
    """Full-screen generative typography application."""

    def __init__(
        self,
        windowed: bool = False,
        test_frames: int = 0,
        screenshot_dir: Optional[str] = None,
    ) -> None:
        pygame.display.init()

        self.windowed = windowed
        self.test_frames = test_frames
        self.screenshot_dir = screenshot_dir

        info = pygame.display.Info()
        desktop_w = info.current_w if info.current_w > 0 else 1512
        desktop_h = info.current_h if info.current_h > 0 else 982

        if not self.windowed:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            self.screen = pygame.display.set_mode((0, 0), flags)
        else:
            win_w = min(1440, int(desktop_w * 0.88))
            win_h = min(900, int(desktop_h * 0.88))
            flags = pygame.RESIZABLE | pygame.DOUBLEBUF
            self.screen = pygame.display.set_mode((win_w, win_h), flags)

        pygame.display.set_caption("THE EYE WITHIN WORDS — Generative Typography Animation")

        self.font_mgr = FontManager()
        self.palette_idx = 0
        self.seed = random.randint(10000, 999999)
        self.blink_ctrl = BlinkController()
        self.camera = CinematicCamera()
        self.consciousness = ConsciousnessEngine()
        self.show_help = False
        self.clock = pygame.time.Clock()

        # Awakening sequence controller (First Look genesis sequence: darkness -> spark -> fibers -> eye opening -> full consciousness)
        self.awakening_active: bool = (self.test_frames == 0)
        self.awakening_start: float = time.perf_counter()
        self.awakening_dur: float = 19.5

        # The Synchronized WOW Moment (Cosmic Awareness Event)
        self.wow_active: bool = False
        self.wow_start: float = 0.0
        self.wow_dur: float = 6.2
        self.next_wow_time: float = time.perf_counter() + 38.0
        self.wow_interval: float = 54.0

        # Smooth Palette Cross-Fading (Cinematic fluid color transitions)
        self.transition_active: bool = False
        self.transition_start: float = 0.0
        self.transition_dur: float = 1.8
        self.prev_full_field_surf: Optional[pygame.Surface] = None
        self.prev_iris_layers: Dict[str, pygame.Surface] = {}

        self.geom: EyeCanvasGeometry = calculate_eye_spatial_and_color_patterns(
            *self.screen.get_size()
        )
        self.full_field_surf: Optional[pygame.Surface] = None
        self.sclera_surf: Optional[pygame.Surface] = None
        self.iris_cutout_mask: Optional[pygame.Surface] = None
        self.iris_layers: Dict[str, pygame.Surface] = {}
        self.eyelid_rim_words: List[EyelidRimWord] = []

        self.virtual_frame_surf: Optional[pygame.Surface] = None
        self.eye_box_canvas: Optional[pygame.Surface] = None
        self.eye_box_mask: Optional[pygame.Surface] = None
        self.eye_box_rect: pygame.Rect = pygame.Rect(0, 0, 10, 10)
        self.mask_u = np.linspace(-1.01, 1.01, 96)
        self.particle_sprites: List[Tuple[str, pygame.Surface]] = []
        self.embers: List[Dict] = []
        self.vignette_surf: Optional[pygame.Surface] = None
        self.afterimage_surf: Optional[pygame.Surface] = None
        self.afterimage_alpha: float = 0.0
        self.thought_birth_sparks: List[Dict] = []
        self.last_thought_birth_time: float = 0.0

        self._build_all_layers()

    def _build_all_layers(self, is_crossfade: bool = False) -> None:
        """Precompute all high-resolution typography surfaces across the virtual canvas."""
        sw, sh = self.screen.get_size()
        self.geom = calculate_eye_spatial_and_color_patterns(sw, sh)
        palette = PALETTES[self.palette_idx]
        rng = random.Random(self.seed)

        (
            self.full_field_surf,
            self.sclera_surf,
            self.iris_cutout_mask,
        ) = layout_full_canvas_typography(self.geom, self.font_mgr, palette, rng)

        self.iris_layers = create_iris_and_pupil_typography(
            self.geom, self.font_mgr, palette, rng
        )
        self.eyelid_rim_words = create_animated_eyelids_and_masks(
            self.geom, self.font_mgr, palette, rng
        )

        # Precompute realistically shaded particle sprites (petals, embers, motes)
        self.particle_sprites = create_shaded_particle_sprites(self.geom, palette)

        # Initialize floating realistically shaded petals & embers particle system
        if not is_crossfade or not self.embers:
            self.embers = []
            for _ in range(58):
                spr_idx = rng.choices([0, 1, 2, 3], weights=[0.30, 0.35, 0.15, 0.20])[0]
                self.embers.append({
                    "x": rng.uniform(0, self.geom.canvas_w),
                    "y": rng.uniform(0, self.geom.canvas_h),
                    "vx": rng.uniform(-14.0, 16.0),
                    "vy": rng.uniform(18.0, 48.0),
                    "scale": rng.uniform(0.70, 1.25),
                    "angle": rng.uniform(0, 360),
                    "rot_spd": rng.uniform(-35.0, 35.0),
                    "base_alpha": rng.randint(110, 220),
                    "pulse_spd": rng.uniform(1.2, 3.2),
                    "sway_spd": rng.uniform(0.7, 2.0),
                    "sway_amp": rng.uniform(14.0, 32.0),
                    "phase": rng.uniform(0, math.tau),
                    "spr_idx": spr_idx,
                })

        # Precompute cinematic radial screen vignette
        sw, sh = self.screen.get_size()
        vig_pil = Image.new("RGBA", (sw, sh), (255, 255, 255, 255))
        v_draw = ImageDraw.Draw(vig_pil)
        diag = math.hypot(sw, sh) * 0.58
        for r_v in range(int(diag), 0, -22):
            frac = r_v / diag
            v_val = int(85 + 170 * (frac ** 0.8))
            v_draw.ellipse(
                (sw // 2 - r_v, sh // 2 - r_v, sw // 2 + r_v, sh // 2 + r_v),
                outline=(v_val, v_val, v_val, 255),
                width=24,
            )
        vig_pil = vig_pil.filter(ImageFilter.GaussianBlur(radius=max(6, int(28 * self.geom.scale))))
        self.vignette_surf = pil_to_pygame(vig_pil)

        self.virtual_frame_surf = pygame.Surface(
            (self.geom.canvas_w, self.geom.canvas_h), pygame.SRCALPHA
        )

        box_w = int(self.geom.eye_half_w * 2.25)
        box_h = int(self.geom.eye_half_h * 2.65)
        box_left = self.geom.center_x - box_w // 2
        box_top = self.geom.center_y - box_h // 2
        self.eye_box_rect = pygame.Rect(box_left, box_top, box_w, box_h)
        self.eye_box_canvas = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        self.eye_box_mask = pygame.Surface((box_w, box_h), pygame.SRCALPHA)

    def trigger_wow_moment(self, now: float) -> None:
        """Trigger the cosmic awareness synchronized WOW moment."""
        self.wow_active = True
        self.wow_start = now
        self.next_wow_time = now + self.wow_interval

    def render_fullscreen_composition(
        self,
        openness: float,
        cam_rect: pygame.Rect,
        gaze_x: float,
        gaze_y: float,
        now: float,
        dt: float,
    ) -> None:
        """
        Composite the full-canvas typography, living layered iris/pupil, and animated blink
        on the virtual canvas, then apply the camera zoom transformation to the screen.
        """
        if self.virtual_frame_surf is None or self.full_field_surf is None:
            return

        geom = self.geom
        palette = PALETTES[self.palette_idx]
        bx, by, bw, bh = self.eye_box_rect
        local_cx = geom.center_x - bx
        local_cy = geom.center_y - by

        # Update the internal Consciousness Engine
        self.consciousness.update(now, dt)

        # ---------------------------------------------------------------------
        # 0. The "First Look" Experience (18s Cinematic Genesis Sequence)
        # ---------------------------------------------------------------------
        awakening_fade = 1.0
        awakening_iris_scale = 1.0
        awakening_ember_pulse = 0.0

        if self.awakening_active:
            aw_t = now - self.awakening_start
            if aw_t >= self.awakening_dur:
                self.awakening_active = False
            else:
                if aw_t < 4.0:
                    # Phase 0: Pure darkness, faint whispers in void (15% opacity)
                    awakening_fade = max(0.04, (aw_t / 4.0) * 0.18)
                    openness = 0.03
                    awakening_iris_scale = 0.30
                    gaze_x *= 0.05
                    gaze_y *= 0.05
                elif aw_t < 8.5:
                    # Phase 1: Tiny red ember spark appears and pulses
                    u_spark = (aw_t - 4.0) / 4.5
                    awakening_fade = 0.18 + 0.22 * u_spark
                    openness = 0.04 + 0.12 * math.sin(u_spark * math.pi * 0.5)
                    awakening_iris_scale = 0.30 + 0.35 * (u_spark ** 1.5)
                    awakening_ember_pulse = math.sin(aw_t * 3.5) * 0.5 + 0.5
                    gaze_x *= 0.15
                    gaze_y *= 0.15
                elif aw_t < 13.5:
                    # Phase 2: Iris fibers construct themselves outward
                    u_fib = (aw_t - 8.5) / 5.0
                    awakening_fade = 0.40 + 0.50 * u_fib
                    openness = 0.16 + 0.45 * (u_fib ** 1.3)
                    awakening_iris_scale = 0.65 + 0.35 * u_fib
                    gaze_x *= (0.15 + 0.35 * u_fib)
                    gaze_y *= (0.15 + 0.35 * u_fib)
                elif aw_t < 17.0:
                    # Phase 3: Pupil void expands open, revealing horizons
                    u_pup = (aw_t - 13.5) / 3.5
                    awakening_fade = 0.90 + 0.10 * u_pup
                    openness = 0.61 + 0.39 * math.sin(u_pup * math.pi * 0.5)
                    awakening_iris_scale = 1.0
                    gaze_x *= (0.50 + 0.50 * u_pup)
                    gaze_y *= (0.50 + 0.50 * u_pup)
                elif aw_t < 19.5:
                    # Phase 4: First Eye Contact & First Biological Blink
                    awakening_fade = 1.0
                    openness = 1.0
                    awakening_iris_scale = 1.0
                    if 17.6 <= aw_t < 18.0:
                        self.blink_ctrl.trigger_blink(now, allow_double=False)
                else:
                    # Phase 5: Fully conscious living state
                    awakening_fade = 1.0
                    awakening_iris_scale = 1.0

        # ---------------------------------------------------------------------
        # 0.3 The "Impossible Moment" (9-Phase Sacred Journey, 13.5s total)
        # ---------------------------------------------------------------------
        impossible_freeze = False
        impossible_snap = False
        impossible_alpha_boost = 0
        impossible_pupil_mult = 1.0
        imp_phase = 0
        imp_t = 0.0

        if self.consciousness.impossible_active:
            imp_t = now - self.consciousness.impossible_start
            if imp_t < 1.8:
                # Phase 1: Silence. World decelerates, eye freezes dead-center.
                imp_phase = 1
                impossible_freeze = True
                gaze_x = 0.0
                gaze_y = 0.0
            elif imp_t < 3.2:
                # Phase 2: Focus. Pupil contracts with razor sharpness.
                imp_phase = 2
                impossible_freeze = True
                impossible_snap = True
                u_foc = (imp_t - 1.8) / 1.4
                impossible_pupil_mult = 1.0 - 0.32 * math.sin(u_foc * math.pi * 0.5)
                impossible_alpha_boost = int(90 * u_foc)
            elif imp_t < 4.5:
                # Phase 3: The World Stops. Absolute stillness.
                imp_phase = 3
                impossible_freeze = True
                impossible_snap = True
                impossible_pupil_mult = 0.68
                impossible_alpha_boost = 110
            elif imp_t < 6.5:
                # Phase 4: The Revelation. Universal sentence glows in silver above collarette.
                imp_phase = 4
                impossible_freeze = True
                impossible_snap = True
                impossible_pupil_mult = 0.68
                impossible_alpha_boost = 140
            elif imp_t < 8.0:
                # Phase 5: The Singularity Opens. Pupil dilates, revealing cosmic interior.
                imp_phase = 5
                impossible_freeze = True
                u_dil = (imp_t - 6.5) / 1.5
                impossible_pupil_mult = 0.68 + 0.58 * math.sin(u_dil * math.pi * 0.5)
                impossible_alpha_boost = int(140 * (1.0 - u_dil * 0.4))
            elif imp_t < 9.2:
                # Phase 6: Sentence Disintegration. Sentence breaks into letter particles.
                imp_phase = 6
                impossible_freeze = True
                impossible_pupil_mult = 1.26
            elif imp_t < 10.5:
                # Phase 7: Gravity of Meaning. Letter-particles spiral into pupil singularity.
                imp_phase = 7
                impossible_freeze = True
                impossible_pupil_mult = 1.26 - 0.16 * ((imp_t - 9.2) / 1.3)
            elif imp_t < 11.4:
                # Phase 8: The Cosmic Blink. Deep biological darkness.
                imp_phase = 8
                if imp_t - dt < 10.5 <= imp_t:
                    self.blink_ctrl.trigger_blink(now, allow_double=False)
                if self.afterimage_surf is None and self.eye_box_canvas is not None:
                    self.afterimage_surf = self.eye_box_canvas.copy()
                    self.afterimage_alpha = 180.0
            else:
                # Phase 9: Radiant Rebirth & Afterimage. Re-opening into refreshed world.
                imp_phase = 9

        # ---------------------------------------------------------------------
        # 0.5 The Synchronized WOW Moment Dynamics
        # ---------------------------------------------------------------------
        wow_pupil_mult = 1.0
        wow_glow_boost = 0
        wow_snap_flash = 0
        if self.wow_active:
            wow_t = now - self.wow_start
            if wow_t >= self.wow_dur:
                self.wow_active = False
            elif wow_t < 3.8:
                u_wow = wow_t / 3.8
                gaze_x *= max(0.0, 1.0 - u_wow * 1.5)
                gaze_y *= max(0.0, 1.0 - u_wow * 1.5)
                wow_pupil_mult = 1.0 + 0.28 * math.sin(u_wow * math.pi * 0.5)
                wow_glow_boost = int(85 * u_wow)
            elif wow_t < 4.2:
                u_snap = (wow_t - 3.8) / 0.4
                wow_pupil_mult = 1.28 - 0.58 * (u_snap ** 2.0)
                wow_snap_flash = int(180 * (1.0 - u_snap))
            else:
                if wow_t - dt < 4.2 <= wow_t:
                    self.blink_ctrl.trigger_blink(now, allow_double=False)
                u_rec = (wow_t - 4.2) / 2.0
                wow_pupil_mult = 0.70 + 0.30 * u_rec

        # 1. Blit the edge-to-edge wall of quotes (with Visual Silence & Mind State Dimming)
        base_field_alpha = int(255 * self.consciousness.text_dimming * awakening_fade)
        if impossible_freeze:
            base_field_alpha = int(255 * 0.12)

        if base_field_alpha >= 250 and not self.transition_active:
            self.virtual_frame_surf.blit(self.full_field_surf, (0, 0))
        else:
            self.virtual_frame_surf.fill((2, 2, 6, 255))
            self.full_field_surf.set_alpha(base_field_alpha)
            self.virtual_frame_surf.blit(self.full_field_surf, (0, 0))

        # Solitary Thought in Visual Silence: A single phrase glows across the quiet void
        if self.consciousness.text_dimming < 0.60 and not self.awakening_active:
            silence_alpha = int(235 * (1.0 - self.consciousness.text_dimming / 0.60))
            st_text = self.consciousness.solitary_thought
            st_fsize = max(11, int(13.5 * geom.scale))
            st_w, _ = self.font_mgr.measure(st_text, st_fsize, bold=True)
            st_x = geom.center_x - st_w * 0.5
            st_y = geom.center_y + int(geom.eye_half_h * 0.74)
            st_surf = create_word_sprite(self.font_mgr, st_text, st_fsize, 0.0, (235, 242, 255, silence_alpha), bold=True)
            self.virtual_frame_surf.blit(st_surf, (int(st_x), int(st_y)))

        # Smooth palette crossfade
        if self.transition_active and self.prev_full_field_surf is not None:
            t_trans = (now - self.transition_start) / self.transition_dur
            if t_trans >= 1.0:
                self.transition_active = False
                self.prev_full_field_surf = None
                self.prev_iris_layers.clear()
            else:
                old_alpha = int(255 * (1.0 - t_trans * t_trans))
                self.prev_full_field_surf.set_alpha(old_alpha)
                self.virtual_frame_surf.blit(self.prev_full_field_surf, (0, 0))

        # 2. Composite the eye interior (Sclera + Iris + Pupil + Highlights)
        if openness > 0.012 and self.eye_box_canvas is not None and self.eye_box_mask is not None:
            self.eye_box_canvas.fill((0, 0, 0, 0))

            sclera_dx = int(gaze_x * 0.25)
            sclera_dy = int(gaze_y * 0.22)
            if self.sclera_surf is not None:
                self.eye_box_canvas.blit(
                    self.sclera_surf,
                    (sclera_dx, sclera_dy),
                    area=self.eye_box_rect,
                )

            iris_cx = local_cx + int(gaze_x)
            iris_cy = local_cy + int(gaze_y) - int(geom.eye_half_h * 0.04)

            if self.iris_cutout_mask is not None:
                cw, ch = self.iris_cutout_mask.get_size()
                self.eye_box_canvas.blit(
                    self.iris_cutout_mask,
                    (iris_cx - cw // 2, iris_cy - ch // 2),
                    special_flags=pygame.BLEND_RGBA_MULT,
                )

            # Atmospheric bloom glow with consciousness luminance & WOW boost
            glow_surf = self.iris_layers.get("glow")
            if glow_surf is not None:
                gw, gh = glow_surf.get_size()
                base_pulse = 130 + 45 * math.sin(now * 1.4)
                glow_val = (base_pulse * self.consciousness.iris_luminance + wow_glow_boost + wow_snap_flash + impossible_alpha_boost)
                glow_surf.set_alpha(int(np.clip(glow_val, 0, 255)))
                self.eye_box_canvas.blit(
                    glow_surf,
                    (iris_cx - gw // 2, iris_cy - gh // 2),
                    special_flags=pygame.BLEND_RGBA_ADD,
                )

            # Organic iris breathing + biological vertical squash on blink
            iris_breath = 1.0 if impossible_freeze else (1.0 + 0.007 * math.sin(now * 1.15))
            iris_squash_y = 1.0 - 0.045 * (1.0 - openness)
            total_iris_scale_x = iris_breath * awakening_iris_scale
            total_iris_scale_y = iris_breath * iris_squash_y * awakening_iris_scale

            # Razor-sharp master anime Iris with 6-layer organic depth
            iris_surf = self.iris_layers.get("iris")
            if iris_surf is not None:
                iw, ih = iris_surf.get_size()
                if abs(total_iris_scale_x - 1.0) > 0.008 or abs(total_iris_scale_y - 1.0) > 0.008:
                    siw = max(10, int(iw * total_iris_scale_x))
                    sih = max(10, int(ih * total_iris_scale_y))
                    s_iris = pygame.transform.smoothscale(iris_surf, (siw, sih))
                    self.eye_box_canvas.blit(s_iris, (iris_cx - siw // 2, iris_cy - sih // 2))
                else:
                    self.eye_box_canvas.blit(iris_surf, (iris_cx - iw // 2, iris_cy - ih // 2))

            # Cross-fade previous iris if palette transition active
            if self.transition_active and "iris" in self.prev_iris_layers:
                old_iris = self.prev_iris_layers["iris"]
                old_iris.set_alpha(int(255 * (1.0 - t_trans)))
                oiw, oih = old_iris.get_size()
                self.eye_box_canvas.blit(old_iris, (iris_cx - oiw // 2, iris_cy - oih // 2))

            # Deep obsidian Pupil with cognitive thought dilation & recursive core
            pupil_surf = self.iris_layers.get("pupil")
            if pupil_surf is not None:
                pw, ph = pupil_surf.get_size()
                cog_pulse = self.camera.accommodation_pulse * 0.04
                att_boost = self.camera.viewer_attentiveness * 0.08
                thought_pulse = 0.0 if impossible_freeze else (0.038 * math.sin(now * 0.90) + 0.025 * (1.0 - openness))
                p_scale = (1.0 + thought_pulse - cog_pulse + att_boost) * self.consciousness.pupil_dilation * wow_pupil_mult * impossible_pupil_mult
                spw = max(8, int(pw * p_scale * total_iris_scale_x))
                sph = max(8, int(ph * p_scale * total_iris_scale_y))
                s_pupil = pygame.transform.smoothscale(pupil_surf, (spw, sph))
                self.eye_box_canvas.blit(
                    s_pupil, (iris_cx - spw // 2, iris_cy - sph // 2)
                )

            # Translucent corneal highlight words & 3D SPHERICAL CORNEA PARALLAX
            hl_surf = self.iris_layers.get("highlights")
            if hl_surf is not None:
                hw, hh = hl_surf.get_size()
                # 3D Spherical Cornea: highlight curves realistically across spherical cornea dome
                hl_dist = math.hypot(gaze_x, gaze_y)
                sphere_curve = max(0.65, 1.0 - (hl_dist / max(1.0, geom.iris_radius * 2.2)) ** 2)
                hl_drift_x = 3.2 * math.cos(now * 0.75) if not impossible_freeze else 0.0
                hl_drift_y = 2.0 * math.sin(now * 0.65) if not impossible_freeze else 0.0
                hl_x = local_cx + int(gaze_x * 1.35 * sphere_curve + hl_drift_x) - hw // 2
                hl_y = local_cy + int(gaze_y * 1.35 * sphere_curve + hl_drift_y) - int(geom.eye_half_h * 0.04) - hh // 2
                hl_alpha = int(np.clip(255 * (openness ** 1.6), 0, 255))
                if imp_phase in (2, 3, 4, 5):
                    hl_alpha = 255
                hl_surf.set_alpha(hl_alpha)
                self.eye_box_canvas.blit(hl_surf, (hl_x, hl_y))

            # The 9-Phase Impossible Revelation: Sentence Glow, Disintegration & Gravity Ingestion
            if self.consciousness.impossible_active and imp_phase in (4, 5, 6, 7):
                rev_text = self.consciousness.revelation_text
                rfsize = max(10, int(12.5 * geom.scale))
                rw_px, _ = self.font_mgr.measure(rev_text, rfsize, bold=True)
                rev_cx = iris_cx
                rev_cy = iris_cy - int(geom.pupil_radius * 1.35)

                if imp_phase in (4, 5):
                    # Solid incandescent silver phrase
                    rev_surf = create_word_sprite(self.font_mgr, rev_text, rfsize, 0.0, (255, 248, 255, 250), bold=True)
                    self.eye_box_canvas.blit(rev_surf, (rev_cx - rw_px // 2, rev_cy))
                elif imp_phase == 6:
                    # Phase 6: Disintegration of sentence into letters and sparks
                    u_dis = (imp_t - 8.0) / 1.2
                    char_x = rev_cx - rw_px // 2
                    for c_idx, ch in enumerate(rev_text):
                        if ch.strip():
                            cw_px, _ = self.font_mgr.measure(ch, rfsize, bold=True)
                            scatter_x = math.sin(c_idx * 1.7) * (38.0 * u_dis * geom.scale)
                            scatter_y = -abs(math.cos(c_idx * 1.3)) * (26.0 * u_dis * geom.scale)
                            ch_surf = create_word_sprite(self.font_mgr, ch, rfsize, float(u_dis * 45.0 * (1 if c_idx % 2 == 0 else -1)), (255, 230, 245, int(255 * (1.0 - u_dis * 0.35))), bold=True)
                            self.eye_box_canvas.blit(ch_surf, (int(char_x + scatter_x), int(rev_cy + scatter_y)))
                            char_x += cw_px
                        else:
                            char_x += int(8 * geom.scale)
                elif imp_phase == 7:
                    # Phase 7: Gravity Ingestion into Pupil Singularity
                    u_abs = (imp_t - 9.2) / 1.3
                    pull_in = max(0.0, 1.0 - u_abs)
                    for c_idx in range(len(rev_text)):
                        ang = (c_idx / float(max(1, len(rev_text)))) * math.tau + u_abs * 7.5
                        r_pull = geom.pupil_radius * (0.2 + 1.3 * pull_in)
                        px_c = iris_cx + r_pull * math.cos(ang)
                        py_c = iris_cy + r_pull * math.sin(ang)
                        p_col = (255, int(190 * pull_in), int(215 * pull_in))
                        p_sz = max(1, int(3.5 * pull_in * geom.scale))
                        pygame.draw.circle(self.eye_box_canvas, (*p_col, int(255 * pull_in)), (int(px_c), int(py_c)), p_sz)

            # Clip the eye interior to the instantaneous upper & lower eyelid curves
            y_up, y_lo = eval_eyelid_curves(self.mask_u, openness, geom)
            lid_gaze_y = gaze_y * 0.20 * openness
            mask_x = local_cx + self.mask_u * geom.eye_half_w
            y_up_box = local_cy + y_up + lid_gaze_y
            y_lo_box = local_cy + y_lo + lid_gaze_y

            poly_pts = list(zip(mask_x.tolist(), y_up_box.tolist())) + list(
                zip(mask_x[::-1].tolist(), y_lo_box[::-1].tolist())
            )
            self.eye_box_mask.fill((0, 0, 0, 0))
            if len(poly_pts) >= 3:
                pygame.draw.polygon(self.eye_box_mask, (255, 255, 255, 140), poly_pts, width=4)
                pygame.draw.polygon(self.eye_box_mask, (255, 255, 255, 255), poly_pts, width=0)

            self.eye_box_canvas.blit(
                self.eye_box_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
            )
            self.virtual_frame_surf.blit(self.eye_box_canvas, (bx, by))

            # Retinal Afterimage persistence of vision
            if self.afterimage_surf is not None and self.afterimage_alpha > 1.0:
                self.afterimage_surf.set_alpha(int(self.afterimage_alpha))
                self.virtual_frame_surf.blit(self.afterimage_surf, (bx, by), special_flags=pygame.BLEND_RGBA_ADD)
                self.afterimage_alpha = max(0.0, self.afterimage_alpha - dt * 65.0)
                if self.afterimage_alpha <= 1.0:
                    self.afterimage_surf = None

        # 2.8 Bold dark anime eyeliner ribbon along moving eyelid contour
        u_liner = np.linspace(-1.0, 1.0, 96)
        yu_l, yl_l = eval_eyelid_curves(u_liner, openness, geom)
        lid_gaze_y = gaze_y * 0.20 * openness
        upper_liner_pts = [
            (int(geom.center_x + u_val * geom.eye_half_w), int(geom.center_y + yu_l[i] + lid_gaze_y))
            for i, u_val in enumerate(u_liner)
        ]
        lower_liner_pts = [
            (int(geom.center_x + u_val * geom.eye_half_w), int(geom.center_y + yl_l[i] + lid_gaze_y))
            for i, u_val in enumerate(u_liner)
        ]
        if len(upper_liner_pts) >= 2:
            pygame.draw.lines(self.virtual_frame_surf, (2, 1, 6), False, upper_liner_pts, width=max(4, int(12 * geom.scale)))
            pygame.draw.lines(self.virtual_frame_surf, (2, 1, 6), False, lower_liner_pts, width=max(2, int(4.5 * geom.scale)))

        # 3. Render anime eyelashes & eyelid rim stream along moving eyelid curves
        if openness < 0.22:
            angle_idx = 0
        elif openness < 0.68:
            angle_idx = 1
        else:
            angle_idx = 2

        u_arr = np.array([w.u for w in self.eyelid_rim_words], dtype=np.float32)
        y_up_w, y_lo_w = eval_eyelid_curves(u_arr, openness, geom)

        for idx, w in enumerate(self.eyelid_rim_words):
            surf = w.surfaces[angle_idx]
            wx = geom.center_x + w.u * geom.eye_half_w
            base_y = float(y_up_w[idx]) if w.is_upper else float(y_lo_w[idx])
            wy = geom.center_y + base_y + lid_gaze_y + w.v_offset
            sw, sh_h = surf.get_size()
            self.virtual_frame_surf.blit(surf, (int(wx) - sw // 2, int(wy) - sh_h // 2))

        # 3.5 Floating shaded anime petals & embers with SUBTLE PUPIL GRAVITATIONAL PULL
        eye_world_cx = geom.center_x + gaze_x
        eye_world_cy = geom.center_y + gaze_y - geom.eye_half_h * 0.04
        grav_radius = geom.iris_radius * (2.4 if self.wow_active else 1.6)

        p_speed_mult = 0.02 if impossible_freeze else 1.0

        for emb in self.embers:
            emb["y"] -= emb["vy"] * dt * p_speed_mult
            emb["x"] += (emb["vx"] + math.sin(now * emb["sway_spd"] + emb["phase"]) * emb["sway_amp"]) * dt * p_speed_mult
            emb["angle"] += emb["rot_spd"] * dt * p_speed_mult

            p_dx = eye_world_cx - emb["x"]
            p_dy = eye_world_cy - emb["y"]
            p_dist = math.hypot(p_dx, p_dy)

            if p_dist < grav_radius and p_dist > 4 and not impossible_freeze:
                pull_factor = (1.0 - p_dist / grav_radius) ** 1.7
                pull_speed = (85.0 if self.wow_active else 32.0) * pull_factor
                emb["x"] += (p_dx / p_dist) * pull_speed * dt
                emb["y"] += (p_dy / p_dist) * pull_speed * dt
                spin_speed = (42.0 if self.wow_active else 16.0) * pull_factor
                emb["x"] += (-p_dy / p_dist) * spin_speed * dt
                emb["y"] += (p_dx / p_dist) * spin_speed * dt

                if p_dist < geom.pupil_radius * 0.88:
                    emb["y"] = geom.canvas_h + 30
                    emb["x"] = random.uniform(0, geom.canvas_w)

            # Boundary wrap
            if emb["y"] < -35:
                emb["y"] = geom.canvas_h + 30
                emb["x"] = random.uniform(0, geom.canvas_w)
            elif emb["y"] > geom.canvas_h + 40:
                emb["y"] = -25
            if emb["x"] < -40:
                emb["x"] = geom.canvas_w + 30
            elif emb["x"] > geom.canvas_w + 40:
                emb["x"] = -30

            pulse = 0.78 + 0.22 * math.sin(now * emb["pulse_spd"] + emb["phase"])
            alpha = int(emb["base_alpha"] * pulse)
            ex = int(emb["x"])
            ey = int(emb["y"])

            dist_c = math.hypot(ex - geom.center_x, ey - geom.center_y) / (geom.eye_half_w * 1.5)
            env_factor = max(0.40, min(1.0, 1.05 - 0.45 * (dist_c ** 1.3)))
            final_alpha = int(alpha * env_factor * awakening_fade)

            if 0 <= emb["spr_idx"] < len(self.particle_sprites):
                _, base_spr = self.particle_sprites[emb["spr_idx"]]
                scale_f = emb["scale"]
                bw, bh = base_spr.get_size()
                tbw, tbh = max(4, int(bw * scale_f)), max(4, int(bh * scale_f))
                s_spr = pygame.transform.smoothscale(base_spr, (tbw, tbh))
                if abs(emb["angle"]) > 1.0:
                    s_spr = pygame.transform.rotate(s_spr, emb["angle"])
                s_spr.set_alpha(final_alpha)
                self.virtual_frame_surf.blit(s_spr, (ex - s_spr.get_width() // 2, ey - s_spr.get_height() // 2))

        # 3.8 THOUGHT GENESIS (Starlight sparks born at pupil center expanding into words)
        if not impossible_freeze and now - self.last_thought_birth_time > 2.2:
            self.last_thought_birth_time = now
            t_angle = random.uniform(0, math.tau)
            t_word = random.choice(THOUGHT_BIRTH_WORDS)
            self.thought_birth_sparks.append({
                "angle": t_angle,
                "r": float(geom.pupil_radius * 0.15),
                "speed": float(geom.iris_radius * 0.42),
                "word": t_word,
                "birth": now,
                "dur": 3.4,
            })

        active_sparks = []
        for tsp in self.thought_birth_sparks:
            age = now - tsp["birth"]
            if age < tsp["dur"]:
                tsp["r"] += tsp["speed"] * dt
                r_sp = tsp["r"]
                ang_sp = tsp["angle"]
                sx = eye_world_cx + r_sp * math.cos(ang_sp)
                sy = eye_world_cy + r_sp * math.sin(ang_sp)
                fade_sp = math.sin((age / tsp["dur"]) * math.pi)
                alpha_sp = int(220 * fade_sp)

                if r_sp < geom.pupil_radius * 1.05:
                    pygame.draw.circle(self.virtual_frame_surf, (*palette.accent_tint, alpha_sp), (int(sx), int(sy)), max(2, int(2.8 * geom.scale)))
                else:
                    w_deg = -math.degrees(ang_sp)
                    if 90 < (w_deg % 360) < 270:
                        w_deg += 180.0
                    w_surf = create_word_sprite(self.font_mgr, tsp["word"], max(6, int(7.2 * geom.scale)), w_deg, (*palette.accent_tint, alpha_sp), bold=True)
                    self.virtual_frame_surf.blit(w_surf, (int(sx) - w_surf.get_width() // 2, int(sy) - w_surf.get_height() // 2))
                active_sparks.append(tsp)
        self.thought_birth_sparks = active_sparks

        # 4. Camera Zoom Transformation: crop `cam_rect` and smoothly scale to physical display
        sub_view = self.virtual_frame_surf.subsurface(cam_rect)
        pygame.transform.smoothscale(
            sub_view, (geom.screen_w, geom.screen_h), self.screen
        )

        # 5. Cinematic radial screen vignette (darkens corners to heighten dramatic focus)
        if self.vignette_surf is not None:
            self.screen.blit(self.vignette_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def _render_help_overlay(self) -> None:
        if not self.show_help:
            return
        palette = PALETTES[self.palette_idx]
        s = min(self.geom.screen_w / 1512.0, self.geom.screen_h / 982.0)
        panel_w = int(490 * s)
        panel_h = int(320 * s)
        pil_panel = Image.new("RGBA", (panel_w, panel_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(pil_panel)
        draw.rounded_rectangle(
            (0, 0, panel_w - 1, panel_h - 1),
            radius=int(12 * s),
            fill=(6, 10, 18, 235),
            outline=(*palette.accent_tint, 170),
            width=1,
        )

        title_font = self.font_mgr.get_font(int(16 * s), bold=True)
        body_font = self.font_mgr.get_font(int(13 * s), bold=False)

        state_str = f"Mind State: {self.consciousness.state.upper()}  |  Palette: {palette.name.split('—')[0].strip()}"
        status_str = f"Zoom: {self.camera.zoom:.2f}x ({'AUTO' if self.camera.auto_zoom else 'LOCKED'}) | Attentive: {int(self.camera.viewer_attentiveness * 100)}% | FPS: {int(self.clock.get_fps())}"
        lines = [
            ("THE EYE WITHIN WORDS — Consciousness Controls", True),
            (state_str, False),
            (status_str, False),
            ("", False),
            ("SPACE : Trigger an immediate biological blink", False),
            ("B     : Enable / disable automatic blinking", False),
            ("Z     : Toggle automatic camera zooming", False),
            ("C     : Fluid color palette cross-fade", False),
            ("W     : Trigger 'Cosmic Awareness' WOW moment", False),
            ("M     : Trigger 'Impossible Moment' (9-Phase Sacred Journey)", False),
            ("R     : Regenerate arrangement of quotes", False),
            ("H     : Show / hide keyboard instructions", False),
            ("ESC   : Close the animation safely", False),
        ]

        y_cursor = int(16 * s)
        for text, is_header in lines:
            if not text:
                y_cursor += int(6 * s)
                continue
            font = title_font if is_header else body_font
            col = (240, 248, 255, 255) if is_header else (180, 206, 232, 240)
            draw.text((int(20 * s), y_cursor), text, font=font, fill=col)
            y_cursor += int((24 if is_header else 20) * s)

        self.screen.blit(pil_to_pygame(pil_panel), (int(28 * s), int(28 * s)))

    def run(self) -> None:
        running = True
        frame_idx = 0
        prev_time = time.perf_counter()

        while running:
            now = time.perf_counter()
            dt = min(0.05, max(0.001, now - prev_time))
            prev_time = now

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    if self.windowed:
                        self.screen = pygame.display.set_mode(
                            (event.w, event.h), pygame.RESIZABLE | pygame.DOUBLEBUF
                        )
                        self._build_all_layers()
                elif event.type == pygame.KEYDOWN:
                    # Any key skips awakening sequence immediately
                    if self.awakening_active:
                        self.awakening_active = False

                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.blink_ctrl.trigger_blink(now, allow_double=False)
                    elif event.key == pygame.K_b:
                        self.blink_ctrl.auto_blink = not self.blink_ctrl.auto_blink
                    elif event.key == pygame.K_z:
                        self.camera.auto_zoom = not self.camera.auto_zoom
                    elif event.key == pygame.K_c:
                        # Smooth cinematic palette crossfade
                        self.prev_full_field_surf = self.full_field_surf
                        self.prev_iris_layers = dict(self.iris_layers)
                        self.palette_idx = (self.palette_idx + 1) % len(PALETTES)
                        self._build_all_layers(is_crossfade=True)
                        self.transition_active = True
                        self.transition_start = now
                    elif event.key == pygame.K_w:
                        self.trigger_wow_moment(now)
                    elif event.key == pygame.K_m:
                        self.consciousness.trigger_impossible_moment(now)
                    elif event.key == pygame.K_r:
                        self.seed = random.randint(10000, 999999)
                        self._build_all_layers()
                    elif event.key == pygame.K_h:
                        self.show_help = not self.show_help
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.awakening_active:
                        self.awakening_active = False

            # Automatic WOW moment trigger
            if not self.wow_active and not self.awakening_active and not self.consciousness.impossible_active and now >= self.next_wow_time:
                self.trigger_wow_moment(now)

            openness = self.blink_ctrl.update(now)
            override_zoom: Optional[float] = None

            if self.test_frames > 0 and self.screenshot_dir:
                if frame_idx == 8:
                    openness = 1.0
                    override_zoom = 1.0
                elif frame_idx == 20:
                    openness = 1.0
                    override_zoom = 2.35
                elif frame_idx == 32:
                    openness = 0.0
                    override_zoom = 1.12

            # Zoom camera management with Cognitive Gaze Delay
            freeze_cam = self.consciousness.impossible_active and (now - self.consciousness.impossible_start < 3.8)
            cam_rect, gaze_x, gaze_y = self.camera.manage_zoom_and_camera(
                self.geom, now, dt, override_zoom=override_zoom, freeze_camera=freeze_cam
            )

            # Render the living composition
            self.render_fullscreen_composition(openness, cam_rect, gaze_x, gaze_y, now, dt)
            self._render_help_overlay()

            pygame.display.flip()
            self.clock.tick(60)

            if self.test_frames > 0 and self.screenshot_dir:
                if frame_idx in (8, 20, 32):
                    label = {8: "wide_open", 20: "closeup_zoom", 32: "blink_closed"}[frame_idx]
                    out_path = os.path.join(self.screenshot_dir, f"eye_within_words_{label}.png")
                    to_fn = getattr(pygame.image, "tobytes", None) or getattr(pygame.image, "tostring")
                    raw_rgb = to_fn(self.screen, "RGB")
                    Image.frombytes("RGB", self.screen.get_size(), raw_rgb).save(out_path)
            if self.test_frames > 0 and frame_idx >= self.test_frames:
                running = False

            frame_idx += 1

        pygame.quit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="THE EYE WITHIN WORDS — Python Generative Typography Animation"
    )
    parser.add_argument(
        "--windowed",
        action="store_true",
        help="Run in a resizable window instead of macOS full-screen mode.",
    )
    parser.add_argument(
        "--test-frames",
        type=int,
        default=0,
        help="Run for N frames and exit automatically (for visual verification).",
    )
    parser.add_argument(
        "--screenshot-dir",
        type=str,
        default=None,
        help="Directory to save verification screenshots when --test-frames is used.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app = EyeWithinWordsApp(
        windowed=args.windowed,
        test_frames=args.test_frames,
        screenshot_dir=args.screenshot_dir,
    )
    app.run()