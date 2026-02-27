# Okta Device Access Authentication

## Summary
Create an architectural diagram for Okta Device Access Windows and Mac authentication with MFA, password reset option, and passwordless # Architecture Diagrams Documentation (v11.1.0+) > In the context of mermaid-js, the architecture diagram is used to show the relationship between services and resources commonly found within the Cloud or CI/CD deployments. In an architecture diagram, services (nodes) are connected by edges. Related services can...

## Projects
- API Integration

## Next Actions
- [ ] Create an architectural diagram for Okta Device Access Windows and Mac authentication with MFA, password reset option, and passwordless

## Key Points
- Create an architectural diagram for Okta Device Access Windows and Mac authentication with MFA, password reset option, and passwordless # Architecture Diagrams Documentation (v11.1.0+) > In the context of mermaid-js, the architecture diagram is used to show th
- In an architecture diagram, services (nodes) are connected by edges.
- Related services can be placed within groups to better illustrate how they are organized.
- ## Example ```mermaid architecture-beta group api(cloud)[API] service db(database)[Database] in api service disk1(disk)[Storage] in api service disk2(disk)[Storage] in api service server(server)[Server] in api db:L -- R:server disk1:T -- B:server disk2:T -- B:
- For supporting components, icons are declared by surrounding the icon name with `()`, while labels are declared by surrounding the text with `[]`.
- To begin an architecture diagram, use the keyword `architecture-beta`, followed by your groups, services, edges, and junctions.

## Open Questions
- group {group id}({icon name})[{title}] (in {parent id})?
- service {service id}({icon name})[{title}] (in {parent id})?
- {serviceId}{{group}}?:{T|B|L|R} {<}?--{>}? {T|B|L|R}:{serviceId}{{group}}?
- junction {junction id} (in {parent id})?
