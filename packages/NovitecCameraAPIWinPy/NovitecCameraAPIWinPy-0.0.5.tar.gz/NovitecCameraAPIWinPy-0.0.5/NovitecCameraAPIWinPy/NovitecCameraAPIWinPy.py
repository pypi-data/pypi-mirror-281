import os
import ctypes
from ctypes import *
from typing import Tuple

# Determine the path to the DLLs directory
dll_path = os.path.join(os.path.dirname(__file__), '_internal')

# Load the DLL files
novitec_camera_apic = ctypes.windll.LoadLibrary(os.path.join(dll_path, 'NOVITECCAMERAAPIC.dll'))

# Define the callback function type for device disconnect event
CallBackDisconnect = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
# Docstring for CallBackDisconnect
"""
CallBackDisconnect is a ctypes function type for device disconnect event callbacks.

This type defines a callback function that takes a single void pointer argument and returns nothing.
It is used to specify the signature of the callback functions that can be registered with 
the SetDeviceDisconnectEventCallback method.

The callback function should match this type to ensure compatibility with the underlying C library.

.. note::
    The callback function should match this type to ensure compatibility with the underlying C library.
    Failure to do so may result in undefined behavior or crashes. Always ensure that the callback function
    signature is compatible with `CallBackDisconnect`.

"""


class CError(ctypes.Structure):
    """
    Structure representing an error.

    .. tip::
        On success, the ``errCode`` will be 0.

    Attributes
    ----------
    errCode : int
        Error code.
    errMessage : char *
        Error message.

    """
    _fields_ = [
        ("errCode", ctypes.c_int),
        ("errMessage", ctypes.c_char_p)
    ]


class CImage(ctypes.Structure):
    """
    Structure representing an image.

    Attributes
    ----------
    width : int
        Image width.
    height : int
        Image height.
    bpp : int
        Bits per pixel.
    timestamp : unsigned int
        Timestamp of the image.
    frameNum : unsigned int
        Frame number.
    payloadType : int
        Payload type.
    pixelFormat : int
        Pixel format.
    dataSize : unsigned int
        Size of the data.
    data : POINTER(c_ubyte)
        Pointer to the image data.
    """
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("bpp", ctypes.c_int),
        ("timestamp", ctypes.c_uint),
        ("frameNum", ctypes.c_uint),
        ("payloadType", ctypes.c_int),
        ("pixelFormat", ctypes.c_int),
        ("dataSize", ctypes.c_uint),
        ("data", ctypes.POINTER(ctypes.c_ubyte)),
    ]


class DiscoverDeviceInfo(ctypes.Structure):
    """
    Structure representing discovered device information.

    Attributes
    ----------
    modelName : bytes (32 bytes)
        Model name of the device.
    serialNumber : bytes (16 bytes)
        Serial number of the device.
    firmwareVersion : bytes (32 bytes)
        Firmware version of the device.
    macAddress : bytes (6 bytes)
        MAC address of the device.
    ipAddress : bytes (4 bytes)
        IP address of the device.
    subnetMask : bytes (4 bytes)
        Subnet mask of the device.
    defaultGateway : bytes (4 bytes)
        Default gateway of the device.
    isNetworkCompatible : bool (1 byte)
        Network compatibility status.

    Example
    -------
    .. code-block:: python

        def print_device_info(info):
            print(f"  Model Name        : {info.modelName.decode().strip()}")
            print(f"  Serial Number     : {info.serialNumber.decode().strip()}")
            print(f"  Firmware Version  : {info.firmwareVersion.decode().strip()}")
            print(f"  MAC Address       : {':'.join(f'{b:02x}' for b in info.macAddress)}")
            print(f"  IP Address        : {'.'.join(str(b) for b in info.ipAddress)}")
            print(f"  Subnet Mask       : {'.'.join(str(b) for b in info.subnetMask)}")
            print(f"  Default Gateway   : {'.'.join(str(b) for b in info.defaultGateway)}")
            is_network_compatible = "Yes" if info.isNetworkCompatible else "No"
            print(f"  Network Compatible: {is_network_compatible}")

    """
    _fields_ = [
        ("modelName", ctypes.c_char * 32),
        ("serialNumber", ctypes.c_char * 16),
        ("firmwareVersion", ctypes.c_char * 32),
        ("macAddress", ctypes.c_ubyte * 6),
        ("ipAddress", ctypes.c_ubyte * 4),
        ("subnetMask", ctypes.c_ubyte * 4),
        ("defaultGateway", ctypes.c_ubyte * 4),
        ("isNetworkCompatible", ctypes.c_bool)
    ]


