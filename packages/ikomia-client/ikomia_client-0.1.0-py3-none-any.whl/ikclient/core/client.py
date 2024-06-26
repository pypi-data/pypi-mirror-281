"""Manage deployment endpoint connection and remote call."""

import logging
import os
from abc import ABC
from pathlib import Path
from typing import Any, Callable, Generator, List, Optional, Union

from PIL import Image
from yarl import URL

import ikclient.http.auth
import ikclient.utils.image
from ikclient.core.context import Context
from ikclient.core.results import Results
from ikclient.core.workflow import Workflow
from ikclient.http.session import AsyncSession, Session

logger = logging.getLogger(__name__)


class BaseClient(ABC):
    """Base client with common functions."""

    def __init__(self, url: Union[str, URL], token: Optional[str] = None):
        """
        Initialize a new client to call deployment endpoints.

        Args:
            url: Endpoint URL
            token: Ikomia Scale API token. If unset, try to get from 'IKOMIA_TOKEN' environment variable.
        """
        # Parse URL if needed
        if isinstance(url, URL):
            self.url = url
        else:
            self.url = URL(url)

        # Initialize authentication
        token = token if token is not None else os.getenv("IKOMIA_TOKEN")
        assert isinstance(token, str)
        scale_url = URL(os.getenv("IKOMIA_URL", "https://scale.ikomia.ai"))
        self._auth = ikclient.http.auth.ScaleJwtAuth(scale_url, self.url, token)

        # Cache workflow
        self._workflow: Optional[Workflow] = None


def image_to_b64_str(*sources: List[Any]) -> Generator[str, None, None]:
    """
    Convert an images from supported sources to base64 str.

    Args:
        sources: Image sources. Can be a path (Python Path or str), Results object, PIL Image or raw bytes

    Yields:
        Base 64 string of image

    Raises:
        TypeError: when source type is not supported
    """
    for source in sources:

        # If source is Results object, iterate over raw output and yield them
        if isinstance(source, Results):
            for i in range(len(source)):
                (t, image) = source.get_output_raw(i)
                assert t in Results.IMAGE_TYPES
                yield image

        # If PIL Image
        elif isinstance(source, Image.Image):
            yield ikclient.utils.image.pil_image_to_b64_str(source)

        # If Path or path as str, try to read file
        elif isinstance(source, Path):
            yield ikclient.utils.image.image_file_to_b64_str(source)
        elif isinstance(source, str):
            yield ikclient.utils.image.image_file_to_b64_str(Path(source))

        # If raw bytes
        elif isinstance(source, bytes):
            yield ikclient.utils.image.image_bytes_to_b64_str(source)

        else:
            raise TypeError(
                f"Image source can be a Results, a Path, a str, raw bytes or PIL Image, but not a {type(source)}"
            )


class Client(BaseClient):
    """Client object to call deployment endpoint."""

    def __init__(self, url: Union[str, URL], token: Optional[str] = None):
        """
        Initialize a new client to call deployment endpoints.

        Args:
            url: Endpoint URL
            token: Ikomia Scale API token. If unset, try to get from 'IKOMIA_TOKEN' environment variable.
        """
        super().__init__(url, token)
        self._session: Optional[Session] = None

    @property
    def session(self) -> Session:
        """
        Return a well initialized session.

        Returns:
            A session
        """
        if self._session is None:
            self._session = Session(self.url, self._auth)
        return self._session

    def close(self):
        """Close session."""
        if self._session is not None:
            self._session.close()

    def __enter__(self):
        """
        Initialize session when enter on context.

        Returns:
            This client well initialized
        """
        logger.debug("Open session on %s", self.url)
        _ = self.session
        return self

    def __exit__(self, *_):
        """
        Close session when exit from context.

        Args:
            *_: extra arguments give to ContextManager exit function
        """
        logger.debug("Close session on %s", self.url)
        self.close()

    def get_workflow(self) -> Workflow:
        """
        Return deployment workflow.

        Returns:
            Deployment workflow
        """
        if self._workflow is None:
            response = self.session.get("/workflow")
            self._workflow = Workflow(response.json())
        return self._workflow

    def build_context(self) -> Context:
        """
        Get a new and well initialized Context for this deployment endpoint.

        Returns:
            A well initialized Context object.
        """
        workflow = self.get_workflow()
        return Context(workflow)

    def run(self, *images: Any, on_progress: Optional[Callable] = None, **parameters: Union[str, float]) -> Results:
        """
        Run deployment final task on images.

        Args:
            *images: Can be a path to image (Python Path or str), raw bytes or PIL Image
            on_progress: A callable to report run progress
            **parameters: Task parameters

        Returns:
            Run call results
        """
        # Get final task from workflow
        workflow = self.get_workflow()
        task_name = workflow.get_first_final_task_name()

        # Then call run_task
        return self.run_task(task_name, *images, on_progress=on_progress, **parameters)

    def run_task(
        self, task_name: str, *images: Any, on_progress: Optional[Callable] = None, **parameters: Union[str, float]
    ) -> Results:
        """
        Run a deployment task on images.

        Args:
            task_name: Task name to run
            *images: Can be a path to image (Python Path or str), raw bytes or PIL Image
            on_progress: A callable to report run progress
            **parameters: Task parameters

        Returns:
            Run call results
        """
        # Get context
        context = self.build_context()

        # Add parameters if needed
        if len(parameters) > 0:
            context.set_parameters(task_name, parameters)

        # Add default output
        context.add_output(task_name)

        # Run context
        return self.run_on(context, *images, on_progress=on_progress)

    def run_on(self, context: Context, *images: Any, on_progress: Optional[Callable] = None) -> Results:
        """
        Run a call context on images.

        Args:
            context: A run call context (include parameters and wanted outputs)
            *images: Can be a path to image (Python Path or str), raw bytes or PIL Image
            on_progress: A callable to report run progress

        Returns:
            Run call results
        """
        # Craft input list
        inputs = [{"image": b64_str} for b64_str in image_to_b64_str(*images)]

        # Run context and return response
        return self.session.run_on(context, inputs, on_progress=on_progress)


