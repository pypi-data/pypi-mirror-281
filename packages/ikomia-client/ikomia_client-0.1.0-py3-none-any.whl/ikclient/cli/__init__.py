"""Root cli."""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click

import ikclient.cli.rich
from ikclient.core.client import AsyncClient

# Click context settings
CONTEXT_SETTINGS = {"help_option_names": ["--help", "-h"]}


async def run(
    url: str,
    token: str,
    *images: Any,
    task_name: Optional[str] = None,
    parameters: Optional[Dict[str, str]] = None,
    output_directory: Optional[Path] = None,
):
    """
    Run deployment task on images.

    Args:
        url: Deployment URL
        token: An Ikomia Scale API valid token
        *images: Image sources. Can be a path (Python Path or str), Results object, PIL Image or raw bytes
        task_name: A task name to run. If None use default task
        parameters: Task parameters
        output_directory: A path to save run results

    Raises:
        Exception: When something wrong happen on task run
    """
    async with AsyncClient(url, token=token) as client:

        # Get context
        context = await client.build_context()

        # Get final task name if unset
        if task_name is None:
            workflow = await client.get_workflow()
            task_name = workflow.get_first_final_task_name()

        # Add parameters if needed
        if parameters is not None:
            context.set_parameters(task_name, parameters)

        # Add default output
        context.add_output(task_name)

        # Run context for each image with progress context
        with ikclient.cli.rich.Progress() as progress:
            for async_run in asyncio.as_completed(
                [client.run_on(context, image, on_progress=progress.on_progress) for image in images]
            ):
                try:
                    results = await async_run
                    if output_directory is not None:
                        results.save_outputs(output_directory)
                    else:
                        ikclient.cli.rich.show_results(results)
                except Exception as e:  # pylint: disable=W0703
                    # If debug enable, let exception raise (and rich display traceback)
                    if logging.root.level == logging.DEBUG:
                        raise

                    # Otherwise try to display it properly, to avoid breaking loop
                    ikclient.cli.rich.show_exception(e)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option("--debug/--no-debug", default=False)
@click.argument("URL")
@click.argument("IMAGE")
@click.argument("IMAGES", nargs=-1)
@click.option("--task-name", help="Task name to run")
@click.option("--parameter", "-p", type=(str, str), multiple=True)
@click.option(
    "--output-directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, path_type=Path),
    help="Save results to output directory",
)
@click.option(
    "--token",
    envvar="IKOMIA_TOKEN",
    help="Ikomia API Token.",
)
def cli(
    url: str,
    image: str,
    images: str,
    task_name: str,
    parameter: List[Tuple[str, str]],
    output_directory: Optional[Path],
    token: str,
    debug: bool,
):
    """
    Run deployment workflow on local images.

    \b
    URL Deployment endpoint url
    IMAGE [IMAGES...] Images to process
    \f  # noqa: D301

    Args:
        url: Deployment endpoint URL
        image: Image to process
        images: Images to process
        task_name: Task name to run
        parameter: Parameter to give to task
        output_directory: Where to save task results (None mean display them)
        token: A valid Ikomia Scale API token
        debug: True to display debug information, False otherwise

    Raises:
        Exception: when something fail on deployment run
    """
    try:
        # Configure logging
        ikclient.cli.rich.logging_config(debug)

        # Run async
        asyncio.run(
            run(
                url,
                token,
                image,
                *images,
                task_name=task_name,
                parameters=dict(parameter),
                output_directory=output_directory,
            )
        )
    except Exception as e:  # pylint: disable=W0703
        # If debug enable, let exception raise (and rich display traceback)
        if logging.root.level == logging.DEBUG:
            raise

        # Otherwise try to display it properly, then exit error
        ikclient.cli.rich.show_exception(e)
        sys.exit(1)


if __name__ == "__main__":
    cli()  # pylint: disable=E1120
