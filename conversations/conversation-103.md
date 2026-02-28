# Device access code registration

## Summary
how to determine when a user registers device access code Short answer: check the Okta System Log for the Desktop MFA enrollment event. That’s when the user finishes ODA enrollment and their Device Access Code is set. ## Where to look 1) **Okta System Log (Admin Console)** - Filter by event type: ``` eventType eq "device.desktop_mfa.enrollment.create" ``` Optional refinements: ``` and outcome.result eq "SUCCESS" and actor.alternateId eq "user@you...

## Projects
- API Integration

## Next Actions
- [ ] Review conversation manually

## Key Points
- how to determine when a user registers device access code Short answer: check the Okta System Log for the Desktop MFA enrollment event.
- That’s when the user finishes ODA enrollment and their Device Access Code is set.
- ## Where to look 1) **Okta System Log (Admin Console)** - Filter by event type: ``` eventType eq "device.desktop_mfa.enrollment.create" ``` Optional refinements: ``` and outcome.result eq "SUCCESS" and actor.alternateId eq "user@yourdomain.com" ``` This event 
- citeturn3view0 - You may also see periodic **recovery PIN/Device Access Code secret rotations**: ``` eventType eq "device.desktop_mfa.recovery_pin.rotate_secret" ``` These normally occur on a schedule (default ~7 days per user per device) and confirm the de
- citeturn3view0 2) **Programmatic check (API)** - Use the System Log API with the same filter: ``` /api/v1/logs?filter=eventType eq "device.desktop_mfa.enrollment.create" ``` Add `and actor.alternateId eq "user@yourdomain.com"` or filter by device identifier

## Open Questions
- None
