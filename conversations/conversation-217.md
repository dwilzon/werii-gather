# Org2Org configuration in Okta

## Summary
How do I configure org2org application on spoke and idp on hub to first auto provision accounts on hub, and then add a custom attribute and profile mapping that gets pushed from the spoke to the hub in Okta OIE Here’s how you’d configure **Org2Org** in **Okta Identity Engine (OIE)** so that: 1. The **spoke** (acting as the Org2Org app) auto-provisions accounts in the **hub** (acting as the IdP), 2. And then you add a **custom attribute** + **prof...

## Projects
- API Integration

## Next Actions
- [ ] Review conversation manually

## Key Points
- How do I configure org2org application on spoke and idp on hub to first auto provision accounts on hub, and then add a custom attribute and profile mapping that gets pushed from the spoke to the hub in Okta OIE Here’s how you’d configure **Org2Org** in **Okta 
- The **spoke** (acting as the Org2Org app) auto-provisions accounts in the **hub** (acting as the IdP), 2.
- And then you add a **custom attribute** + **profile mapping** that flows from spoke → hub.
- Setup: Spoke → Hub Auto-Provisioning - **On the hub (IdP / target org):** 1.
- Go to **Applications → Applications**.
- Add **“Org2Org”** and set it as a **Service Provider (SP)** app.

## Open Questions
- Would you like me to also draft a **step-by-step Okta Admin Console walk-through with screenshots** (annotated steps for each tab), or a **JSON/terraform example** (for IaC automation with Okta APIs)?
