# Windows Authentication with Okta

## Summary
How to setup Windows Authentication using Okta To set up **Windows Authentication using Okta**, you're typically trying to achieve **Integrated Windows Authentication (IWA)** so users on a corporate network can sign in to Okta (or apps federated through Okta) **without being prompted for credentials**. This is often used in hybrid environments or where seamless SSO is important. There are **two main approaches** depending on your exact architectu...

## Projects
- Windows Authentication with Okta

## Next Actions
- [ ] Create or update a policy that:

## Key Points
- How to setup Windows Authentication using Okta To set up **Windows Authentication using Okta**, you're typically trying to achieve **Integrated Windows Authentication (IWA)** so users on a corporate network can sign in to Okta (or apps federated through Okta) 
- This is often used in hybrid environments or where seamless SSO is important.
- There are **two main approaches** depending on your exact architecture: --- ## ✅ Option 1: **Use Okta IWA Web Agent** ### 🔧 Overview The **Okta IWA Web agent** is a component you install on a Windows Server inside your network that allows domain-joined users t
- --- ### 🧰 Requirements - Windows Server 2016 or later - IIS installed with Windows Authentication enabled - Okta Admin access - Domain-joined environment (Active Directory) --- ### 🛠 Steps #### 1.
- **Prepare the Windows Server** - Join the server to your Active Directory domain.
- - Install **IIS** and enable **Windows Authentication** and **.NET Framework 4.7 or higher**.

## Open Questions
- Would you like help setting this up step-by-step on a specific Windows Server or integrating it with an existing Okta tenant?
- ## 🧩 Want Full Windows Login via Okta?
- Would you like help deploying FastPass across your org or combining this with Windows Hello or FIDO2 keys for hybrid environments?
