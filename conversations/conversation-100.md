# Authorization server audiences

## Summary
how do we provide different audiences for the same authorization server Short answer: in Okta you can’t. A **custom Authorization Server has exactly one Audience** value (the `aud` claim). You can’t emit different `aud` values from the *same* auth server. Here are your workable patterns: 1) One audience per API ⇒ one auth server per API - Create Auth Server A with audience `api://orders` and Auth Server B with `api://billing`. - Each server has i...

## Projects
- API Integration

## Next Actions
- [ ] Create Auth Server A with audience `api://orders` and Auth Server B with `api://billing`.

## Key Points
- how do we provide different audiences for the same authorization server Short answer: in Okta you can’t.
- A **custom Authorization Server has exactly one Audience** value (the `aud` claim).
- You can’t emit different `aud` values from the *same* auth server.
- Here are your workable patterns: 1) One audience per API ⇒ one auth server per API - Create Auth Server A with audience `api://orders` and Auth Server B with `api://billing`.
- - Each server has its own policies, scopes, lifetimes, and keys.
- - Apps call the right issuer when they need a token for that API.

## Open Questions
- GET /oauth2/<authServerId>/v1/authorize?
- Which should you choose?
