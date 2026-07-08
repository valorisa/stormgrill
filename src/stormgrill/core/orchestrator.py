"""Core orchestrator: agent lifecycle, Hourglass Pipeline, Framing Sentinel, Kill & Fork.

See docs/protocol.md, Branch A (context isolation) and Branch C (resource priority).
"""

# TODO(V0): agent process/task management, throttling.
# TODO(V1): Framing Sentinel — detect explicit pivots in decision-maker input.
# TODO(V1): Kill & Fork — interrupt stale agents, relaunch with new framing.
