# YubiKey vs SMS Authentication

## Summary
Explain the following because I'm confused: Unlike the SMS codes or authenticator apps that got compromised in that breach, your YubiKey creates unique signatures each time you authenticate, and the private key never leaves the physical device that sits on your keychain. When you tap your YubiKey, it uses public-key cryptography to prove your identity. Your key stores a secret private key that signs a challenge from the website, while the website...

## Projects
- API Integration

## Next Actions
- [ ] Review conversation manually

## Key Points
- Explain the following because I'm confused: Unlike the SMS codes or authenticator apps that got compromised in that breach, your YubiKey creates unique signatures each time you authenticate, and the private key never leaves the physical device that sits on you
- When you tap your YubiKey, it uses public-key cryptography to prove your identity.
- Your key stores a secret private key that signs a challenge from the website, while the website uses a public key to verify it's really you.
- This makes it mathematically impossible for attackers to fake your identity without physically stealing your key.
- Let’s break this down into simple pieces so it’s clear why YubiKeys are more secure than SMS codes or authenticator apps: --- ### 🔐 **What Happened in That Breach** - Attackers intercepted **SMS codes** or stole **authenticator app tokens** using malware or ph
- - These methods rely on something **you know or can copy**, not something **you physically own**.

## Open Questions
- How does the website get your public key and how exactly does it check the signature to make sure the private key signed it?
- Want a hands-on example in code (like using `openssl` or WebAuthn APIs) to see how this actually works?
- ## 🧪 Want to Try This With Real WebAuthn?
- Would you like a local script or demo webpage that simulates a basic WebAuthn-style interaction with your own key?
