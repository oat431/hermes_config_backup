---
name: personal-audio-guidance
description: "Use for personal-audio advice. Audit owned gear first."
version: 1.1.0
author: Audiophile + Panomete
license: MIT
platforms: [windows, macos, linux, android, ios]
metadata:
  hermes:
    tags: [audio, headphones, iem, dac, amp, eq, windows, recommendations]
    category: audio
---

# Personal Audio Guidance

## Overview

Give practical, measurement-aware advice for headphones, IEMs, DACs, amplifiers, wireless audio, EQ, and desktop listening chains. Start from what the user already owns and what they actually hear. Improve the signal path and fit before recommending replacement hardware.

This is a class-level workflow: it applies to a single IEM chain, a desktop setup, a commuting system, or an upgrade plan. The goal is not to maximize equipment count; it is to maximize useful listening improvement per baht.

## When to Use

Load when the user asks how to:

- improve sound quality or listening enjoyment;
- choose or pair an IEM/headphone with a source, dongle, DAC, or amplifier;
- understand 3.5 mm, 4.4 mm, balanced, USB, codecs, impedance, sensitivity, or output power;
- configure Windows/macOS audio, EQ, exclusive mode, spatial processing, or music players;
- decide whether a cable, DAC/amp, eartip, software, or new transducer is the next upgrade;
- compare a user's owned gear with a purchase candidate.

Do not use this as the owner of self-hosted music-server deployment, room/network infrastructure, or general computer troubleshooting; route those parts to the relevant specialist while retaining the audio requirements.

## Operating Principles

1. **Translate the goal.** Map vague requests such as “make listening better” to the likely target: tonal balance, bass, treble fatigue, detail, imaging, soundstage, loudness, noise, comfort, isolation, or workflow convenience. If the goal is obvious, act; ask only when different goals would change the recommendation.
2. **Inspect the actual host when invited.** For computer-side audio, run a read-only device/process/endpoint audit before prescribing software. Report only observable facts, distinguish detection from active routing, and state what could not be inspected. Do not infer the phone's live state from a connected Windows PC; Android inspection requires an authorized bridge or user-provided screenshots.
3. **Treat mobile and desktop as separate DSP paths.** A Windows system-wide EQ such as Equalizer APO + Peace does not apply to Android playback. For an Android USB DAC, use the player's own direct USB driver and its own PEQ/DSP, or a compatible Android/system EQ—not the Windows configuration.
4. **Configure UAPP in two explicit modes.** For a clean TIDAL/USB baseline use `Use USB DAC` on, bit-perfect `When possible` first, then test `On` only if playback is stable and no DSP is needed; leave resampling and EQ off initially. For tonal correction, turn bit-perfect off and use UAPP ToneBoosters PEQ or another single DSP layer. Verify the now-playing technical display instead of assuming the requested sample rate is the delivered rate.
5. **Prefer reliable defaults over audiophile theater.** Do not force 192/384/768 kHz, add obscure USB tweaks, or configure around MQA without a demonstrated need. Try `USB tweak 2` and a larger buffer only when there are dropouts/clicks or device-specific failures. `When possible` is preferable to forcing strict bit-perfect when a format or route cannot be handled.
6. **Include the portable physical layer.** Check that the USB-C cable carries data, the phone grants USB permission, and the dongle is mechanically supported. A short/flexible/right-angle cable can reduce port strain but is not a sound-quality upgrade. Do not recommend random charge-through splitters; powered USB hubs must explicitly support USB host/audio and charging.
7. **Account for Android power management.** If playback stops with the screen off, set the player to `No restrictions`/allow background activity and lock it in recents where applicable. Treat this as a conditional troubleshooting step, not a universal tweak.
8. **Clarify the volume-control domain.** Distinguish the phone media slider, UAPP software volume, USB-controlled device volume, and the MX1's hardware volume. Start the MX1 at low gain and low volume; do not assume a bit-perfect path has normal software-volume behavior.
9. **Separate current streaming formats from legacy documentation.** UAPP pages may still mention MQA and older TIDAL behavior. Check the current service format and subscription before recommending an MQA decoder; prefer current lossless/Hi-Res FLAC where available and label legacy evidence.
10. **Separate phone DSP labels from the actual player path.** Dolby Atmos, Xiaomi Sound, Mi Sound, spatial audio, and similar vendor controls are DSP choices, not additional amplifier power. With a player's direct USB driver, they may be bypassed or may not affect the external DAC. Test the toggle while holding volume and track constant; if UAPP's direct output does not change, leave the phone effect off for the neutral baseline. A TIDAL Dolby Atmos mix is distinct from a phone's generic Dolby sound-effect toggle.
11. **Keep user-facing responses compact before detail.** Lead with a short verdict and a copyable settings table, then explain the why, troubleshooting branches, and what not to buy. Avoid making the user parse a long research narrative to find the settings.
12. **Inventory first.** Check the user's known gear before suggesting anything. Ask what is already connected and inspect the computer when permission is given. Do not recommend a duplicate DAC/amp merely because a product is newer or more expensive.
13. **Treat headphones with both analog and wireless modes as two different devices.** Write separate chains and settings for wired passive/active use and Bluetooth use. Do not carry over UAPP USB settings, Sony Bluetooth EQ, LDAC, DSEE, or ANC assumptions from one path to the other.
14. **Verify adapter direction and load before recommending a 4.4 mm-to-3.5 mm connection.** A headphone with one 3.5 mm input is not balanced merely because its source uses 4.4 mm. Prefer the source's 3.5 mm output or a cable explicitly documented as safe from the specific balanced source to a single-ended load; never approve a generic adapter based only on plug fit.
15. **For Bluetooth, optimize reliability before codec numbers.** Start with the vendor app, disable multipoint while evaluating, select the highest-quality codec only if it is actually active and stable, and fall back when there are dropouts. Verify the active codec rather than assuming “high quality” means LDAC.
16. **Separate headphone firmware DSP from upstream DSP.** App EQ, DSEE/upscaling, ANC/ambient processing, adaptive sound controls, spatial modes, and player/system EQ can each alter the signal. Begin with a flat, repeatable profile; add one feature at a time and level-match comparisons.
17. **Treat self-contained TWS earbuds as their own complete chain.** For earbuds such as Xiaomi Buds 5 Pro, do not route the BGVP MX1 into them or recommend another DAC/amp. Start with the official companion app, firmware update, fit/seal, flat or manufacturer reference profile, highest stable negotiated codec, and ANC appropriate to the environment. Verify the active codec rather than assuming the phone/earbud advertises the best one.
18. **Keep TWS feature claims model- and region-aware.** Distinguish the Bluetooth model from a Wi-Fi variant, and mark aptX Lossless, LHDC, spatial audio, head tracking, EQ presets, and multipoint as conditional on both device compatibility, firmware, and current app support. If the exact phone codec support is not verified, instruct the user to inspect the live negotiated codec instead of asserting it.

