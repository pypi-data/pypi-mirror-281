# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: PaddlePaddle Authors
"""

import json
import signal

__all__ = [
    'UnsupportedAPIError', 'UnsupportedParamError', 'CalledProcessError',
    'raise_unsupported_api_error', 'raise_key_not_found_error',
    'raise_class_not_found_error', 'raise_unsupported_device_error',
    'DuplicateRegistrationError'
]


class UnsupportedAPIError(Exception):
    """ UnsupportedAPIError """
    pass


class UnsupportedParamError(Exception):
    """ UnsupportedParamError """
    pass


class KeyNotFoundError(Exception):
    """ KeyNotFoundError """
    pass


class ClassNotFoundException(Exception):
    """ ClassNotFoundException """
    pass


class UnsupportedDeviceError(Exception):
    """ UnsupportedDeviceError """
    pass


class CalledProcessError(Exception):
    """ CalledProcessError """

    def __init__(self, returncode, cmd, output=None, stderr=None):
        super().__init__()
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr

    def __str__(self):
        if self.returncode and self.returncode < 0:
            try:
                return f"Command {repr(self.cmd)} died with {repr(signal.Signals(-self.returncode))}."
            except ValueError:
                return f"Command {repr(self.cmd)} died with unknown signal {-self.returncode}."
        else:
            return f"Command {repr(self.cmd)} returned non-zero exit status {self.returncode}."


class DuplicateRegistrationError(Exception):
    """ DuplicateRegistrationError """
    pass


def raise_unsupported_api_error(api_name, cls=None):
    """ raise unsupported api error """
    # TODO: Automatically extract `api_name` and `cls` from stack frame
    if cls is not None:
        name = f"{cls.__name__}.{api_name}"
    else:
        name = api_name
    raise UnsupportedAPIError(f"The API `{name}` is not supported.")


def raise_key_not_found_error(key, config=None):
    """ raise key not found error """
    msg = f"`{key}` not found in config."
    if config:
        config_str = json.dumps(config, indent=4, ensure_ascii=False)
        msg += f"\nThe content of config:\n{config_str}"
    raise KeyNotFoundError(msg)


def raise_class_not_found_error(cls_name, base_cls, all_entities=None):
    """ raise class not found error """
    base_cls_name = base_cls.__name__
    msg = f"`{cls_name}` not registry on {base_cls_name}."
    if all_entities is not None:
        all_entities_str = ",".join(all_entities)
        msg += f"\nThe registied entities:`[{all_entities_str}]`"
    raise ClassNotFoundException(msg)


def raise_unsupported_device_error(device, supported_device=None):
    """ raise_unsupported_device_error """
    msg = f"The device `{device}` is not supported! "
    if supported_device is not None:
        supported_device_str = ", ".join(supported_device)
        msg += f"The supported device types are: [{supported_device_str}]."
    raise UnsupportedDeviceError(msg)
