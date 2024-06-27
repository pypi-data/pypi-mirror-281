class Result:
    def __init__(self, timestamp, relay_lines):
        self.timestamp = timestamp
        self.relay_lines = relay_lines


class RelayLine:
    def __init__(self, relay_id, bw, nick):
        self.relay_id = relay_id
        self.bw = bw
        self.nick = nick


def parse_tornettools_v3bw(filepath):

    with open(filepath, "r") as f:

        timestamp = int(next(f).strip())

        relay_lines = {}

        for line in f:
            relay_id = None
            bw = None
            nick = None

            kv_pairs = line.split()

            for kv_pair in kv_pairs:
                kv = kv_pair.split('=')

                if len(kv) != 2:
                    raise Exception(f"Unexpected len(kv)={len(kv)} (should be 2) in line {line}!")

                k = kv[0]
                v = kv[1]

                if k == "node_id":
                    relay_id = v.lstrip('$')
                elif k == "bw":
                    bw = int(v)
                elif k == "nick":
                    nick = v

            if not (relay_id and bw and nick):
                raise Exception("Missing one or more of the relay_id, bw, or nick in a relay line!")

            if relay_id in relay_lines:
                raise Exception(f"Relay {relay_id} has duplicate entries!")

            relay_lines[relay_id] = RelayLine(relay_id, bw, nick)

        return Result(timestamp, relay_lines)

