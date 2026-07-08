"""Command-line entry point for StormGrill.

V0 scope: `stormgrill storm <topic>` only. Grill and fusion commands
are stubbed pending V1/V2.
"""

import typer

app = typer.Typer(
    name="stormgrill",
    help="Decision Intelligence Orchestrator — Storm (research) + Grill (interrogation).",
)


@app.command()
def storm(
    topic: str = typer.Argument(..., help="Research topic for the Storm run."),
    agents: int = typer.Option(5, help="Number of expert agents to deploy."),
    out: str = typer.Option("reports/", help="Output directory for the report."),
) -> None:
    """Run a Storm research session: N expert agents, Phase 4b verification, HTML report."""
    typer.echo(f"[V0 stub] Would run Storm on '{topic}' with {agents} agents -> {out}")
    raise NotImplementedError("Storm orchestration is not implemented yet. See docs/roadmap.md#v0.")


@app.command()
def grill(
    plan: str = typer.Option(..., help="Path to a YAML file describing the decision plan."),
) -> None:
    """Run an interactive Grill session against a decision plan. (V1)"""
    typer.echo(f"[V1 stub] Would grill plan '{plan}'")
    raise NotImplementedError("Grill module lands in V1. See docs/roadmap.md#v1.")


@app.command()
def fuse(
    storm: str = typer.Option(..., help="Path to a Storm report JSON."),
    grill: str = typer.Option(..., help="Path to a Grill session JSON."),
    out: str = typer.Option("report.html", help="Output path for the fused HTML report."),
) -> None:
    """Fuse a Storm report and a Grill session into a single HTML deliverable. (V2)"""
    typer.echo(f"[V2 stub] Would fuse {storm} + {grill} -> {out}")
    raise NotImplementedError("Fusion module lands in V2. See docs/roadmap.md#v2.")


if __name__ == "__main__":
    app()
