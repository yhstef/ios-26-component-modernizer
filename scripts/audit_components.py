#!/usr/bin/env python3
"""Find Swift source patterns worth reviewing during an iOS 26+ UI migration.

Matches are candidates, not errors. The script is read-only and uses only the
Python standard library.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SKIP_PARTS = {
    ".build",
    ".git",
    ".swiftpm",
    "Carthage",
    "DerivedData",
    "Pods",
    "SourcePackages",
}


PATTERNS: tuple[tuple[str, str, str], ...] = (
    (
        "legacy-bar-customization",
        r"UINavigationBarAppearance|UITabBarAppearance|UIToolbarAppearance|UIBarAppearance|configureWithOpaqueBackground|toolbarBackground",
        "Review custom bar backgrounds and appearance overrides before adding new effects.",
    ),
    (
        "custom-blur-or-material",
        r"UIBlurEffect|UIVisualEffectView|\.(?:ultraThin|thin|regular|thick)Material",
        "Decide whether this is valid content-layer separation or a custom control that should use a system component.",
    ),
    (
        "custom-shape-control",
        r"cornerRadius\(|clipShape\(RoundedRectangle|background\([^\n]*RoundedRectangle",
        "Check whether a custom rounded control can become a standard iOS control.",
    ),
    (
        "system-structure",
        r"NavigationView|NavigationStack|NavigationSplitView|TabView|UITabBarController|UISplitViewController",
        "Inspect the system structure after recompiling with the current SDK before rewriting it.",
    ),
    (
        "presentation-background",
        r"presentationBackground|modalPresentationStyle|UIAlertController|actionSheet\(",
        "Review presentation customization and source anchoring on iOS 26+.",
    ),
    (
        "existing-liquid-glass",
        r"glassEffect|GlassEffectContainer|UIGlassEffect|UIGlassContainerEffect|\.glassProminent|\.glass\(\)",
        "Review availability, grouping, modifier order, interactivity, and fallback behavior.",
    ),
)


@dataclass(frozen=True)
class Finding:
    category: str
    file: str
    line: int
    excerpt: str
    guidance: str


def swift_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        if root.suffix == ".swift":
            yield root
        return

    for path in root.rglob("*.swift"):
        if not any(part in SKIP_PARTS for part in path.parts):
            yield path


def scan(root: Path) -> list[Finding]:
    compiled = [(category, re.compile(pattern), guidance) for category, pattern, guidance in PATTERNS]
    findings: list[Finding] = []

    for path in sorted(swift_files(root)):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        for number, line in enumerate(lines, start=1):
            for category, pattern, guidance in compiled:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            category=category,
                            file=str(path),
                            line=number,
                            excerpt=line.strip()[:180],
                            guidance=guidance,
                        )
                    )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Locate Swift UI patterns worth reviewing for an iOS 26+ component migration."
    )
    parser.add_argument("path", nargs="?", default=".", help="Swift file or project directory to scan")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        parser.error(f"path does not exist: {root}")

    findings = scan(root)
    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2, ensure_ascii=False))
    elif not findings:
        print("No migration candidates found. This does not prove the UI is fully modernized.")
    else:
        print(f"Found {len(findings)} review candidate(s). Matches are not errors.\n")
        for item in findings:
            print(f"[{item.category}] {item.file}:{item.line}")
            print(f"  {item.excerpt}")
            print(f"  {item.guidance}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

