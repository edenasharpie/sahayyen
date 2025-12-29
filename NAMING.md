## Event and State Namespacing

All event types and state keys MUST be dot-separated strings.

### Format
`<namespace>.<resource>[.<detail>...]`

### Rules
- The top-level namespace belongs to the plugin emitting it.
- Any plugin may subscribe to events or read state from any namespace.
- Only the owning plugin, however, should write state or emit events to its namespace.
- The following namespaces are reserved by the `core` module:
  - `system.*`
  - `plugin.*`
  - `state.*`

### Examples
- `calendar.upcoming`
- `lights.state`
- `heartbeat.tick`
- `system.startup`