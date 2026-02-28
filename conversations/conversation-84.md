# Custom claim in Okta

## Summary
How do I create a custom claim that shows the name of the client credentials / machine to machine app name of the clientid minting a token in okta Here’s the straight answer, no fluff — and this lines up with how Okta behaves under the hood. --- # ✅ Goal You want a **custom claim** in an Okta Authorization Server **access token** that shows the **OAuth client application's name** when the token is minted via **Client Credentials (M2M)**. --- # ⚠️...

## Projects
- IAM Engineering
- API Integration

## Next Actions
- [ ] Review conversation manually

## Key Points
- How do I create a custom claim that shows the name of the client credentials / machine to machine app name of the clientid minting a token in okta Here’s the straight answer, no fluff — and this lines up with how Okta behaves under the hood.
- --- # ✅ Goal You want a **custom claim** in an Okta Authorization Server **access token** that shows the **OAuth client application's name** when the token is minted via **Client Credentials (M2M)**.
- --- # ⚠️ Key Limitation **Okta does *not* expose the client application name as a built-in variable in access-token claims.** You *can* reference the `client_id`, but not the application’s friendly name directly.
- So you cannot do: ``` app.name app.label client.name ``` None of those exist in claims for tokens.
- --- # ✔️ The Supported Way ### **1.
- Create a custom claim** Use your Authorization Server → Claims → Add Claim.

## Open Questions
- None
