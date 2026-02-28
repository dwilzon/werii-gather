# Okta interaction_code flow

## Summary
How do I create a postman api call to Okta auth server requiring interaction_code grant type To create a **Postman API call to an Okta Authorization Server** using the **`interaction_code` grant type**, you must follow the **OAuth 2.0 Interaction Code flow** — part of **OAuth 2.1 and the Identity Engine** in Okta. This flow is used for embedded sign-in experiences using the **Okta Identity Engine (OIE)** and replaces the Resource Owner Password f...

## Projects
- API Integration

## Next Actions
- [ ] You need to pass the `interaction_handle` to Okta's **IDX endpoints** (like `/idp/idx/identify`, `/idp/idx/challenge/answer`, etc.) to authenticate the user. This depends on how your org is configured (e.g., password, email, WebAuthn).
- [ ] Create an exception that **does not deny ROPC grant type**
- [ ] To set up **Jamf Pro** to connect to **Okta Identity Engine (OIE)** using the **`interaction_code`** grant type (part of the **OAuth 2.1 Interaction Code Flow**), you'll need to configure both Okta and Jamf to support secure, modern authent

## Key Points
- How do I create a postman api call to Okta auth server requiring interaction_code grant type To create a **Postman API call to an Okta Authorization Server** using the **`interaction_code` grant type**, you must follow the **OAuth 2.0 Interaction Code flow** —
- This flow is used for embedded sign-in experiences using the **Okta Identity Engine (OIE)** and replaces the Resource Owner Password flow.
- --- ### ⚠️ Prerequisites 1.
- **Okta Identity Engine (OIE)** is enabled on your org.
- You have a **Client** (OIDC app) set up with: - **OAuth 2.0** enabled - **Grant types** including `interaction_code`, `authorization_code`, `refresh_token` - **PKCE** enabled 3.
- You must simulate or have a **front-end interaction** (e.g., IDX SDK or authenticator) to initiate the authentication and receive an `interaction_handle`.

## Open Questions
- Would you like an example script that gets the interaction code using Node.js or curl before using Postman?
- Would you like help converting your current flow into the supported **Interaction Code + PKCE flow**?
- Would you like a specific Postman test setup or curl script to simulate the interaction code token exchange part?