## Core Reasoning Rules

1. **Manifest the real chain.** Write the path as `source → operating-system mixer → DSP/enhancement → DAC/amp → output connector → transducer`. Distinguish a device that is installed from the endpoint that is actually active. Virtual endpoints such as FxSound can hide the physical USB DAC behind another output.
2. **Separate problems from preferences.** Insufficient volume, clipping, channel imbalance, audible hiss, high output impedance interaction, driver problems, and dropouts are technical problems. A request for warmer bass or softer treble is a tuning preference. Treat each differently.
3. **Check the transducer before power.** Use impedance and sensitivity to judge whether the source has enough voltage/current. Efficient IEMs normally need low gain and little amplifier power. If the IEM is already clean and loud enough, fit, seal, eartips, EQ, recording quality, and the IEM's tuning are more plausible limits than the DAC chip.
4. **Connector is not circuit.** A 4.4 mm plug identifies a connector format, not automatically a balanced signal. Confirm the source's output circuit and use a directly terminated cable. Never claim that a passive adapter converts single-ended output to balanced; beware adapters that join grounds on a true balanced output.
5. **Build a neutral baseline.** For diagnosis, select the physical DAC endpoint, bypass spatial audio and vendor effects, disable or bypass extra enhancement layers, and use one predictable volume path. Re-enable effects one at a time only when intentionally choosing their sound.
6. **Use one DSP at a time.** Choose the hardware/player PEQ or the system EQ first, not both. Equalizer APO + Peace is a strong Windows-wide option; a capable player with WASAPI exclusive output is useful for local files. Explain that exclusive mode controls routing and can provide bit-exact output; it is not a magic tonal upgrade.
7. **EQ conservatively.** Prefer a trustworthy measurement and label its target, rig, and limitations. Apply a negative preamp when positive filters can clip. Make small changes, match loudness, compare against bypass, and account for seal/insertion depth. Never invent exact filters from a graph that was not actually read or from a search snippet; if a measurement page is rate-limited, give a labeled listening experiment instead.
8. **Price for the local user.** When recommending a purchase, check Thailand availability and warranty through official Thai distributors, Shopee/Lazada, or reputable local dealers when possible. Distinguish official stock from grey import and say when a price could not be verified. For expensive gear, suggest auditioning first.
9. **Reject snake oil politely.** Do not sell exotic USB cables, cable burn-in, audiophile fuses, connector-only “balanced” adapters, or DAC/amp swaps that cannot address the stated problem. Respect a preference purchase when the user understands it is a preference purchase.
10. **Protect hearing.** Start efficient IEMs on low gain and low volume. Warn when a source has excessive power for the load, and do not encourage volume increases as a substitute for better tuning or fit.

