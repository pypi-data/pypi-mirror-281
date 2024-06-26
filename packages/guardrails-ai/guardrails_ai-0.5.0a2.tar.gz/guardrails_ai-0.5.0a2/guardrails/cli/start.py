from typing import Optional
import typer

from guardrails.cli.guardrails import guardrails
from guardrails.cli.hub.utils import pip_process
from guardrails.cli.logger import logger


def api_is_installed() -> bool:
    try:
        import guardrails_api  # type: ignore  # noqa

        return True
    except ImportError:
        return False


@guardrails.command()
def start(
    env: Optional[str] = typer.Option(
        default="",
        help="An env file to load environment variables from.",
    ),
    config: Optional[str] = typer.Option(
        default="",
        help="A config file to load Guards from.",
    ),
    timeout: Optional[int] = typer.Option(
        default=5,
        help="Gunicorn worker timeout.",
    ),
    threads: Optional[int] = typer.Option(
        default=10,
        help="Number of Gunicorn worker threads.",
    ),
    port: Optional[int] = typer.Option(
        default=8000,
        help="The port to run the server on.",
    ),
):
    logger.debug("Checking for prerequisites...")
    if not api_is_installed():
        # FIXME: once 0.5.0 is released, and the guardrails-api package is published,
        #   this should be the package name
        # package_name = "guardrails-api"
        package_name = (
            "/Users/calebcourier/Projects/gr-mono/guardrails-cdk/guardrails-api"
        )
        pip_process("install", package_name)

    from guardrails_api.cli.start import start  # type: ignore

    logger.info("Starting Guardrails server")
    start(env, config, timeout, threads, port)
