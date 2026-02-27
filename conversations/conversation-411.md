# YubiKey OTP Okta Setup

## Summary
How do I create a yubikey seed file to use with otp and Okta? To create a YubiKey seed file (also called a credential or secret seed) for use with OTP (specifically **TOTP or HOTP**) and integrate it with **Okta**, you need to follow a few steps that involve secure generation, formatting, and provisioning. This is generally done using the **YubiKey Personalization Tool** (deprecated), or **YubiKey Manager (ykman)** for newer versions. Okta suppor...

## Projects
- YubiKey OTP Okta Setup

## Next Actions
- [ ] To create a YubiKey seed file (also called a credential or secret seed) for use with OTP (specifically **TOTP or HOTP**) and integrate it with **Okta**, you need to follow a few steps that involve secure generation, formatting, and provisio
- [ ] You’ll need to create a **seed file** and load it into slot 2 of the YubiKey.
- [ ] For TOTP, you’ll need to configure Okta to accept custom authenticators.

## Key Points
- How do I create a yubikey seed file to use with otp and Okta?
- To create a YubiKey seed file (also called a credential or secret seed) for use with OTP (specifically **TOTP or HOTP**) and integrate it with **Okta**, you need to follow a few steps that involve secure generation, formatting, and provisioning.
- This is generally done using the **YubiKey Personalization Tool** (deprecated), or **YubiKey Manager (ykman)** for newer versions.
- Okta supports **OTP (HOTP)** with YubiKey, but only for the **Yubico OTP mode** or **TOTP (if using as a generic MFA with 3rd-party OTP)**, depending on how you're integrating the device (e.g., into Okta Verify via custom integration or with YubiCloud).
- --- ### 🔐 Overview If you're provisioning a YubiKey for **OTP use with Okta**, you have two main paths: #### Option 1: **Yubico OTP + Okta** - Register the YubiKey’s **public identity** and OTP functionality with **YubiCloud**.
- - Okta supports this natively if you're using YubiKeys in **YubiOTP mode**.

## Open Questions
- How do I create a yubikey seed file to use with otp and Okta?
- Would you like help creating a script to auto-generate and load seed files for multiple YubiKeys?
