# Android UAPP + USB DAC Triage

Use when a user connects an Android phone to a USB DAC/dongle and plays a streaming service through USB Audio Player PRO (UAPP) or a similar direct-USB player.

## Establish the path

```text
Android phone → USB-C data/OTG connection → player custom USB driver → USB DAC/amp → headphone/IEM
```

Do not confuse the player's external USB driver with an Android internal Hi-Res driver. The former is the relevant path for an external dongle.

## Clean baseline

1. Unlock the phone and connect the DAC with a known data-capable USB-C cable.
2. Accept the Android USB permission prompt for UAPP.
3. Confirm the DAC name in UAPP and keep `Use USB DAC` enabled.
4. Start with low gain and low hardware volume on the DAC.
5. Set bit-perfect to `When possible`; test `On` only when all tracks are stable and no DSP/EQ is required.
6. Keep UAPP EQ/DSP and resampling off initially.
7. Prefer `Device Native`/automatic sample-rate behavior; test `Variable` if the phone/DAC route behaves better. Never force extreme sample rates merely to obtain a higher indicator.
8. Inspect UAPP's now-playing technical display: source format, bit depth, delivered sample rate, and direct/USB status.

## EQ branch

Bit-perfect playback and player DSP are competing modes. For UAPP ToneBoosters PEQ or another player DSP:

```text
bit-perfect: Off
player PEQ/DSP: On
negative preamp: use when positive filters can clip
```

Do not stack UAPP PEQ, a system-wide Android EQ, and hardware/player EQ until each layer is understood. External Android equalizers may not affect a player that owns the USB stream directly.

## Vendor DSP and spatial-audio decision

Phone controls named Dolby Atmos, Xiaomi Sound, Mi Sound, or spatial audio are vendor DSP choices. They may affect phone speakers, ordinary stereo headphone output, or neither; a direct USB player can bypass them. Test by holding the track and volume constant while toggling one control. A TIDAL Dolby Atmos mix is different from a generic phone Dolby effect, so do not treat the label alone as proof that an immersive stream is reaching the external DAC.

## Format and legacy documentation

UAPP documentation and forum posts may mention MQA because the app historically supported it. Do not assume a current TIDAL stream is MQA. Check the current TIDAL/UAPP display and prefer the currently offered lossless/Hi-Res FLAC path. Do not buy an MQA DAC for this setup.

## Reliability branch

- **No detection:** unlock, reconnect, accept permission, try a data cable, and close other apps that may own the USB device.
- **Clicks/dropouts:** increase the UAPP USB buffer; try `USB tweak 2` only as a troubleshooting step; keep sample rate automatic.
- **Cannot play a format in strict bit-perfect:** change to `When possible` rather than forcing `Always`.
- **Playback stops with the screen off:** set UAPP battery use to `No restrictions`/allow background activity and lock it in recents if the phone's power manager is closing it.
- **Unexpected loudness:** check whether volume is UAPP software volume, USB/device volume, or the DAC's hardware volume; return the DAC to low gain before testing.

## Hardware and safety

A short, flexible USB-C cable reduces mechanical leverage on the phone port; it does not change sound quality. Support the dongle so it does not hang from the port. Do not use charge-only cables or random charge-through splitters. If simultaneous charging is necessary, use a powered hub explicitly designed for USB host/audio plus charging and test it before relying on it.

For efficient IEMs, low gain is the default. High output power is not a reason to increase volume or claim more detail.

## Evidence and verification

UAPP's official site says it supports external USB DACs, a custom USB audio driver, high-resolution formats, and TIDAL integration. Its forum is useful for version/device-specific troubleshooting but is not a substitute for verifying the user's current screen. Record the exact UAPP version, Android/HyperOS version, DAC display, and any error before making a device-specific claim.

Sources:

- https://extreamsd.com/index.php/products/usb-audio-player-pro
- https://extreamsd.com/index.php/uapp-overview
- https://play.google.com/store/apps/details?id=com.extreamsd.usbaudioplayerpro
- https://extreamsd.com/forum/thread-1476.html
- https://extreamsd.com/forum/thread-1515.html
- https://extreamsd.com/forum/thread-1532-post-4208.html
- https://extreamsd.com/forum/showthread.php?tid=779
- https://extreamsd.com/forum/showthread.php?tid=553
- https://www.mi.com/global/product/redmi-note-14-pro-plus-5g/
