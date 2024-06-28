# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0110", "0"],  # Binary 0
    ["0101", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding
binary2pulses_mapping = {}

name = "pir1"
type = RFControlProtocolTypes.PIR
brands = []
pulse_lengths = [358, 1095, 11244]
pulse_count = 50


def decode(pulses):
    # Pulses is something like:
    # 01010110010101100110011001100110010101100110011002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 101000001000
    # | 10100 | 00010 |     0 |    0 |
    # |  Unit |    ID | fixed | State|

    # Now we extract the data from that string.
    decoded = {
        "unit": int(binary[0:5], 2),
        "id": int(binary[5:10], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded
