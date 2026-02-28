# JWT Issuer Configuration Issue

## Summary
jwt issuer is not configured postman warning The **"JWT issuer is not configured"** warning in **Postman** typically appears when you're using **JWT authentication** in an **OAuth 2.0 token request** or **Pre-request script**, and Postman can't verify or locate the `iss` (issuer) value from your JWT against a known configuration. ### Common Causes: 1. **Missing or Incorrect `iss` claim** in the JWT. 2. **No configuration of the JWT issuer** under...

## Projects
- JWT Issuer Configuration Issue

## Next Actions
- [ ] If you're using **Postman’s OAuth 2.0 helper**, you may need to properly configure:

## Key Points
- jwt issuer is not configured postman warning The **"JWT issuer is not configured"** warning in **Postman** typically appears when you're using **JWT authentication** in an **OAuth 2.0 token request** or **Pre-request script**, and Postman can't verify or locat
- ### Common Causes: 1.
- **Missing or Incorrect `iss` claim** in the JWT.
- **No configuration of the JWT issuer** under Postman's "Authorization" tab or environment.
- **Attempting to decode a JWT without context** (Postman doesn’t know the trusted issuer).
- --- ### How to Fix It: #### Option 1: Check JWT Format and Issuer Make sure your JWT payload includes a valid `iss` (issuer) claim: ```json { "iss": "https://your-auth-server.com/", ...

## Open Questions
- Would you like help debugging the specific JWT you're using?
