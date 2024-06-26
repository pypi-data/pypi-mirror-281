"""Override, wrap or embed rich components to display info about endpoint and runs."""

import logging
import time
from typing import Optional, Tuple

import click
import PIL.Image
import rich
import rich.progress
from rich.logging import RichHandler

from ikclient.core.results import Results


def logging_config(debug: bool):
    """
    Configure logging to use rich as handler.

    Args:
        debug: True if we must display debug, False otherwise
    """
    level = logging.INFO
    if debug:
        level = logging.DEBUG
        rich.traceback.install(show_locals=True, suppress=[click])
    logging.basicConfig(level=level, datefmt="[%X]", handlers=[RichHandler()])


class Progress(rich.progress.Progress):
    """Override rich progress to easily manage endpoint runs progress."""

    def __init__(self, *args, **kwargs):
        """
        Initialize new Progress to track endpoint runs progress.

        Args:
            *args: args given to rich.progress.Progress
            **kwargs: kwargs given to rich.progress.Progress
        """
        super().__init__(*args, **kwargs)

        # Store rich progress task by run run_id
        self._runs = {}

    def __enter__(self) -> "Progress":
        """
        Enter on progress context.

        Returns:
            This progress
        """
        self.start()
        return self

    @classmethod
    def get_default_columns(cls) -> Tuple[rich.progress.ProgressColumn, ...]:
        """
        Override get_default_columns to fit with endpoint run progress.

        Returns:
            A tuple of default ProgressColumn
        """
        return (
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.BarColumn(),
            rich.progress.TimeRemainingColumn(compact=True, elapsed_when_finished=True),
        )

    def add_run_task(self, run_id: str, name: str, short_uuid: str, eta_in_ms: Optional[int], state: str):
        """
        Add a new progress task to track endpoint run progress.

        Args:
            run_id: A run unique id
            name: A name to display on progress bar
            short_uuid: An endpoint run uuid (compact version)
            eta_in_ms: A task estimated time of arrival, in ms
            state: Initial run state
        """
        # Add progress task
        task_id = self.add_task(f"[bright_black]{name}[{short_uuid}] {state}", total=eta_in_ms, start=True)

        # Transform ETA in ms to future timestamp
        if eta_in_ms is not None:
            eta = time.time() + eta_in_ms / 1000
        else:
            eta = None

        # Store info about run
        self._runs[run_id] = {
            "task_id": task_id,
            "eta": eta,
            "start": time.time(),
        }

    def update_all(self):
        """Update all run tasks."""
        now = time.time()
        for runs in self._runs.values():
            completed = (now - runs["start"]) * 1000
            self.update(runs["task_id"], completed=completed, refresh=True)

    def on_progress(self, run_id: str, name: str, uuid: str, state: str, eta: Tuple[int, int], **_):
        """
        Endpoint run progress callback function.

        Args:
            run_id: A run unique id
            name: A name to display on progress bar
            uuid: Endpoint run uuid
            state: Endpoint run state (eg: PENDING, SUCCESS, ... )
            eta: A tuple with eta lower bound / upper bound
            **_: Extra and unused parameters
        """
        # Split eta into lower and upper bound
        (eta_lower_bound, eta_upper_bound) = eta

        # Reduce UUID to 8 chars to compact bar description
        if uuid is not None:
            short_uuid = uuid[:8]
        else:
            short_uuid = "--------"

        # Check if it's a new run
        if run_id not in self._runs:
            self.add_run_task(run_id, name, short_uuid, eta_upper_bound, state)
            return

        # If defined, ensure expected ETA is still in bounds
        if eta_upper_bound is not None:

            # Get ETA lower and upper bound as timestamp
            eta_lower_bound_ts = time.time() + eta_lower_bound / 1000
            eta_upper_bound_ts = time.time() + eta_upper_bound / 1000

            # If ETA was previously unset, or if previously calculated ETA is out of new bounds, reset it
            if (
                self._runs[run_id]["eta"] is None
                or self._runs[run_id]["eta"] < eta_lower_bound_ts
                or self._runs[run_id]["eta"] > eta_upper_bound_ts
            ):
                self._runs[run_id]["eta"] = eta_upper_bound_ts
                self.update(
                    self._runs[run_id]["task_id"],
                    total=(self._runs[run_id]["eta"] - self._runs[run_id]["start"]) * 1000,
                )

        # Update description
        description = rich.markup.escape(f"{name}[{short_uuid}] {state}")
        if state == "STARTED":
            description = "[cyan]" + description
        elif state == "SUCCESS":
            description = "[bright_green]" + description
        elif state == "FAILURE":
            description = "[bright_red]" + description
        else:
            description = "[bright_black]" + description
        self.update(self._runs[run_id]["task_id"], description=description)

        # Update all tasks progress
        self.update_all()


def show_results(results: Results):
    """
    Show run Results outputs, e.g. display image and pretty print data as json.

    Args:
        results: A Results object to display outputs
    """
    for result in results:
        if isinstance(result, PIL.Image.Image):
            result.show()
        else:
            rich.print_json(data=result)


def show_exception(e: Exception):
    """
    Display exception properly.

    Args:
        e: Exception to display
    """
    title = e.__class__.__name__
    message = format(e)

    rich.print(
        rich.panel.Panel(
            rich.padding.Padding(message, (1, 1), style="white"),
            title=title,
            width=80,
            border_style="bold red",
        )
    )
