# Windows USB DAC / IEM Triage

Use when auditing a Windows desktop or laptop chain that includes a USB DAC/dongle, an IEM, and optional enhancement software.

## What to establish

Record the chain in order:

```text
source app → Windows endpoint → virtual/DSP layer → physical USB DAC → output connector → IEM/headphone
```

The most important distinction is **present versus active**. A USB DAC can appear in Device Manager while another endpoint is selected for playback. A virtual endpoint can also sit between the app and the physical DAC.

Useful read-only discovery on Windows:

```powershell
Get-PnpDevice -Class AudioEndpoint |
  Select-Object Status, FriendlyName, InstanceId

Get-CimInstance Win32_SoundDevice |
  Select-Object Name, Status, PNPDeviceID
```

Then inspect the audio app's selected output and the enhancement application's saved output target. Do not infer routing from installation alone.

## Neutral baseline

1. Select the physical USB DAC endpoint in **Settings → System → Sound**.
2. Set audio enhancements and spatial audio to Off for the baseline.
3. Bypass FxSound, DTS, Realtek effects, player EQ, and hardware PEQ except for the one layer being tested.
4. Use low gain for an efficient IEM and start at low volume.
5. Compare bypass and processing at closely matched loudness.

If a virtual enhancer is useful for movies or games, keep a named preset for it and a separate neutral music preset. Never diagnose the chain with several unnamed effects enabled.

## Player choice

For general Windows audio, shared mode is convenient because other applications can use the endpoint. For local-file listening, a player such as foobar2000 with official WASAPI output can use exclusive mode. Exclusive mode takes control of the endpoint and may silence other system audio; it is a routing/format choice, not a guaranteed audible tonal improvement.

## Recovery when the result is unexpected

- **No change after EQ installation:** verify that the physical target endpoint was selected in the EQ configurator and that the app is not routed to a virtual endpoint.
- **Movie preset sounds wrong for music:** bypass it and compare against the neutral baseline; a movie preset is intentionally processed.
- **Too loud or fatiguing:** lower gain/volume first; do not use more power to solve a tuning problem.
- **Dropouts or distortion:** temporarily disable enhancement layers, test another supported default format, and update the device driver through normal Windows/device-vendor channels.

## Verification

The audit is complete when the endpoint name, active route, processing layers, gain state, and chosen test preset are all observable and the user can toggle the intended change without losing the baseline.
