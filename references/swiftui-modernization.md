# SwiftUI Component Modernization

Read this only for SwiftUI migrations.

## Migration map

| Existing pattern | Preferred direction |
| --- | --- |
| Custom navigation or tab bar | `NavigationStack`, `NavigationSplitView`, or `TabView` with system items |
| Custom search overlay | `.searchable` at the container that owns the search scope |
| Custom toolbar blur/background | System `.toolbar` composition; remove conflicting backgrounds first |
| Custom filled or blurred action button | Standard `Button`; use `.glass` or `.glassProminent` on iOS 26+ only when functionally appropriate |
| Several nearby custom glass controls | One `GlassEffectContainer` with consistent shapes and spacing |
| Glass applied to cards or reading content | Keep content solid or use a standard material when separation is actually needed |
| Custom collapsing tab bar | `tabBarMinimizeBehavior` on supported systems |
| Bottom control floating above tabs | `tabViewBottomAccessory` when it matches the product behavior |
| Sheet with forced custom background | Remove unnecessary `presentationBackground` customization and inspect the system result |

## Compatibility boundary

Keep availability logic around the complete component so semantics do not drift:

```swift
@ViewBuilder
private var primaryAction: some View {
    let button = Button(action: save) {
        Label("Save", systemImage: "checkmark")
            .frame(maxWidth: .infinity)
    }
    .controlSize(.large)

    if #available(iOS 26.0, *) {
        button.buttonStyle(.glassProminent)
    } else {
        button.buttonStyle(.borderedProminent)
    }
}
```

Do not create two separate actions or labels across branches.

## Custom glass

Use custom glass only after standard controls prove insufficient:

```swift
@available(iOS 26.0, *)
private struct FloatingActions: View {
    var body: some View {
        GlassEffectContainer(spacing: 12) {
            HStack(spacing: 12) {
                actionButton("square.and.arrow.up")
                actionButton("ellipsis")
            }
        }
    }

    private func actionButton(_ symbol: String) -> some View {
        Button { } label: {
            Image(systemName: symbol)
                .frame(width: 44, height: 44)
        }
        .buttonStyle(.glass)
        .accessibilityLabel(symbol == "ellipsis" ? "More" : "Share")
    }
}
```

When applying `.glassEffect(...)` directly, apply it after layout and appearance modifiers, use `.interactive()` only for controls, and keep related elements in the same `GlassEffectContainer`.

## Review traps

- Retaining `.toolbarBackground`, opaque overlays, or darkening gradients that obscure the system scroll-edge effect.
- Applying `.glassEffect()` to every card because glass is available.
- Nesting glass elements in separate containers even though they visually interact.
- Using tint as a palette rather than semantic emphasis.
- Hiding essential actions behind a gesture-only custom control.
- Raising the deployment target just to avoid a small fallback branch.
- Claiming Dynamic Type, VoiceOver, Reduce Transparency, or performance support without testing it.

