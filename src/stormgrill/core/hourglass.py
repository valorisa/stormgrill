"""Hourglass Pipeline: Storm runs ahead of the Grill while the topic is being framed.

See docs/protocol.md, Branch C — resolves the "simultaneity paradox" via an
ahead-cache instead of blocking the Grill's <8s latency budget.
"""

# TODO(V1): ahead-cache implementation with "verification in progress" fallback state.
