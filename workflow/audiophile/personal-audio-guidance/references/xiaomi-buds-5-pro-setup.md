# Xiaomi Buds 5 Pro Setup Reference

## Scope

Session-specific reference for configuring the user's Xiaomi Buds 5 Pro with a Redmi Note 14 Pro+ 5G and TIDAL/UAPP. Re-check exact model, firmware, and regional feature availability before making stronger codec claims.

## Signal-chain boundary

The Buds are self-contained TWS earbuds:

```text
Redmi phone → Bluetooth codec → Buds internal DAC/DSP/amplifier → drivers
```

The BGVP MX1 is not part of this chain and cannot improve it. Prioritize fit/seal, official firmware/app configuration, and one controlled DSP layer before considering hardware.

## Official app and baseline

Use the official **Xiaomi Earbuds** app to pair/manage the earbuds, update firmware, adjust EQ/noise cancellation, and customize controls. Begin with:

```text
Reference/Flat/Harman AudioEFX profile
Custom EQ: Off
Dolby Atmos/Xiaomi Sound: Off initially
Spatial audio/head tracking: Off for ordinary stereo music
ANC: Off in a quiet room; adaptive/appropriate mode in noisy travel
Multipoint: Off while evaluating
```

The names and available controls can vary by app version, firmware, region, and Buds model. Xiaomi's official product material advertises Harman AudioEFX tuning, app customization, and aptX Lossless for the Buds 5 Pro; it does not establish that every phone/firmware combination negotiates every feature.

## Codec decision tree

1. Update the app, earbuds, and case firmware.
2. Disable multipoint for a controlled quality test.
3. Select quality-priority/high-quality mode if exposed.
4. Inspect the live negotiated codec in Android Bluetooth details or Developer Options.
5. Use the highest codec that is actually active and stable.
6. If there are dropouts, revert to automatic/stable mode; do not force a codec with a third-party utility as a first step.

Do not assert aptX Lossless, LHDC, or a particular bit depth solely from product marketing. Both ends must support the codec, and Android/HyperOS may select a different one.

## EQ and DSP rules

Use the Xiaomi Earbuds EQ first because it is the companion configuration for the Buds wireless path. Test presets one at a time:

- Harman AudioEFX/Flat: baseline;
- Decrease Bass: if bass is boomy;
- Enhance Voice: speech/vocal preference;
- Enhance Treble: only if the sound is dull, with fatigue monitoring;
- Harman Master/Audiophile: preference comparisons, not automatically more accurate.

For custom EQ, start with 1–2 dB changes, match volume, and listen for 20–30 minutes. Do not stack Xiaomi EQ with Dolby, Xiaomi Sound, UAPP PEQ, Wavelet/Poweramp, and another system effect while diagnosing.

## ANC, transparency, and spatial features

ANC can improve real-world listening by reducing noise and making moderate music levels sufficient. Transparency is useful for awareness but may sound processed. Spatial audio and head tracking change presentation; they are not automatic fidelity upgrades. Test them separately with fixed track and volume, and prefer Off for a neutral stereo baseline.

## TIDAL/UAPP boundary

For Bluetooth Buds listening:

```text
TIDAL/native app or UAPP → Android Bluetooth → Buds
```

UAPP's direct USB settings (MX1, bit-perfect USB mode, USB buffer, device-native USB rate) apply to the MX1 route, not to the Buds' Bluetooth transport. The native TIDAL app is a clean comparison path if UAPP's Bluetooth routing is unclear.

## Evidence anchors

- Xiaomi product page: https://www.mi.com/global/product/xiaomi-buds-5-pro/
- Xiaomi Thailand product page: https://www.mi.com/th/product/xiaomi-buds-5-pro/
- Xiaomi Earbuds app: https://play.google.com/store/apps/details?id=com.mi.earphone
- Thai pairing FAQ: https://www.mi.com/th/support/faq/details/KA-541301/
- Thai app connection FAQ: https://www.mi.com/th/support/faq/details/KA-541296/
- Thai app features FAQ: https://www.mi.com/th/support/faq/details/KA-541289/
- Thai ANC FAQ: https://www.mi.com/th/support/faq/details/KA-541332/
