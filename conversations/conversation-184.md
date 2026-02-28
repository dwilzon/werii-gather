# YubiKey ODA setup

## Summary
How do I setup yubikey for use with ODA - both Windows and Mac - what are the limitations using on each environment Got it 👍 You’re asking how to set up **YubiKey for Okta Device Access (ODA)** on both **Windows** and **Mac**, and what the environment-specific limitations are. I’ll break it down step by step for each OS. --- # 🔑 YubiKey + Okta Device Access (ODA) ## 1. Windows Setup 1. **Pre-reqs** - ODA agent installed on Windows (Okta Device Ac...

## Projects
- Guitar Mastery
- IAM Engineering
- API Integration

## Next Actions
- [ ] First login: they’ll need to enter PIN + tap.
- [ ] 👉 If you’ve confirmed profiles are correct but the **extension still won’t register**, the very next step is to look at the **`com.apple.app-sso` log stream** (step 3). That will usually tell you if macOS is rejecting the profile vs the Okt
- [ ] ## ✅ Next step in your case
- [ ] Perfect — since you **see Okta in `/Applications`**, the app bundle is there. Now we need to check whether it’s the *right* build (ODA-enabled with Platform SSO daemon), and if not, fix it.
- [ ] ## 🛠 Next steps for you
- [ ] 👉 Do you want me to show you exactly how to create that **symlink** step (so you don’t need to hand-edit the plist) and then re-run the daemon bootstrap?
- [ ] ✅ Next step for you:
- [ ] # Use the plist it installs (don’t handcraft one if you don’t need to)
- [ ] First login: they’ll need to enter PIN + tap.
- [ ] 👉 If you’ve confirmed profiles are correct but the **extension still won’t register**, the very next step is to look at the **`com.apple.app-sso` log stream** (step 3). That will usually tell you if macOS is rejecting the profile vs the Okt
- [ ] ## ✅ Next step in your case
- [ ] Perfect — since you **see Okta in `/Applications`**, the app bundle is there. Now we need to check whether it’s the *right* build (ODA-enabled with Platform SSO daemon), and if not, fix it.
- [ ] ## 🛠 Next steps for you
- [ ] 👉 Do you want me to show you exactly how to create that **symlink** step (so you don’t need to hand-edit the plist) and then re-run the daemon bootstrap?
- [ ] ✅ Next step for you:
- [ ] # Use the plist it installs (don’t handcraft one if you don’t need to)
- [ ] First login: they’ll need to enter PIN + tap.
- [ ] 👉 If you’ve confirmed profiles are correct but the **extension still won’t register**, the very next step is to look at the **`com.apple.app-sso` log stream** (step 3). That will usually tell you if macOS is rejecting the profile vs the Okt
- [ ] ## ✅ Next step in your case
- [ ] Perfect — since you **see Okta in `/Applications`**, the app bundle is there. Now we need to check whether it’s the *right* build (ODA-enabled with Platform SSO daemon), and if not, fix it.
- [ ] ## 🛠 Next steps for you
- [ ] 👉 Do you want me to show you exactly how to create that **symlink** step (so you don’t need to hand-edit the plist) and then re-run the daemon bootstrap?
- [ ] ✅ Next step for you:
- [ ] # Use the plist it installs (don’t handcraft one if you don’t need to)

## Key Points
- How do I setup yubikey for use with ODA - both Windows and Mac - what are the limitations using on each environment Got it 👍 You’re asking how to set up **YubiKey for Okta Device Access (ODA)** on both **Windows** and **Mac**, and what the environment-specific
- I’ll break it down step by step for each OS.
- --- # 🔑 YubiKey + Okta Device Access (ODA) ## 1.
- **Pre-reqs** - ODA agent installed on Windows (Okta Device Access for Windows).
- - Okta Identity Engine enabled.
- - YubiKey must be registered with Okta (as a WebAuthn/FIDO2 authenticator).

## Open Questions
- Do you want me to also map this into a **deployment checklist** (practical step-by-step for rolling out across your org), or keep it just at the comparison/setup level?
- Do you want me to also map **how these settings affect login flow specifically in ODA (Windows vs. Mac)**, so you can see what your end-users will actually experience?
- Do you want me to also draft a **user-friendly guide** (screenshots + simple wording) that you can hand to end-users at your org for when you roll out YubiKeys with ODA?
- Do you want me to show what the **login flow looks like in Okta ODA when the PIN is enforced** (Windows vs Mac), so you can see how users will experience it day-to-day?
- when setting up yubikey for fido2 webauthn - is it the Security Key or biometric authenticator security setup?
- Would you like me to also map out **what happens if a user accidentally registers under “biometric authenticator” instead** (so you can explain to helpdesk what to watch for)?
- Do you want me to draft the **exact XML payload structure Jamf needs** for the Okta Platform SSO extension, so you can cross-check against what you pushed?
- 👉 Do you want me to give you the **exact Jamf Configuration Profile payload (SSO Extension XML)** for Okta ODA so you can confirm it’s scoped and landing correctly?
