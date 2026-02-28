# Okta Desktop MFA policies

## Summary
What policies does Okta look at to send someone to Desktop MFA policy for ODA in Okta Good question — this is one of the most important but confusing areas in **Okta Device Access (ODA)** when you’re trying to understand **why a user is being prompted for “Desktop MFA”** or not. Let’s break down exactly **which Okta policies and settings determine whether a user is sent to the Desktop MFA policy flow** for ODA (Windows or macOS). --- ### 🔹 1. Pri...

## Projects
- Okta Desktop MFA policies

## Next Actions
- [ ] Review conversation manually

## Key Points
- What policies does Okta look at to send someone to Desktop MFA policy for ODA in Okta Good question — this is one of the most important but confusing areas in **Okta Device Access (ODA)** when you’re trying to understand **why a user is being prompted for “Des
- Let’s break down exactly **which Okta policies and settings determine whether a user is sent to the Desktop MFA policy flow** for ODA (Windows or macOS).
- Primary Okta Policy Sources for ODA Okta evaluates several layers of policy in sequence.
- The key ones involved in sending someone to the **Desktop MFA policy** are: | Policy Type | Purpose | How it Affects ODA Desktop MFA | |--------------|----------|--------------------------------| | **Global Session Policy** | Governs web sessions (browser and 
- | ODA registration and login both use this policy when invoking Okta’s authentication endpoint.
- If it requires MFA for device types or access contexts that match ODA, user will see MFA at device unlock.

## Open Questions
- - Is device registered and known?
- - Does the ODA app’s policy require MFA for this user, device, or zone?
