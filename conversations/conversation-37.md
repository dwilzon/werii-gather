# Custom profile attribute claim

## Summary
can a custom profile attribute be created in okta oie oauth m2m api app that is accessible to a custom claim? Short answer: **yes, but only in the “right” kind of OAuth app + auth server combo.** More specifically: --- ### 1. Can you add a custom profile attribute on an OAuth/OIDC M2M app? Yes. For OIDC apps (including ones you use for client_credentials / M2M), you can define **custom app profile attributes**: - **Admin Console → Directory → Pro...

## Projects
- API Integration

## Next Actions
- [ ] Review conversation manually

## Key Points
- can a custom profile attribute be created in okta oie oauth m2m api app that is accessible to a custom claim?
- Short answer: **yes, but only in the “right” kind of OAuth app + auth server combo.** More specifically: --- ### 1.
- Can you add a custom profile attribute on an OAuth/OIDC M2M app?
- For OIDC apps (including ones you use for client_credentials / M2M), you can define **custom app profile attributes**: - **Admin Console → Directory → Profile Editor** - Filter **Apps** - Click your **OIDC/OAuth app profile** - Click **Add Attribute** and defi
- Can that attribute be used in a custom claim for M2M tokens?
- Also yes — **if you’re using a Custom Authorization Server**, not the org AS.

## Open Questions
- can a custom profile attribute be created in okta oie oauth m2m api app that is accessible to a custom claim?
- ### 1. Can you add a custom profile attribute on an OAuth/OIDC M2M app?
- ### 2. Can that attribute be used in a custom claim for M2M tokens?
