# Okta SAML group behavior

## Summary
In Okta I have a saml application configured with multiple Okta_SSO_ AD groups assigned to the application. I have a group attribute that has a filter "Starts with" Okta_SSO_ - a user logs into the application who is assigned only one AD group in the application, however, Okta is returning all AD groups the user has assigned on his okta profile rather than just in context of the applcication - what is going on here? What you're seeing is expected...

## Projects
- Okta SAML group behavior

## Next Actions
- [ ] ## 🧪 Need to Distinguish AD vs Okta Groups More Explicitly?
- [ ] So if both Okta and AD groups use the same prefix, you can’t distinguish them in expressions — you’d need to:

## Key Points
- In Okta I have a saml application configured with multiple Okta_SSO_ AD groups assigned to the application.
- I have a group attribute that has a filter "Starts with" Okta_SSO_ - a user logs into the application who is assigned only one AD group in the application, however, Okta is returning all AD groups the user has assigned on his okta profile rather than just in c
- What you're seeing is expected behavior based on how Okta evaluates **group attribute statements** in SAML assertions.
- ### 🔍 What's happening: Even though your SAML app is assigned specific AD groups (e.g., those starting with `Okta_SSO_`), **Okta does not scope group attribute statements to only those assigned to the app**.
- Instead, by default: > Okta includes **all groups a user is a member of that match the group filter**, regardless of whether they’re assigned to the app or not.
- So, if the user is a member of multiple `Okta_SSO_` AD groups (in their profile), all of them will be included in the SAML response—even those **not assigned to the app**.

## Open Questions
- In Okta I have a saml application configured with multiple Okta_SSO_ AD groups assigned to the application.  I have a group attribute that has a filter "Starts with" Okta_SSO_ - a user logs into the application who is assigned only one AD g
- ## 🧪 Need to Distinguish AD vs Okta Groups More Explicitly?