class NovitecCamera:
    """
    A class for controlling Novitec cameras.

    This class provides methods to interact with and control Novitec cameras.
    Key functionalities include device discovery, connection, control, start and stop operations,
    and image capture.
    """

    def __init__(self):
        self.callback_disconnect = None

        self.lib = novitec_camera_apic
        self.lib.Discover.argtypes = [ctypes.POINTER(ctypes.c_uint)]
        self.lib.Discover.restype = CError

        self.lib.GetDeviceInfo.argtypes = [ctypes.c_uint, ctypes.POINTER(DiscoverDeviceInfo)]
        self.lib.GetDeviceInfo.restype = CError

        self.lib.SendForceIP.argtypes = [ctypes.c_uint]
        self.lib.SendForceIP.restype = CError

        self.lib.ConnectBySerialNumber.argtypes = [ctypes.c_char_p]
        self.lib.ConnectBySerialNumber.restype = CError

        self.lib.Start.argtypes = []
        self.lib.Start.restype = CError

        self.lib.Stop.argtypes = []
        self.lib.Stop.restype = CError

        self.lib.Disconnect.argtypes = []
        self.lib.Disconnect.restype = CError

        self.lib.GetImage.argtypes = [ctypes.POINTER(CImage)]
        self.lib.GetImage.restype = CError

        self.lib.SetFeatureValueInt.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.lib.SetFeatureValueInt.restype = CError

        self.lib.SetFeatureValueFloat.argtypes = [ctypes.c_char_p, ctypes.c_float]
        self.lib.SetFeatureValueFloat.restype = CError

        self.lib.SetFeatureValueEnum.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.SetFeatureValueEnum.restype = CError

        self.lib.SetFeatureValueString.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.SetFeatureValueString.restype = CError

        self.lib.ExecuteFeature.argtypes = [ctypes.c_char_p]
        self.lib.ExecuteFeature.restype = CError

        self.lib.WriteMemory.argtypes = [ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
        self.lib.WriteMemory.restype = CError

        self.lib.GetFeatureValueInt.argtypes = [ctypes.c_char_p, POINTER(ctypes.c_int)]
        self.lib.GetFeatureValueInt.restype = CError

        self.lib.GetFeatureValueFloat.argtypes = [ctypes.c_char_p, POINTER(ctypes.c_float)]
        self.lib.GetFeatureValueFloat.restype = CError

        self.lib.GetFeatureValueEnum.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.GetFeatureValueEnum.restype = CError

        self.lib.GetFeatureValueString.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.GetFeatureValueString.restype = CError

        self.lib.GetFeatureMinMaxValueInt.argtypes = [ctypes.c_char_p, POINTER(ctypes.c_int), POINTER(ctypes.c_int)]
        self.lib.GetFeatureMinMaxValueInt.restype = CError

        self.lib.GetFeatureMinMaxValueFloat.argtypes = [ctypes.c_char_p, POINTER(ctypes.c_float), POINTER(ctypes.c_float)]
        self.lib.GetFeatureMinMaxValueFloat.restype = CError

        self.lib.SetDeviceDisconnectEventCallback.argtypes = [CallBackDisconnect, ctypes.c_void_p]
        self.lib.SetDeviceDisconnectEventCallback.restype = CError

    def discover(self) -> Tuple[CError, int]:
        """
        Discovers devices.

        Returns
        -------
        Tuple[CError, int]
            A tuple containing the result of the discovery operation and the number of devices found.
        """
        num_of_device = ctypes.c_uint()
        result = self.lib.Discover(ctypes.byref(num_of_device))
        return result, num_of_device.value

    def get_device_info(self, device_index: int) -> Tuple[CError, DiscoverDeviceInfo]:
        """
        Retrieves device information by index.

        .. note::
            The ``discover()`` function must be called before.

        Parameters
        ----------
        device_index : int
            The index of the device to retrieve information for.

        Returns
        -------
        Tuple[CError, DiscoverDeviceInfo]
            A tuple containing the result of the operation and the device information.
        """
        device_info = DiscoverDeviceInfo()
        result = self.lib.GetDeviceInfo(ctypes.c_uint(device_index), ctypes.byref(device_info))
        return result, device_info

    def send_force_ip(self, device_index: int) -> CError:
        """
        Sends a Force IP command.

        Sends a command to change the device's IP information.
        This feature is used to set a random IP in the same range as the PC's network IP when the device and PC network IP ranges do not match.

        .. note::
            The ``discover()`` function must be called before.

        Parameters
        ----------
        device_index : int
            The index of the device to which the command is sent.

        Returns
        -------
        CError
            The result of the connection operation.
        """
        result = self.lib.SendForceIP(ctypes.c_uint(device_index))
        return result

    def connect_by_serial_number(self, serial_number: str) -> CError:
        """
        Connects to a device using its serial number.

        .. note::
            The ``discover()`` function must be called before.

        Parameters
        ----------
        serial_number : str
            The serial number of the device to connect to.

        Returns
        -------
        CError
            The result of the connection operation.
        """
        result = self.lib.ConnectBySerialNumber(serial_number.encode("utf-8"))
        return result

    def start(self) -> CError:
        """
        Start grabbing images from a camera.

        Returns
        -------
        CError
            The result of the start operation.
        """
        result = self.lib.Start()
        return result

    def stop(self) -> CError:
        """
        Stop grabbing images from a camera.

        Returns
        -------
        CError
            The result of the stop operation.
        """
        result = self.lib.Stop()
        return result

    def disconnect(self) -> CError:
        """
        Disconnects from the device.

        Returns
        -------
        CError
            The result of the disconnect operation.
        """
        result = self.lib.Disconnect()
        return result

    def get_image(self) -> Tuple[CError, CImage]:
        """
        Get an image from the frame buffer.

        .. note::
            The ``start()`` function must be called before.

        Returns
        -------
        Tuple[CError, CImage]
            A tuple containing the result of the operation and the image.
        """
        image = CImage()
        result = self.lib.GetImage(ctypes.byref(image))
        return result, image

    def set_feature_value_int(self, feature_name: str, value: int) -> CError:
        """
        Sets an integer feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to set.
        value : int
            The integer value to set.

        Returns
        -------
        CError
            The result of the set operation.
        """
        result = self.lib.SetFeatureValueInt(feature_name.encode("utf-8"), ctypes.c_int(value))
        return result

    def set_feature_value_float(self, feature_name: str, value: float) -> CError:
        """
        Sets a float feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to set.
        value : float
            The float value to set.

        Returns
        -------
        CError
            The result of the set operation.
        """
        result = self.lib.SetFeatureValueFloat(feature_name.encode("utf-8"), ctypes.c_float(value))
        return result

    def set_feature_value_enum(self, feature_name: str, value: str) -> CError:
        """
        Sets an enum feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to set.
        value : str
            The enum value to set.

        Returns
        -------
        CError
            The result of the set operation.
        """
        result = self.lib.SetFeatureValueEnum(feature_name.encode("utf-8"), value.encode("utf-8"))
        return result

    def set_feature_value_string(self, feature_name: str, value: str) -> CError:
        """
        Sets a string feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to set.
        value : str
            The string value to set.

        Returns
        -------
        CError
            The result of the set operation.
        """
        result = self.lib.SetFeatureValueString(feature_name.encode("utf-8"), value.encode("utf-8"))
        return result

    def execute_feature(self, feature_name: str) -> CError:
        """
        Executes a feature.

        Parameters
        ----------
        feature_name : str
            The name of the feature to execute.

        Returns
        -------
        CError
            The result of the execute operation.
        """
        result = self.lib.ExecuteFeature(feature_name.encode("utf-8"))
        return result

    def write_memory(self, address: int, data, length: int) -> CError:
        """
        Write memory to device.

        Parameters
        ----------
        address : int
            The address to write to.
        data : int, float, str, or bytes
            The data to write.
        length : int
            The length of the data to write.

        Returns
        -------
        CError
            The result of the write operation.
        """
        if isinstance(data, int):
            data_c = ctypes.c_int(data)
            data_ptr = ctypes.byref(data_c)
        elif isinstance(data, float):
            data_c = ctypes.c_float(data)
            data_ptr = ctypes.byref(data_c)
        elif isinstance(data, str):
            data_bytes = data.encode('utf-8')
            data_c = ctypes.create_string_buffer(data_bytes)
            length = len(data_bytes)
            data_ptr = data_c
        elif isinstance(data, bytes):
            data_c = ctypes.create_string_buffer(data)
            data_ptr = data_c
        else:
            result = CError()
            result.errCode = -1
            result.errMessage = b"Unsupported data type"
            return result

        result = self.lib.WriteMemory(ctypes.c_uint(address), data_ptr, ctypes.c_uint(length))
        return result

    def get_feature_value_int(self, feature_name: str) -> Tuple[CError, int]:
        """
        Gets an integer feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to get.

        Returns
        -------
        Tuple[CError, int]
            A tuple containing the result of the get operation and the integer value.
        """
        c_int_value = ctypes.c_int()
        result = self.lib.GetFeatureValueInt(feature_name.encode("utf-8"), ctypes.byref(c_int_value))
        return result, c_int_value.value

    def get_feature_value_float(self, feature_name: str) -> Tuple[CError, float]:
        """
        Gets a float feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to get.

        Returns
        -------
        Tuple[CError, float]
            A tuple containing the result of the get operation and the float value.
        """
        c_float_value = ctypes.c_float()
        result = self.lib.GetFeatureValueFloat(feature_name.encode("utf-8"), ctypes.byref(c_float_value))
        return result, c_float_value.value

    def get_feature_value_enum(self, feature_name: str) -> Tuple[CError, str]:
        """
        Gets an enum feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to get.

        Returns
        -------
        Tuple[CError, str]
            A tuple containing the result of the get operation and the enum value.
        """
        symbolic_value = ctypes.create_string_buffer(128)
        result = self.lib.GetFeatureValueEnum(feature_name.encode("utf-8"), symbolic_value)
        return result, symbolic_value.value.decode('utf-8').strip()

    def get_feature_value_string(self, feature_name: str) -> Tuple[CError, str]:
        """
        Gets a string feature value.

        Parameters
        ----------
        feature_name : str
            The name of the feature to get.

        Returns
        -------
        Tuple[CError, str]
            A tuple containing the result of the get operation and the string value.
        """
        string_value = ctypes.create_string_buffer(256)
        result = self.lib.GetFeatureValueString(feature_name.encode("utf-8"), string_value)
        return result, string_value.value.decode('utf-8').strip()

    def get_feature_min_max_value_int(self, feature_name: str) -> Tuple[CError, int, int]:
        """
        Gets the minimum and maximum values of an integer feature.

        Parameters
        ----------
        feature_name : str
            The name of the feature to get the min and max values for.

        Returns
        -------
        Tuple[CError, int, int]
            A tuple containing the result of the get operation and the min and max integer values.
        """
        c_min = ctypes.c_int()
        c_max = ctypes.c_int()
        result = self.lib.GetFeatureMinMaxValueInt(feature_name.encode("utf-8"), ctypes.byref(c_min), ctypes.byref(c_max))
        return result, c_min.value, c_max.value

    def get_feature_min_max_value_float(self, feature_name: str) -> Tuple[CError, float, float]:
        """
        Gets the minimum and maximum values of a float feature.

        Parameters
        ----------
        feature_name : str
            The name of the feature to get the min and max values for.

        Returns
        -------
        Tuple[CError, float, float]
            A tuple containing the result of the get operation and the min and max float values.
        """
        c_min = ctypes.c_float()
        c_max = ctypes.c_float()
        result = self.lib.GetFeatureMinMaxValueFloat(feature_name.encode("utf-8"), ctypes.byref(c_min), ctypes.byref(c_max))
        return result, c_min.value, c_max.value

    def set_device_disconnect_event_callback(self, callback_disconnect: CallBackDisconnect) -> CError:
        """
        Sets the callback function for device disconnect events.

        This method registers a callback function that will be called whenever the device
        is disconnected. The callback function must match the signature defined by
        `CallBackDisconnect`, which takes a single void pointer argument.

        Parameters
        ----------
        callback_disconnect : CallBackDisconnect
            The callback function to be called when the device disconnects. This function
            should be defined to match the `CallBackDisconnect` type signature.

        Returns
        -------
        CError
            The result of the operation, indicating whether the callback was successfully
            registered. The specific error codes and their meanings should be referred to
            in the library's documentation.

        Example
        -------
        .. code-block:: python

            def disconnect_callback(param: ctypes.c_void_p):
                print("Device disconnected:", param)

            result = novitec_camera.set_device_disconnect_event_callback(CallBackDisconnect(disconnect_callback))
            if result == CError.SUCCESS:
                print("Callback set successfully")
            else:
                print("Failed to set callback, error code:", result)

        Notes
        -----
        The callback function should match this type to ensure compatibility with the underlying C library.
        Failure to do so may result in undefined behavior or crashes. Always ensure that the callback function
        signature is compatible with `CallBackDisconnect`.
        """
        # Store the callback reference to avoid garbage collection
        self.callback_disconnect = callback_disconnect
        # Call the library function to set the callback
        return self.lib.SetDeviceDisconnectEventCallback(self.callback_disconnect, ctypes.c_void_p(None))
