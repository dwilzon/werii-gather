# Assign AD groups to app

## Summary
use okta oie api to assign about too ad groups to an application Got it—here’s the quickest way to assign (AD-synced) groups to an app via the Okta **Identity Engine** management APIs. # 1) What endpoint to use Use the **Application Groups** endpoint to assign a group to an app: ``` PUT /api/v1/apps/{appId}/groups/{groupId} ``` - Scope needed (OAuth 2.0): `okta.apps.manage` - Optional body lets you set **priority** or a per-assignment **profile**...

## Projects
- API Integration

## Next Actions
- [ ] Review conversation manually

## Key Points
- use okta oie api to assign about too ad groups to an application Got it—here’s the quickest way to assign (AD-synced) groups to an app via the Okta **Identity Engine** management APIs.
- # 1) What endpoint to use Use the **Application Groups** endpoint to assign a group to an app: ``` PUT /api/v1/apps/{appId}/groups/{groupId} ``` - Scope needed (OAuth 2.0): `okta.apps.manage` - Optional body lets you set **priority** or a per-assignment **prof
- If you omit it, Okta auto-assigns the next priority.
- citeturn1view0 > Note: You can assign *directory-sourced* (AD) groups to an app the same way you do Okta-mastered groups.
- The only limitation is you can’t change **membership** of APP_GROUP/AD groups via the Groups API; but you *can* use them for app assignment.
- citeturn0search11 # 2) Get the IDs you need - **Get the appId** (example: by label): `GET /api/v1/apps?filter=label eq "Your App Label"` (Apps API).

## Open Questions
- None
