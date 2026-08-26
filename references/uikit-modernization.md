# UIKit Component Modernization

Read this only for UIKit migrations.

## Migration map

| Existing pattern | Preferred direction |
| --- | --- |
| Custom tab or sidebar controller | `UITabBarController` / `UISplitViewController` and current system APIs |
| Opaque navigation or toolbar styling | Remove unnecessary `UINavigationBarAppearance`, `UIToolbarAppearance`, background-color, or shadow overrides |
| Custom floating action background | `UIButton.Configuration.glass()` where available and appropriate |
| Custom blur pretending to be glass | `UIGlassEffect` inside `UIVisualEffectView` for a genuinely custom functional element |
| Several nearby glass elements | `UIGlassContainerEffect` with nested `UIVisualEffectView` glass elements |
| Artwork clipped beside an iPad sidebar | `UIBackgroundExtensionView` for eligible media, with text and controls as siblings |
| Custom minimizing tab bar | `UITabBarController.tabBarMinimizeBehavior` on supported systems |
| Custom mini-player above tabs | `UITabAccessory` when it matches the interaction model |

## Standard button migration

```swift
private func configurePrimaryButton(_ button: UIButton) {
    var configuration: UIButton.Configuration

    if #available(iOS 26.0, *) {
        configuration = .glass()
    } else {
        configuration = .filled()
    }

    configuration.title = "Continue"
    configuration.image = UIImage(systemName: "arrow.right")
    button.configuration = configuration
    button.accessibilityLabel = "Continue"
}
```

Keep the action, accessibility identity, menu, enabled state, and test identifier unchanged during a visual migration.

## Custom glass

For a custom functional element on iOS 26+, `UIGlassEffect(style:)` provides glass configuration through `isInteractive` and `tintColor`. Render it with `UIVisualEffectView`. When several glass elements are near one another, use a `UIVisualEffectView` configured with `UIGlassContainerEffect` and place the individual glass effect views inside its `contentView`.

Verify the exact `UIGlassEffect.Style` case in the active SDK before writing the initializer. Do not guess API cases from memory.

## Review traps

- Global `UIAppearance` rules that silently override every bar or control.
- `configureWithOpaqueBackground()`, custom bar colors, and shadow images left in place after recompiling.
- Extending text or controls with `UIBackgroundExtensionView` instead of extending only eligible media.
- Using multiple independent glass containers for controls that visually merge.
- Replacing a native control with a custom one just to reproduce the new appearance.
- Removing fallback UI or raising the deployment target without authorization.
- Reporting runtime success without exercising the actual controller hierarchy.

