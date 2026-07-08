"""Typer sub-app for `stormgrill storm`."""

import asyncio
from pathlib import Path

import typer

storm_app = typer.Typer(help="Storm — recherche multi-agents vérifiée.")


@storm_app.command("search")
def search(
    topic: str = typer.Argument(..., help="Sujet de recherche."),
    role: str = typer.Option(  # noqa: B008 - idiomatic typer pattern
        "Lead Architect / Head of AI", "--role", "-r", help="Rôle du lecteur."
    ),
    out: Path = typer.Option(  # noqa: B008 - idiomatic typer pattern
        Path("storm-reports"), "--out", "-o", help="Répertoire de sortie."
    ),
    agents: int = typer.Option(5, "--agents", "-a", help="Nombre d'agents (V0 : toujours 5)."),
) -> None:
    """Lance une recherche Storm sur un sujet et sauvegarde le résultat en JSON."""
    from .pipeline import run_storm, save_result  # local import: keep CLI import light

    typer.echo(f"Storm sur : {topic}")
    typer.echo(f"Rôle du lecteur : {role}")
    if agents != 5:
        typer.echo("Note : V0 exécute toujours le panel fixe de 5 agents.")

    result = asyncio.run(run_storm(topic, role, agents))
    output_file = save_result(result, out)

    typer.echo(f"Résultat sauvegardé : {output_file}")
    typer.echo(f"Résumé de vérification : {result.verification_summary}")
    typer.echo(
        "Rappel V0 : les résumés d'agents sont des placeholders [MOCK] et la "
        "vérification confirme la joignabilité des sources, pas leur contenu. "
        "Voir docs/roadmap.md."
    )
