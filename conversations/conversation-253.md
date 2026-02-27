# Domain consolidation comparison

## Summary
What are some things that would benefit or hurt a company for consolidating multiple domains to a single domain - compare how it would look moving all users to one domain and forest, or creating a greenfield new domain - knowing that we have legacy applications connected for several years - what benefits would we get for greenfield vs using existing domain - we use Okta for identity in newer apps, but ldap for old apps - and we need to do some di...

## Projects
- Book Writing
- IAM Engineering
- Infrastructure
- API Integration

## Next Actions
- [ ] What are some things that would benefit or hurt a company for consolidating multiple domains to a single domain - compare how it would look moving all users to one domain and forest, or creating a greenfield new domain - knowing that we hav
- [ ] **Reduced cost:** No need to build a brand-new AD forest, migration tooling, or new domain controllers.
- [ ] What foundational activities do we need to do before we even begin looking at doing either consolidation (identity broker) or greenfield
- [ ] Create rules requiring **biometric factor** at device unlock, re-authentication, or app access.
- [ ] If I have no internet access for ODA can I enter Okta Verify code to authenticate or do I need to enter Device Access Code?
- [ ] Would you like me to put together a **decision guide** showing when to use Okta ASA vs. a Thales-style key management approach — e.g., cloud-native vs. legacy/regulatory environments? That’s usually what leadership teams need to pick a stra
- [ ] Tell me what I need to know about SSH in the scenario where Okta and Thales work together
- [ ] **Value:** Eliminates the need to vault, rotate, or distribute static SSH keys.
- [ ] What are some things that would benefit or hurt a company for consolidating multiple domains to a single domain - compare how it would look moving all users to one domain and forest, or creating a greenfield new domain - knowing that we hav
- [ ] **Reduced cost:** No need to build a brand-new AD forest, migration tooling, or new domain controllers.
- [ ] What foundational activities do we need to do before we even begin looking at doing either consolidation (identity broker) or greenfield
- [ ] Create rules requiring **biometric factor** at device unlock, re-authentication, or app access.
- [ ] If I have no internet access for ODA can I enter Okta Verify code to authenticate or do I need to enter Device Access Code?
- [ ] Would you like me to put together a **decision guide** showing when to use Okta ASA vs. a Thales-style key management approach — e.g., cloud-native vs. legacy/regulatory environments? That’s usually what leadership teams need to pick a stra
- [ ] Tell me what I need to know about SSH in the scenario where Okta and Thales work together
- [ ] **Value:** Eliminates the need to vault, rotate, or distribute static SSH keys.
- [ ] What are some things that would benefit or hurt a company for consolidating multiple domains to a single domain - compare how it would look moving all users to one domain and forest, or creating a greenfield new domain - knowing that we hav
- [ ] **Reduced cost:** No need to build a brand-new AD forest, migration tooling, or new domain controllers.
- [ ] What foundational activities do we need to do before we even begin looking at doing either consolidation (identity broker) or greenfield
- [ ] Create rules requiring **biometric factor** at device unlock, re-authentication, or app access.
- [ ] If I have no internet access for ODA can I enter Okta Verify code to authenticate or do I need to enter Device Access Code?
- [ ] Would you like me to put together a **decision guide** showing when to use Okta ASA vs. a Thales-style key management approach — e.g., cloud-native vs. legacy/regulatory environments? That’s usually what leadership teams need to pick a stra
- [ ] Tell me what I need to know about SSH in the scenario where Okta and Thales work together
- [ ] **Value:** Eliminates the need to vault, rotate, or distribute static SSH keys.
- [ ] What are some things that would benefit or hurt a company for consolidating multiple domains to a single domain - compare how it would look moving all users to one domain and forest, or creating a greenfield new domain - knowing that we hav
- [ ] **Reduced cost:** No need to build a brand-new AD forest, migration tooling, or new domain controllers.
- [ ] What foundational activities do we need to do before we even begin looking at doing either consolidation (identity broker) or greenfield
- [ ] Create rules requiring **biometric factor** at device unlock, re-authentication, or app access.
- [ ] If I have no internet access for ODA can I enter Okta Verify code to authenticate or do I need to enter Device Access Code?
- [ ] Would you like me to put together a **decision guide** showing when to use Okta ASA vs. a Thales-style key management approach — e.g., cloud-native vs. legacy/regulatory environments? That’s usually what leadership teams need to pick a stra
- [ ] Tell me what I need to know about SSH in the scenario where Okta and Thales work together
- [ ] **Value:** Eliminates the need to vault, rotate, or distribute static SSH keys.

## Key Points
- What are some things that would benefit or hurt a company for consolidating multiple domains to a single domain - compare how it would look moving all users to one domain and forest, or creating a greenfield new domain - knowing that we have legacy application
- Let’s break it down into a **comparison of two strategies**: 1.
- **Consolidate into an existing domain/forest** 2.
- **Greenfield (build a brand-new domain/forest and migrate)** I’ll highlight **benefits vs risks** for each, and tie in the Okta + LDAP angle.
- Consolidating into an Existing Domain/Forest ### ✅ Benefits - **Lower disruption upfront:** Existing trusts, policies, and connectors stay in place.
- Legacy apps continue to authenticate with minimal changes.

## Open Questions
- - **Workstation/server domain joins**: How many devices are joined to each domain? Where are the dependencies?
- - **Certificates & PKI**: Any AD Certificate Services dependencies? Smartcards?
- - **Password policies**: Do they align across domains?
- - **Provisioning**: Which systems sync from AD → apps vs Okta → apps?
- - **Entitlements model**: Are entitlements based on groups, roles, or manual assignment?
- If I have no internet access for ODA can I enter Okta Verify code to authenticate or do I need to enter Device Access Code?
- # 🔑 What is SSH?
- Would you like me to turn this into a **one-page architecture slide (diagram format, clean and visual)** that you can drop into your GAC deck?
