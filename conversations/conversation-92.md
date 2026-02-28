# 802.1X user authentication fix

## Summary
I have Okta Device Access with platform sso configured on my network - there is an issue connecting to 802.1x - How can I connect to 802.1x which requires user authentication to be on the network without not being authenticated yet? Here’s the clean, real explanation of what’s happening with **Okta Device Access (ODA) + Platform SSO** when your network requires **802.1X user-based authentication** before the user is even allowed on the network: -...

## Projects
- 802.1X user authentication fix

## Next Actions
- [ ] Review conversation manually

## Key Points
- I have Okta Device Access with platform sso configured on my network - there is an issue connecting to 802.1x - How can I connect to 802.1x which requires user authentication to be on the network without not being authenticated yet?
- Here’s the clean, real explanation of what’s happening with **Okta Device Access (ODA) + Platform SSO** when your network requires **802.1X user-based authentication** before the user is even allowed on the network: --- # **The Core Problem** 802.1X (EAP-TLS, 
- But ODA’s workflow is: 1.
- macOS/Windows shows **Platform SSO (Okta login)** 3.
- User signs in with Okta 4.
- Device receives tokens 5.

## Open Questions
- I have Okta Device Access with platform sso configured on my network - there is an issue connecting to 802.1x - How can I connect to 802.1x which requires user authentication to be on the network without not being authenticated yet?
