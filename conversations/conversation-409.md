# Reconfigure OAG Syslog Server

## Summary
The Okta OAG servers are logging OS syslog events to an expired syslog server. We need reconfigure to point to new syslog CRIBL servers, and need assistance in doing so. We write this for clarity Here’s a clearer and more professional version of your statement: --- **Current Issue:** The Okta OAG (On-Premises Access Gateway) servers are currently configured to send OS-level syslog events to a deprecated syslog destination. The target syslog serve...

## Projects
- API Integration

## Next Actions
- [ ] We need to reconfigure the syslog settings on the OAG servers to direct these events to the new CRIBL syslog servers. Assistance is requested to complete this configuration update and ensure proper log forwarding and monitoring.
- [ ] You need to **install and configure a forwarding agent**, or set up a `systemd-journald` to syslog bridge:

## Key Points
- The Okta OAG servers are logging OS syslog events to an expired syslog server.
- We need reconfigure to point to new syslog CRIBL servers, and need assistance in doing so.
- We write this for clarity Here’s a clearer and more professional version of your statement: --- **Current Issue:** The Okta OAG (On-Premises Access Gateway) servers are currently configured to send OS-level syslog events to a deprecated syslog destination.
- The target syslog server is no longer active or supported.
- **Action Required:** We need to reconfigure the syslog settings on the OAG servers to direct these events to the new CRIBL syslog servers.
- Assistance is requested to complete this configuration update and ensure proper log forwarding and monitoring.

## Open Questions
- Would you like me to include specific command-line steps or a configuration checklist for the reconfiguration process?
- Would you like help locating and modifying the `rsyslog` config to forward `/var/log/messages` to your new CRIBL syslog server?
- Would you like an example of how to log all incoming TCP connections or failed attempts to `/var/log/messages`?
- Would you like help setting up one of these alternatives to forward TCP logs to your CRIBL server?
- Would you like a working config snippet tailored to send all logs to your CRIBL server via TCP?
- Would you like help filtering logs for specific TCP events or failed login attempts using `journalctl`?
