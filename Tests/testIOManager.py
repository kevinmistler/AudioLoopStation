import unittest
import sounddevice
import AudioLoopStation.io_manager


class Test_ioManager(unittest.TestCase):
    def setUp(self):
        self.io_manager = AudioLoopStation.io_manager.IO_manager()
        self.valid_input = self.io_manager._inputs[0]['index'] if \
            self.io_manager._inputs != [] else 0
        self.valid_output = self.io_manager._outputs[0]['index'] if \
            self.io_manager._outputs != [] else 0

    def tearDown(self):
        AudioLoopStation.io_manager._IO_manager._instance = None

    def test_modify_singleton(self):
        new_io_manger = AudioLoopStation.io_manager.IO_manager()
        new_io_manger._inputs.append("House")
        self.assertListEqual(
            new_io_manger._inputs,
            self.io_manager._inputs
            )

    def test_select_output_valid(self):
        output = self.valid_output
        self.io_manager.select_output(output)

        device = {}
        for d in self.io_manager._outputs:
            if d['index'] == int(output):
                device = d

        self.assertDictEqual(device, self.io_manager._selected_output)

    def test_select_output_wrong_string(self):
        self.assertRaises(
            TypeError,
            self.io_manager.select_output("12haldf@@")
            )

    def test_select_output_empty(self):
        prev_value = self.io_manager._selected_output
        self.io_manager.select_output("")
        self.assertDictEqual(prev_value, self.io_manager._selected_output)

    def test_select_input_valid(self):
        input = self.valid_input
        self.io_manager.select_input(input)

        device = {}
        for d in self.io_manager._inputs:
            if d['index'] == int(input):
                device = d

        self.assertEqual(device, self.io_manager._selected_input)

    def test_select_input_wrong_string(self):
        self.assertRaises(
            TypeError,
            self.io_manager.select_input("12haldf@@")
            )

    def test_select_input_empty(self):
        prev_value = self.io_manager._selected_input
        self.io_manager.select_input("")
        self.assertDictEqual(prev_value, self.io_manager._selected_input)

    def test_parse_input(self):
        device_list = sounddevice.query_devices()
        input_list = self.io_manager._parse_input(device_list)
        self.assertListEqual(input_list, self.io_manager._inputs)

    def test_parse_outputs(self):
        device_list = sounddevice.query_devices()
        output_list = self.io_manager._parse_output(device_list)
        self.assertListEqual(output_list, self.io_manager._outputs)

    def test_get_selected_input(self):
        if self.io_manager._inputs == []:
            self.skipTest("No detected input devices")

        new_input = self.valid_input
        self.io_manager.select_input(new_input)
        self.assertTrue(
            self.io_manager.get_selected_input()['index'] == int(new_input)
            )

    def test_get_selected_output(self):
        if self.io_manager._outputs == []:
            self.skipTest("No detected output devices")

        new_output = self.valid_output
        self.io_manager.select_output(new_output)
        self.assertTrue(
            self.io_manager.get_selected_output()['index'] == int(new_output)
            )
