import logging
import os
from typing import Any

import click

from datafold_sdk.cli import dbt, alerts, ci, context
from datafold_sdk.cli.context import CliContext
from datafold_sdk.cli.context import DATAFOLD_HOST, DATAFOLD_API_KEY, DATAFOLD_APIKEY
from datafold_sdk.versions import start_fetching_versions, check_newer_version
from datafold_sdk.version import __version__


FORMAT = '%(asctime)-15s:%(levelname)s:%(module)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

logger = logging.getLogger(__file__)


@click.group()
@click.option('--host',
              default="https://app.datafold.com",
              help="The host where the datafold app is located, e.g. 'https://app.datafold.com'")
@click.pass_context
def manager(ctx, host: str, **kwargs):
    """Management script for Datafold CLI"""
    api_key = os.environ.get(DATAFOLD_API_KEY) or os.environ.get(DATAFOLD_APIKEY)
    if not api_key:
        raise ValueError(f"The {DATAFOLD_API_KEY} environment variable is not set")

    override_host = os.environ.get(DATAFOLD_HOST)
    if override_host is not None:
        logger.info(f"Overriding host {host} to {override_host}")
        host = override_host

    start_fetching_versions()
    ctx.obj = CliContext(host=host, api_key=api_key)


@manager.result_callback()
def check_latest_version(result: None, **_: Any) -> None:
    check_newer_version()
    return result


@manager.command()
@click.pass_context
def version(ctx):
    """Displays Datafold CLI version."""
    print(__version__)


manager.add_command(dbt.manager, "dbt")
manager.add_command(alerts.manager, "queries")
manager.add_command(ci.manager, "ci")
