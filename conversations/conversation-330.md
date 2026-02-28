# Okta as identity broker

## Summary
How can Okta act as an identity broker when merging 2 separate ad domains on separate forests to a single directory (ad or okta as final directory) Great question. Okta is very good at being the “hub” (identity broker) while you merge two independent AD forests into one target directory—whether that target ends up being a new/consolidated AD or Okta itself (Universal Directory). Here’s the practical way to run it. # The core idea Stand up one Okt...

## Projects
- Book Writing

## Next Actions
- [ ] Review conversation manually

## Key Points
- How can Okta act as an identity broker when merging 2 separate ad domains on separate forests to a single directory (ad or okta as final directory) Great question.
- Okta is very good at being the “hub” (identity broker) while you merge two independent AD forests into one target directory—whether that target ends up being a new/consolidated AD or Okta itself (Universal Directory).
- Here’s the practical way to run it.
- # The core idea Stand up one Okta tenant as the **single IdP for all apps**.
- Connect **both AD forests** to Okta at the same time.
- Okta handles who authenticates where (routing) and keeps identities linked and provisioned while you migrate users and apps in waves.

## Open Questions
- None
