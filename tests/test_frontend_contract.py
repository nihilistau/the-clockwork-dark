"""
Frontend contract tests
========================

Guards the a11y + XSS-escaping invariants of the clockwork scene from the Python
suite — no Node toolchain required. The behavioural unit tests of the pure
helpers live in ``frontend-tests/`` (vitest); these static checks make sure the
fixes can't silently regress in CI.
"""

from __future__ import annotations

from pathlib import Path

_SCENE = Path(__file__).resolve().parents[1] / "content" / "scenes" / "clockwork"
_JS = (_SCENE / "static" / "js" / "clockwork.js").read_text(encoding="utf-8")
_HELPERS = (_SCENE / "static" / "js" / "clockwork-helpers.js").read_text(encoding="utf-8")
_DIALOGS = (_SCENE / "static" / "js" / "clockwork-dialogs.js").read_text(encoding="utf-8")
_CSS = (_SCENE / "static" / "css" / "clockwork.css").read_text(encoding="utf-8")
_HTML = (_SCENE / "templates" / "clockwork.html").read_text(encoding="utf-8")


def test_inventory_render_escapes_model_text():
    # The model-controlled item name must route through escapeHtml in the
    # innerHTML sink (a textContent fallback elsewhere is inherently safe).
    assert "${escapeHtml(item.name)}" in _JS
    for line in _JS.splitlines():
        if "innerHTML" in line:
            assert "${item.name}" not in line
            assert "${item.qty}" not in line


def test_overlay_model_text_is_escaped():
    # Rumors and foe text are escaped too.
    assert "${escapeHtml(foe.name" in _JS
    assert "escapeHtml(typeof r ===" in _JS


def test_pure_modules_extracted_and_loaded_first():
    # Both extracted modules are dual-mode and load before the bundle that uses them.
    assert "module.exports" in _HELPERS and "ClockworkHelpers" in _HELPERS
    assert "module.exports" in _DIALOGS and "ClockworkDialogs" in _DIALOGS
    main = _HTML.index('js/clockwork.js"')
    assert _HTML.index("clockwork-helpers.js") < main
    assert _HTML.index("clockwork-dialogs.js") < main
    # The bundle consumes the dialog manager.
    assert "ClockworkDialogs.create" in _JS


def test_dialogs_have_keyboard_dismissal_and_focus_trap():
    # The behaviour lives in the extracted, unit-tested dialog manager.
    assert 'ev.key === "Escape"' in _DIALOGS
    assert 'ev.key === "Tab"' in _DIALOGS  # focus trap
    assert "function openDialog" in _DIALOGS and "function closeDialog" in _DIALOGS
    # Every role=dialog overlay is focus-targetable (tabindex=-1).
    assert _HTML.count('role="dialog"') == _HTML.count('tabindex="-1"')
    assert _HTML.count('role="dialog"') >= 4


def test_doom_end_modal_is_dismissable():
    assert 'id="doom-end-close"' in _HTML
    assert "doom-end-close" in _JS


def test_dead_mic_button_is_disabled():
    assert 'id="mic-btn"' in _HTML
    tag = _HTML[_HTML.index('id="mic-btn"'):]
    tag = tag[: tag.index(">")]
    assert "disabled" in tag and "aria-disabled" in tag


def test_reduced_motion_and_focus_visible_present():
    assert "prefers-reduced-motion" in _CSS
    assert ":focus-visible" in _CSS


def test_dice_toast_shows_the_rolled_face():
    assert 'id="dice-face"' in _HTML
    assert "diceFace" in _JS
    assert "dice_faces" in _JS
    assert ".dice-face" in _CSS


def test_reactive_notice_board():
    # The board reacts to the world flags and pins the Dark's own bounties.
    assert "NOTICE_POSTERS" in _JS
    assert "notice-board-tunnel-revealed" in _JS
    assert "lastFlags" in _JS
    # poster title/text routed through escapeHtml
    assert "escapeHtml(p.title)" in _JS
    assert ".notice-posting" in _CSS


def test_ambient_doom_toast_is_polite():
    tag = _HTML[_HTML.index('id="doom-toast"'):]
    tag = tag[: tag.index(">")]
    assert 'aria-live="polite"' in tag
