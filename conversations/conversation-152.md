# Force Okta device registration

## Summary
I removed a device from device registration in Okta - Desktop password Sync Authentication - no platformsso-device registration found - how to force new registration Got it — you removed the device from **Device Registration** in Okta, and now your **Desktop Password Sync / Okta Device Access (ODA)** client won’t re-register automatically. Let’s walk through what’s happening and how to force a clean re-registration. --- ### 🔍 What’s Happening Whe...

## Projects
- API Integration

## Next Actions
- [ ] You’ll need to **install or repair the Okta Device Access client**:
- [ ] and I’ll tailor the exact next step (reinstall vs. policy check vs. keychain cleanup).
- [ ] | **Client ID** | You’ll get this from Okta when you add *Platform SSO for macOS* app (see next step). |

## Key Points
- I removed a device from device registration in Okta - Desktop password Sync Authentication - no platformsso-device registration found - how to force new registration Got it — you removed the device from **Device Registration** in Okta, and now your **Desktop P
- Let’s walk through what’s happening and how to force a clean re-registration.
- --- ### 🔍 What’s Happening When a device is removed from **Okta Universal Directory → Devices**, the **local ODA client** (on Windows or macOS) still thinks it’s registered.
- It holds cached tokens and the old `deviceId` locally, so it won’t automatically re-register unless those caches are reset.
- --- ### 💻 To Force New Device Registration #### 🪟 **If Windows** 1.
- **Sign out of the device completely.** 2.

## Open Questions
- Would you like me to tailor exact steps for **Windows** or **macOS** (and note whether this is for **ODA login** or just **Desktop Password Sync**) — so I can include the right registry keys and service names?
- Would you confirm which client(s) you have installed — **Okta Device Access**, **Okta Verify**, or **Okta Desktop Password Sync** — and whether this machine should perform **FastPass login (desktop unlock)** or just **password sync**?
- Would you confirm which package IDs show up under `pkgutil --pkgs | grep -i okta`?
- Would you like me to generate a **ready-to-import Jamf Configuration Profile (XML .mobileconfig)** prefilled for your Okta org domain (`gmfinancial.okta.com`)?
- Would you like me to extract the **expected contents tree** (paths and permissions) from the latest **Okta Verify macOS PKG**, so you can compare what your version installs before pushing via Jamf?
- Would you like me to give you a **ready-to-import Jamf `.mobileconfig`** file for Platform SSO pre-filled with your domain (`gmfinancial.okta.com`)?
- Does com.jamf.appinstalers.OktaVerify do platform sso?
