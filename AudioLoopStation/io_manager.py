import sounddevice as sd


class _IO_manager:
    """
    Singleton class created to allow IO device interaction as well as
    maintaining IO device state across the application.

    The IO_manager() function should be used to access this class.

    DO NOT directly create an object of this class.
    Examples:

    DON'T   -> my_object = _IO_manager()
    DO      -> my_object = IO_manager()
    """
    _instance = None

    def __init__(self) -> None:
        self._inputs = []
        self._outputs = []
        self._selected_input = {}
        self._selected_output = {}
        self._fetch_IO()

    # Public functions
    def get_inputs(self) -> list[dict]:
        """Returns list of input devices

        Returns:
            list[dict]: list of dicts with the following keys:

            ``'name'``
                The name of the device.
            ``'index'``
                The device index.
            ``'hostapi'``
                The ID of the corresponding host API.
            ``'max_input_channels'``, ``'max_output_channels'``
                The maximum number of input/output channels supported by the
                device.
            ``'default_low_input_latency'``, ``'default_low_output_latency'``
                Default latency values for interactive performance.
            ``'default_high_input_latency'``, ``'default_high_output_latency'``
                Default latency values for robust non-interactive
                applications (e.g. playing sound files).
            ``'default_samplerate'``
                The default sampling frequency of the device.
        """
        return self._inputs

    def get_outputs(self) -> list[dict]:
        """Returns list of output devices

        Returns:
            list[dict]: list of dicts with the following keys:

            ``'name'``
                The name of the device.
            ``'index'``
                The device index.
            ``'hostapi'``
                The ID of the corresponding host API.
            ``'max_input_channels'``, ``'max_output_channels'``
                The maximum number of input/output channels supported by the
                device.
            ``'default_low_input_latency'``, ``'default_low_output_latency'``
                Default latency values for interactive performance.
            ``'default_high_input_latency'``, ``'default_high_output_latency'``
                Default latency values for robust non-interactive
                applications (e.g. playing sound files).
            ``'default_samplerate'``
                The default sampling frequency of the device.
        """
        return self._outputs

    def get_selected_input(self) -> dict:
        """Returns the user selected audio input device. Defaults to
        system default.

        Returns:
            dict: dict with the following keys:

            ``'name'``
                The name of the device.
            ``'index'``
                The device index.
            ``'hostapi'``
                The ID of the corresponding host API.
            ``'max_input_channels'``, ``'max_output_channels'``
                The maximum number of input/output channels supported by the
                device.
            ``'default_low_input_latency'``, ``'default_low_output_latency'``
                Default latency values for interactive performance.
            ``'default_high_input_latency'``, ``'default_high_output_latency'``
                Default latency values for robust non-interactive
                applications (e.g. playing sound files).
            ``'default_samplerate'``
                The default sampling frequency of the device.
        """
        return self._selected_input

    def get_selected_output(self) -> dict:
        """Returns the user selected audio output device. Defaults to
        system default.

        Returns:
            dict: dict with the following keys:

            ``'name'``
                The name of the device.
            ``'index'``
                The device index.
            ``'hostapi'``
                The ID of the corresponding host API.
            ``'max_input_channels'``, ``'max_output_channels'``
                The maximum number of input/output channels supported by the
                device.
            ``'default_low_input_latency'``, ``'default_low_output_latency'``
                Default latency values for interactive performance.
            ``'default_high_input_latency'``, ``'default_high_output_latency'``
                Default latency values for robust non-interactive
                applications (e.g. playing sound files).
            ``'default_samplerate'``
                The default sampling frequency of the device.
        """
        return self._selected_output

    def select_input(self, id: str or int) -> None:
        """Select the audio input that should be used for recording.
        Updates self._selected_input.

        Args:
            id (str or int): id of the device to use for audio input.
            See get_inputs for info regrarding extracting device id.
        """
        if id == "":
            print("Could not save selected input. " +
                  "Wrong type: Requires int or str")
            return

        try:
            converted_id = int(id)
            self._selected_input = self._match_id(self._inputs, converted_id)
        except (ValueError, TypeError, OverflowError):
            print("Could not save selected input. " +
                  "Wrong type: Requires int or str")
            return

    def select_output(self, id: str or int) -> None:
        """Select the audio output.
        Updates self._selected_output.

        Args:
            id (str or int): id of the device to use for audio output.
            See get_outputs for info regrarding extracting device id.
        """
        if id == "":
            print("Could not save selected output. " +
                  "Wrong type: Requires int or str")
            return

        try:
            converted_id = int(id)
            self._selected_output = self._match_id(self._outputs, converted_id)
        except (ValueError, TypeError, OverflowError):
            print("Could not save selected output. " +
                  "Wrong type: Requires int or str")

    # Private functions
    def _fetch_IO(self):
        """Funtion that queries user device for IO devices.
        Updates self._selected_input, self._selected_output,
        self._inputs, and self._outputs.
        """
        fetchedData = sd.query_devices()
        # parse input and save in _inputs
        self._inputs = self._parse_input(fetchedData)
        # parse output and save in _outputs
        self._outputs = self._parse_output(fetchedData)
        # set defaults for input and output -> default.device: (in,out)
        input_id, output_id = sd.default.device
        self._selected_input, self._selected_output = \
            self._grab_defaults(fetchedData, input_id, output_id)

    def _parse_input(
            self,
            fetchedData: sd.DeviceList
            ) -> list[dict]:
        """Function that parses an sd.DeviceList and returns list of
        dicts for each input device.
        """
        input_list = []
        for device in fetchedData:
            if device['max_input_channels'] > 0:
                input_list.append(device)
        return input_list

    def _parse_output(
            self,
            fetchedData: sd.DeviceList
            ) -> list[dict]:
        """Function that parses an sd.DeviceList and returns list of
        dicts for each output device.
        """
        output_list = []
        for device in fetchedData:
            if device['max_output_channels'] > 0:
                output_list.append(device)
        return output_list

    def _grab_defaults(
            self,
            deviceList: list[dict],
            input: int,
            output: int) -> tuple[dict, dict]:
        """function that scans a list of Device dicts and returns
        a tuple of the input and output devices matching the provided
        input and output id int parameters.

        Returns:
            tuple[dict, dict]: (input_device, output_device)
        """
        input_device = {}
        output_device = {}
        for d in deviceList:
            if d['index'] == input:
                input_device = d
            if d['index'] == output:
                output_device = d
        return (input_device, output_device)

    def _match_id(self, device_list: list[dict], id: int) -> dict:
        """Function that checks whether a device matching the provided id
        exists in the provided device list

        Returns:
            dict: Returns dict matching id. Returns empty dict if no matching
            device found.
        """
        match = {}
        for d in device_list:
            if d['index'] == id:
                match = d
                break
        return match


def IO_manager() -> object:
    """Factory function that produces a _IO_manager object.

    Returns:
        _IO_manager object
    """
    if _IO_manager._instance is None:
        _IO_manager._instance = _IO_manager()
    return _IO_manager._instance