class AsyncClient(BaseClient):
    """Client object to call deployment endpoint, async version."""

    def __init__(self, url: Union[str, URL], token: Optional[str] = None):
        """
        Initialize a new async client to call deployment endpoints.

        Args:
            url: Endpoint URL
            token: Ikomia Scale API token. If unset, try to get from 'IKOMIA_TOKEN' environment variable.
        """
        super().__init__(url, token)
        self._session: Optional[AsyncSession] = None

    @property
    def session(self) -> AsyncSession:
        """
        Return a well initialized session.

        Returns:
            A session
        """
        if self._session is None:
            self._session = AsyncSession(self.url, self._auth)
        return self._session

    async def close(self):
        """Close session."""
        if self._session is not None:
            await self._session.aclose()

    async def __aenter__(self):
        """
        Initialize session when enter on context.

        Returns:
            This client well initialized
        """
        logger.debug("Open session on %s", self.url)
        _ = self.session
        return self

    async def __aexit__(self, *_):
        """
        Close session when exit from context.

        Args:
            *_: extra arguments give to ContextManager exit function
        """
        logger.debug("Close session on %s", self.url)
        await self.close()

    async def get_workflow(self) -> Workflow:
        """
        Return deployment workflow.

        Returns:
            Deployment workflow
        """
        if self._workflow is None:
            response = await self.session.get("/workflow")
            self._workflow = Workflow(response.json())
        return self._workflow

    async def build_context(self) -> Context:
        """
        Get a new and well initialized Context for this deployment endpoint.

        Returns:
            A well initialized Context object.
        """
        workflow = await self.get_workflow()
        return Context(workflow)

    async def run(
        self, *images: Any, on_progress: Optional[Callable] = None, **parameters: Union[str, float]
    ) -> Results:
        """
        Run deployment final task on images.

        Args:
            *images: Can be a path to image (Python Path or str), raw bytes or PIL Image
            on_progress: A callable to report run progress
            **parameters: Task parameters

        Returns:
            Run call results
        """
        # Get final task from workflow
        workflow = await self.get_workflow()
        task_name = workflow.get_first_final_task_name()

        # Then call run_task
        return await self.run_task(task_name, *images, on_progress=on_progress, **parameters)

    async def run_task(
        self, task_name: str, *images: Any, on_progress: Optional[Callable] = None, **parameters: Union[str, float]
    ) -> Results:
        """
        Run a deployment task on images.

        Args:
            task_name: Task name to run
            *images: Can be a path to image (Python Path or str), raw bytes or PIL Image
            on_progress: A callable to report run progress
            **parameters: Task parameters

        Returns:
            Run call results
        """
        # Get context
        context = await self.build_context()

        # Add parameters if needed
        if len(parameters) > 0:
            context.set_parameters(task_name, parameters)

        # Add default output
        context.add_output(task_name)

        # Run context
        return await self.run_on(context, *images, on_progress=on_progress)

    async def run_on(self, context: Context, *images: Any, on_progress: Optional[Callable] = None) -> Results:
        """
        Run a call context on images.

        Args:
            context: A run call context (include parameters and wanted outputs)
            *images: Can be a path to image (Python Path or str), raw bytes or PIL Image
            on_progress: A callable to report run progress

        Returns:
            Run call results
        """
        # Craft input list
        inputs = [{"image": b64_str} for b64_str in image_to_b64_str(*images)]

        # Run context and return response
        return await self.session.run_on(context, inputs, on_progress=on_progress)
