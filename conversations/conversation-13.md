# Yubico Authenticator error fix

## Summary
error adding fingerprint no such node in yubico authenticator That specific error — **“error adding fingerprint: no such node”** — happens when Yubico Authenticator/Homebrew-installed `python-pyscard`/`libfido2`/`opensc` can’t talk to the Secure Enclave on a **YubiKey Bio** *because macOS thinks it’s a non-bio key*, OR because the **CCID/SmartCard driver is interfering**. This is a *known quirk*, especially on macOS Ventura/Sonoma and YubiKey Bio...

## Projects
- API Integration

## Next Actions
- [ ] Review conversation manually

## Key Points
- error adding fingerprint no such node in yubico authenticator That specific error — **“error adding fingerprint: no such node”** — happens when Yubico Authenticator/Homebrew-installed `python-pyscard`/`libfido2`/`opensc` can’t talk to the Secure Enclave on a *
- This is a *known quirk*, especially on macOS Ventura/Sonoma and YubiKey Bio FIDO Edition.
- Here’s the **quick, practical fix path** — grounded and specific.
- Confirm You’re Using **Yubico Authenticator 6.x** or Newer The fingerprint enrollment API was updated.
- Open Authenticator → *About*.
- If outdated, download fresh: https://www.yubico.com/products/services-software/download/yubico-authenticator/ --- # ✅ 2.

## Open Questions
- None