## Obsidian Knowledge-Base Workflow

When the user asks to build terminology, fundamentals, or buying guidance for the audio vault, treat it as a class-level knowledge-base task rather than a one-off answer:

1. Inspect the requested vault location and existing note structure before writing.
2. Preserve the user's folder separation: durable setup notes in `audio/setup/` and reusable concepts/terminology in `audio/knowledge/`.
3. Use numbered, hyphenated filenames (`00-...`, `01-...`) and maintain a navigable index/MOC at the root of each section.
4. Start with a practical learning map, then create concept notes that explain the term, why it matters, how to interpret its values, and how it applies to the user's owned chain.
5. Include decision matrices for “high value / conditional / mostly marketing,” with the reason and the cheapest reversible test—not just a glossary.
6. Link related notes with relative Obsidian wikilinks such as `[[knowledge/04-Frequency-Response-and-EQ]]`; after moving existing notes, update all index links and verify the resulting file tree and link targets.
7. Keep claims scoped: label manufacturer specifications, independent measurements, and subjective experiments separately; cite sources when research was used.
8. Do not overwrite existing supporting notes blindly. Read them first, preserve useful content, and report any unresolved links or path assumptions.

For this user's audio vault, `references/obsidian-audio-knowledge-template.md` contains the reusable note structure and matrix pattern.

## Recommendation Order

Use this order unless the user has a clearly different priority:

1. Confirm the goal and listening context.
2. Check owned gear and the actual signal path.
3. Fix endpoint selection, routing, driver, enhancement, and fit issues.
4. Try reversible EQ or eartip changes.
5. Upgrade the transducer if its tuning or comfort is the bottleneck.
6. Upgrade the source only for a demonstrated technical need: noise, output impedance, insufficient power, controls, connectivity, or reliability.
7. Consider premium hardware only after the rest of the chain and the budget justify it.

Every recommendation should state **what changes**, **why it changes**, **what it will not change**, and **the cheapest reversible test**.

## Research and Evidence

For current specs, measurements, prices, and availability:

- prefer manufacturer specifications for connector/function claims;
- prefer independent measurements for frequency response, output impedance, noise, distortion, and power behavior;
- cite the page actually inspected, not only a search-result snippet;
- label manufacturer claims, independent measurements, and subjective impressions separately;
- state uncertainty when different measurement rigs, revisions, cables, or insertion depths can change the result.

Load `references/mx1-d1-evidence.md` for the evidence bank from the BGVP MX1 + COZOY D1 case, `references/windows-audio-triage.md` for the reusable Windows endpoint/DSP audit pattern, and `references/android-uapp-triage.md` for the reusable Android/UAPP/USB-DAC setup pattern. The Android reference includes the vendor-DSP/spatial-audio decision tree.

## Output Style

Use direct, friendly language and explain the “why” in plain English or Thai as requested. Prefer a short verdict followed by an ordered setup and a clear “do not buy yet” section. Avoid audiophile status language, unexplained jargon, and long lists of products before diagnosing the bottleneck.

If the user asks to retain the setup in Obsidian, use the user's numbered, hyphenated filenames and an index; keep the note focused on durable configuration and reasoning rather than a transient command log.

## Completion Checklist

- [ ] Goal and use case are clear or the assumption is stated
- [ ] Owned gear and current chain were checked
- [ ] Active endpoint is distinguished from installed/virtual endpoints
- [ ] Impedance, sensitivity, gain, power, and connector claims are not overgeneralized
- [ ] Technical problem is separated from tuning preference
- [ ] Enhancement/DSP stacking is addressed
- [ ] EQ advice includes clipping/loudness/fit caveats
- [ ] Current market claims are verified or explicitly marked unverified
- [ ] No snake oil or unnecessary hardware is pushed
- [ ] A cheaper reversible test and a sensible next step are provided
- [ ] Hearing-safety advice is included when efficient IEMs or high-power outputs are involved

## Common Pitfalls

- Recommending a DAC/amp before asking what the user owns and whether the current chain is loud, clean, and reliable.
- Treating a visible `4.4 mm` connector or adapter as proof of a balanced circuit.
- Assuming FxSound, DTS, or Realtek processing is affecting the target device merely because it is installed.
- Stacking vendor effects, a system EQ, player EQ, and a hardware PEQ while trying to diagnose sound.
- Calling a large target-curve correction “neutral” without considering the user's fit, ears, music, and preference.
- Copying EQ values from snippets or unreadable/rate-limited graphs.
- Confusing bit-perfect routing with an audible improvement in frequency response.
- Using loudness, “more detail,” or a premium price as evidence of better sound without level-matched comparison.
- Claiming a current Thai price or warranty without checking the actual listing and seller.
