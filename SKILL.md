---
name: ios-26-component-modernizer
description: Modernize existing SwiftUI and UIKit components for iOS and iPadOS 26+ using current system structures, controls, and Liquid Glass where it belongs, while preserving behavior, accessibility, performance, and earlier-OS fallbacks. Use when auditing or implementing an iOS 26 design-system migration, replacing custom bars or controls with native components, removing legacy appearance overrides, or correcting Liquid Glass adoption. Do not use for visual-only mockups, product art direction, unrelated Swift bugs, or decorative glass treatment without an implementation request.
---

# iOS 26 Component Modernizer

Modernize real app code, not screenshots alone. Prefer the smallest native change that improves platform fit without changing product behavior.

## Route the Work

- For every substantial migration, read [references/apple-guidance.md](references/apple-guidance.md).
- For SwiftUI code, read [references/swiftui-modernization.md](references/swiftui-modernization.md).
- For UIKit code, read [references/uikit-modernization.md](references/uikit-modernization.md).
- Read both framework references only for a mixed SwiftUI/UIKit feature.
- When the user asks for current or latest API behavior, verify it against Apple Developer documentation before editing.

Do not take over product positioning or broad visual art direction. If the request is only a design concept, hand it to a design-focused workflow. If the request is an ordinary compiler, state, data, or performance bug, handle it as iOS engineering unless iOS 26 component migration is materially involved.

## Inspect Before Converting

1. Read repository instructions and inspect the relevant code, deployment target, Swift version, Xcode/SDK, navigation structure, appearance proxies, design tokens, tests, and user-owned changes.
2. Build with the newest available SDK before assuming code changes are necessary. Standard SwiftUI and UIKit components can adopt the new appearance automatically.
3. Optionally run `python3 scripts/audit_components.py <project-path>` to locate migration candidates. Treat its output as leads, never as errors or permission to edit every match.
4. Write a compact migration contract: components in scope, behavior that must remain unchanged, minimum OS, fallback behavior, accessibility requirements, and verification plan.

## Classify Each Candidate

Choose exactly one disposition per component:

1. **Keep and recompile** — the component already uses a standard structure or control and gains the current appearance automatically.
2. **Remove interference** — delete or narrow custom bar backgrounds, blur layers, shadows, fixed metrics, or appearance overrides that fight the system design.
3. **Replace with a system component** — prefer native navigation, tabs, toolbars, search, sheets, menus, buttons, sliders, toggles, and presentations over look-alike custom implementations.
4. **Apply custom Liquid Glass** — only for an important functional control or navigation surface that system components cannot express.
5. **Leave as content** — cards, media, reading surfaces, forms, and decorative backgrounds normally remain in the content layer and should not become glass.

Do not equate modernization with adding `.glassEffect()` everywhere.

## Implement Safely

- Preserve action semantics, state ownership, navigation, focus, restoration, analytics, and test identifiers unless the task explicitly changes them.
- Put content first and keep Liquid Glass in the functional layer for controls and navigation.
- Prefer standard controls before custom glass. Remove conflicting customization before adding new effects.
- Use tint only to communicate prominence, selection, or status; never as decoration across every control.
- Make custom glass interactive only when the element is actually interactive.
- Group nearby SwiftUI glass elements in `GlassEffectContainer`; group UIKit glass elements with `UIGlassContainerEffect` when appropriate.
- Apply SwiftUI glass effects after layout and appearance modifiers.
- Use morphing IDs only when animated hierarchy changes benefit from spatial continuity.
- Gate iOS 26-only APIs with availability checks when the deployment target is earlier, and keep the fallback behaviorally equivalent.
- Preserve Dynamic Type, VoiceOver labels and order, sufficient contrast, non-color cues, comfortable targets, Reduce Transparency, Increase Contrast, and Reduce Motion behavior.
- Avoid custom blur, masking, shadow, or animation stacks that recreate effects the system already provides.

## Verify Proportionally

At minimum:

1. Build the affected target with an SDK that contains the APIs used.
2. Exercise the changed component on iOS 26+ and the earliest supported fallback OS when available.
3. Check light and dark appearances, Increase Contrast, Reduce Transparency, accessibility text sizes, VoiceOver, localization expansion, rotation or iPad resizing where relevant.
4. Inspect scrolling and interaction for layering artifacts, illegible content, duplicated materials, incorrect safe areas, and expensive effect composition.
5. Run focused tests and report only checks that actually ran.

If the required SDK or simulator is unavailable, implement only code that can be reasoned about safely, identify the unverified boundary, and give the exact remaining build or runtime check.

## Report the Result

Lead with the implemented outcome. Then include:

- the component mapping: old implementation → chosen disposition → new implementation;
- files changed and important compatibility decisions;
- build, test, runtime, accessibility, and performance evidence actually collected;
- remaining risks or components intentionally left unchanged, with reasons.
