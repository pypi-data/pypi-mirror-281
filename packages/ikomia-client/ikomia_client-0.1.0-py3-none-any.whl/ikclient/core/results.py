"""Endpoint call results."""

import json
from pathlib import Path
from typing import Generator, List, Optional, Tuple, Union

from PIL.Image import Image

import ikclient.utils.image


class Results:
    """To easily manage endpoint call results."""

    # Image output types
    IMAGE_TYPES = ["image", "image_binary"]

    def __init__(self, uuid: str, inputs: List[dict], outputs: List[dict]):
        """
        Initialize a new object that contains endpoint run results.

        Args:
            uuid: run call uuid
            inputs: raw run inputs
            outputs: endpoint run outputs
        """
        self.uuid = uuid
        self._inputs = inputs
        self._outputs = outputs

    def __len__(self) -> int:
        """
        Get results output length.

        Returns:
            Output length
        """
        return len(self._outputs)

    def get_output_raw(self, index: int) -> Tuple[str, Union[str, dict]]:
        """
        Get raw output type and data from index.

        Args:
            index: output index

        Returns:
            A tuple that contains type and data

        Raises:
            IndexError: when index is out of outputs range
        """
        # Ensure output index exists
        try:
            output = self._outputs[index]
        except IndexError as e:
            # Custom error message if index out of bound
            raise IndexError("Results output index out of range") from e

        # Extract type and data then return
        return next(iter(output.items()))

    def get_output_binary(self, index: int) -> bytes:
        """
        Return image output as binary.

        Args:
            index: output index

        Returns:
            Image as bytes

        Raises:
            ValueError: when output is not an image
        """
        # Get raw type and data
        (output_type, data) = self.get_output_raw(index)

        # Ensure type is image
        if output_type not in self.IMAGE_TYPES:
            raise ValueError(f"Can't get binary output as '{output_type}' is not image type")

        # Decode base64 data and return
        assert isinstance(data, str)
        return ikclient.utils.image.b64_str_to_image_bytes(data)

    def get_output(self, index: int) -> Union[Image, dict]:
        """
        Get a result formatted output.

        Args:
            index: output index

        Returns:
            Output as PIL.Image or Python data
        """
        # Get raw type and data
        (output_type, data) = self.get_output_raw(index)

        # If image type, return a PIL.Image
        if output_type in self.IMAGE_TYPES:
            assert isinstance(data, str)
            return ikclient.utils.image.b64_str_to_pil_image(data)

        # Otherwise return as python data
        assert isinstance(data, dict)
        return data

    def get_outputs(self) -> Generator[Union[Image, dict], None, None]:
        """
        Get all results outputs.

        Yields:
            Formatted output as Image or Python data
        """
        for output in self._outputs:
            for output_type, data in output.items():
                if output_type in self.IMAGE_TYPES:
                    yield ikclient.utils.image.b64_str_to_pil_image(data)
                else:
                    yield data

    # To get Results output, pythonic way
    __iter__ = get_outputs

    def save_output(self, index: int, directory: Path, filename: Optional[str] = None):
        """
        Save output to directory / filename.

        Args:
            index: Output index to save
            directory: Directory to save output
            filename: Filename to use to save output. If None, craft one from uuid and index
        """
        # Get output
        output = self.get_output(index)

        # Craft filename from uuid and index, if needed
        if filename is None:
            extension = "json"
            if isinstance(output, Image):
                assert output.format is not None
                extension = output.format.lower()
            filename = f"{self.uuid}_{index}.{extension}"

        # Save to file
        with open(directory / filename, "wb") as f:
            if isinstance(output, Image):
                # Prefer to use original binary given by server, as PIL Image
                #  can re-compress or transform binary when using Image.save()
                f.write(self.get_output_binary(index))
            else:
                f.write(json.dumps(output).encode("UTF-8"))

    def save_outputs(self, directory: Path):
        """
        Save all outputs to directory.

        Args:
            directory: directory to save outputs
        """
        for i in range(len(self._outputs)):
            self.save_output(i, directory)

    def get_input_raw(self, index: int) -> Tuple[str, Union[str, dict]]:
        """
        Get raw intput type and data from index.

        Args:
            index: input index

        Returns:
            A tuple that contains type and data

        Raises:
            IndexError: when index is out of inputs range
        """
        # Ensure input index exists
        try:
            input_ = self._inputs[index]
        except IndexError as e:
            # Custom error message if index out of bound
            raise IndexError("Results input index out of range") from e

        # Extract type and data then return
        return next(iter(input_.items()))

    def get_input_binary(self, index: int) -> bytes:
        """
        Return image input as binary.

        Args:
            index: input index

        Returns:
            Image as bytes

        Raises:
            ValueError: when input is not an image
        """
        # Get raw type and data
        (input_type, data) = self.get_input_raw(index)

        # Ensure type is image
        if input_type not in self.IMAGE_TYPES:
            raise ValueError(f"Can't get binary input as '{input_type}' is not image type")

        # Decode base64 data and return
        assert isinstance(data, str)
        return ikclient.utils.image.b64_str_to_image_bytes(data)

    def get_input(self, index: int) -> Union[Image, dict]:
        """
        Get a result formatted input.

        Args:
            index: input index

        Returns:
            Input as PIL.Image or Python data
        """
        # Get raw type and data
        (input_type, data) = self.get_input_raw(index)

        # If image type, return a PIL.Image
        if input_type in self.IMAGE_TYPES:
            assert isinstance(data, str)
            return ikclient.utils.image.b64_str_to_pil_image(data)

        # Otherwise return as python data
        assert isinstance(data, dict)
        return data

    def get_inputs(self) -> Generator[Union[Image, dict], None, None]:
        """
        Get all results inputs.

        Yields:
            Formatted input as Image or Python data
        """
        for input_ in self._inputs:
            for input_type, data in input_.items():
                if input_type in self.IMAGE_TYPES:
                    yield ikclient.utils.image.b64_str_to_pil_image(data)
                else:
                    yield data
