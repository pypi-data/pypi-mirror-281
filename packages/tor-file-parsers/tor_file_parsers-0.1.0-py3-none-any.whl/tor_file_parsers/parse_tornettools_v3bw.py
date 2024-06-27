from .v3bw import V3bw
from .line2kv import line_to_kv_pairs


class ParseTornettoolsV3bwException(Exception):
    pass


def parse_tornettools_v3bw(filepath):

    relay_lines = {}

    with open(filepath, "r") as f:

        try:
            timestamp = int(next(f).strip())
        except:
            raise ParseTornettoolsV3bwException(f"Can't parse the timestamp at the first line when parsing the tornettools v3bw at {filepath}")

        for i, line in enumerate(f):

            kv_pairs = line_to_kv_pairs(line)

            if "node_id" not in kv_pairs:
                raise ParseTornettoolsV3bwException(f"Missing the node_id field at line {i + 2} when parsing the tornettools v3bw at {filepath}")
            if "bw" not in kv_pairs:
                raise ParseTornettoolsV3bwException(f"Missing the bw field at line {i + 2} when parsing the tornettools v3bw at {filepath}")
            if "nick" not in kv_pairs:
                raise ParseTornettoolsV3bwException(f"Missing the nick field at line {i + 2} when parsing the tornettools v3bw at {filepath}")

            # Get the relay ID and use it as the key
            # to insert into the relay_lines dict.
            relay_id = kv_pairs["node_id"].lstrip("$")
            if relay_id in relay_lines:
                raise ParseTornettoolsV3bwException(f"Found duplicate relay ID {relay_id} at line {i + 2} when parsing the tornettools v3bw at {filepath}")
            relay_lines[relay_id] = kv_pairs

        if not relay_lines:
            raise ParseTornettoolsV3bwException(f"Got no relay lines when parsing the tornettools v3bw at {filepath}")

        # tornettools v3bw has no header line except the timestamp.
        return V3bw(timestamp, {}, relay_lines)

