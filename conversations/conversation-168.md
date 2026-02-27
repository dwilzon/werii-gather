# Okta OAuth to Kerberos

## Summary
f5 bigip translate okta oauth access token to kergeros ticket Got it — you want BIG-IP APM to take an Okta OIDC/OAuth login and then get a Kerberos ticket for a legacy app (i.e., OIDC → Kerberos bridge via KCD). Quick truth bomb: you don’t literally “convert” an access token into a Kerberos ticket. Instead, APM validates the Okta token, identifies the user, and then uses Kerberos Constrained Delegation (S4U) to obtain a backend service ticket on...

## Projects
- API Integration

## Next Actions
- [ ] Create the APM delegation service account; set constrained delegation to **only** the backend SPNs (`HTTP/app01.domain`).
- [ ] If you tell me your exact backend target — e.g., *IIS app on Azure VM*, *Azure App Service*, or *legacy internal site behind BIG-IP* — I can show you exactly which SPN you need to register (`setspn`) or whether you can drop Kerberos and do

## Key Points
- f5 bigip translate okta oauth access token to kergeros ticket Got it — you want BIG-IP APM to take an Okta OIDC/OAuth login and then get a Kerberos ticket for a legacy app (i.e., OIDC → Kerberos bridge via KCD).
- Quick truth bomb: you don’t literally “convert” an access token into a Kerberos ticket.
- Instead, APM validates the Okta token, identifies the user, and then uses Kerberos Constrained Delegation (S4U) to obtain a backend service ticket on the user’s behalf.
- citeturn0search9turn0search11turn0search3 ### What you build (high-level) 1.
- **Okta → BIG-IP (OIDC)** - Okta is the IdP.
- Create an OIDC app for BIG-IP (RP).

## Open Questions
- If you tell me your exact backend target — e.g., *IIS app on Azure VM*, *Azure App Service*, or *legacy internal site behind BIG-IP* — I can show you exactly which SPN you need to register (`setspn`) or whether you can drop Kerberos and do 
- Would you like me to draw the full **Okta → BIG-IP → AD → App** certificate + token + KCD diagram showing which cert or key is used at each step?
- Would you like me to generate that image next?
- Would you like me to show a side-by-side flow diagram of **User Context OIDC → KCD** vs **M2M → static service ticket**, so you can show your team *why only the first supports true per-user SSO*?
