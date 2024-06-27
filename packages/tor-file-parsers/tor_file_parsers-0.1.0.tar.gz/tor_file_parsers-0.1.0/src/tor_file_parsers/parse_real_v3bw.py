from .v3bw import V3bw
from .line2kv import line_to_kv_pairs


class ParseRealV3bwException(Exception):
    pass


def parse_real_v3bw(filepath):

    header = {}
    relay_lines = {}

    with open(filepath, "r") as f:

        # Parse the timestamp at line 0.
        try:
            timestamp = int(next(f).strip())
        except:
            raise ParseRealV3bwException(f"Can't parse the timestamp at the first line when parsing the real v3bw at {filepath}")

        is_in_header = True

        for i, line in enumerate(f):

            # Parse the separator between the header and relay lines.
            if line == '=====\n':
                is_in_header = False
                continue

            kv_pairs = line_to_kv_pairs(line)

            if is_in_header:
                header = {**header, **kv_pairs}
            else:
                relay_id = kv_pairs["node_id"].lstrip("$")

                if relay_id in relay_lines:
                    raise ParseRealV3bwException(f"Found duplicate relay ID {relay_id} at line {i + 2} when parsing the real v3bw at {filepath}")

                relay_lines[relay_id] = kv_pairs

    if not header:
        raise ParseRealV3bwException(f"Got no header information when parsing the real v3bw at {filepath}.")
    if not relay_lines:
        raise ParseRealV3bwException(f"Got no relay lines when parsing the real v3bw at {filepath}.")

    return V3bw(timestamp, header, relay_lines)

