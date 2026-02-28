# YubiKey fingerprint fix

## Summary
yubikey fingerpint registration keeps failing When **YubiKey fingerprint enrollment keeps failing**, it usually comes down to one of four root causes: **firmware version**, **USB power/connection**, **enrollment flow confusion between Yubico Authenticator vs OS**, or **a corrupted/locked FIDO2 biometric slot**. Here’s the clean, direct way to diagnose and fix it: --- # ✅ FIRST — Confirm the right app **Yubico Authenticator does *not* register fin...

## Projects
- YubiKey fingerprint fix

## Next Actions
- [ ] Review conversation manually

## Key Points
- yubikey fingerpint registration keeps failing When **YubiKey fingerprint enrollment keeps failing**, it usually comes down to one of four root causes: **firmware version**, **USB power/connection**, **enrollment flow confusion between Yubico Authenticator vs O
- Here’s the clean, direct way to diagnose and fix it: --- # ✅ FIRST — Confirm the right app **Yubico Authenticator does *not* register fingerprints.** Fingerprints are only handled by the **YubiKey Manager (YubiKey Manager / ykman)**.
- If you’re attempting this inside the *Yubico Authenticator app*, that’s exactly why you see errors like: > “no such node” > “could not add fingerprint” > “biometrics: unsupported” ➡️ **Open “YubiKey Manager” instead**, not YubiKey Authenticator.
- --- # ✅ Step-by-Step Fix ### **1.
- Check the YubiKey’s model** Only these keys support biometrics: - **YubiKey Bio FIDO Edition** - **YubiKey Bio USB-A / USB-C** ➡️ Standard YubiKeys (5 Series, etc.) **do not** support fingerprint registration at all.
- If your key is *not* a Bio model, fingerprint enrollment will always fail.

## Open Questions
- ## 1. Who does what?
- - Greyed-out button?
- - Error?
- - No options at all?
