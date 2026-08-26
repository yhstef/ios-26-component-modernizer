# Apple iOS 26+ Modernization Baseline

Updated 2026-08-26 from official Apple sources. This is a maintained synthesis, not a substitute for checking current API availability when a task asks for the latest behavior.

## Official sources

- [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass)
- [Human Interface Guidelines: Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [SwiftUI: `glassEffect(_:in:)`](https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:))
- [SwiftUI: `GlassEffectContainer`](https://developer.apple.com/documentation/SwiftUI/GlassEffectContainer)
- [UIKit appearance customization](https://developer.apple.com/documentation/uikit/appearance-customization)
- [UIKit: `UIGlassEffect`](https://developer.apple.com/documentation/uikit/uiglasseffect)
- [UIKit: `UIGlassContainerEffect`](https://developer.apple.com/documentation/uikit/uiglasscontainereffect)
- [WWDC25: Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/)
- [WWDC25: Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/)
- [WWDC25: Build a UIKit app with the new design](https://developer.apple.com/videos/play/wwdc2025/284/)

## Normative migration principles

These come directly from Apple guidance:

1. **Recompile first.** Standard SwiftUI and UIKit structures and controls adopt much of the current appearance automatically when built with the current SDK.
2. **Use system components first.** Navigation, tabs, toolbars, search, sheets, menus, buttons, sliders, and toggles carry platform behavior that custom replicas usually miss.
3. **Separate function from content.** Liquid Glass is a functional layer for controls and navigation floating above content. Do not turn ordinary content surfaces into glass.
4. **Remove interference.** Custom toolbar, navigation-bar, tab-bar, or sheet backgrounds can fight automatic glass and scroll-edge behavior.
5. **Use custom glass sparingly.** Reserve it for important custom controls that standard components cannot express.
6. **Group related glass.** SwiftUI `GlassEffectContainer` and UIKit `UIGlassContainerEffect` provide coherent sampling, rendering, and interaction for nearby elements.
7. **Tint semantically.** Tint may signal a primary action, selection, or status. Tinting everything weakens hierarchy.
8. **Respect adaptation.** Regular and clear glass respond to content and accessibility settings. Clear glass is appropriate only over visually rich media when foreground content remains bold and legible.
9. **Preserve continuity.** Use hierarchy transitions and morphing only when they explain the spatial relationship between a control and the content or presentation it reveals.
10. **Design across contexts.** Verify different device sizes, input modes, content, appearances, and accessibility settings.

## Engineering interpretation

The following are implementation rules derived from the official principles, not verbatim Apple requirements:

- A successful migration often removes more custom styling than it adds.
- A match from the audit script is only a review candidate; `Material` and `UIVisualEffectView` can remain correct in the content layer.
- Preserve the app's minimum deployment target unless the user explicitly authorizes raising it.
- Prefer one compatibility branch at a component boundary over scattered availability checks throughout a view.
- Treat iOS 26 as the baseline for the named APIs, while verifying newer SDK changes before claiming current behavior.

