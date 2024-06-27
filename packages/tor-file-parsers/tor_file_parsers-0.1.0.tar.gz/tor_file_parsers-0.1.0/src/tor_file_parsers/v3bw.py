class V3bw:
    def __init__(self, timestamp, header, relay_lines):

        self.timestamp = timestamp

        # This is a dict because each header line seems to be
        # a single key-value pair (except the timestamp).
        self.header = header

        # An dict of relay lines, indexed by relay IDs.
        # Each relay line is also a dict.
        self.relay_lines = relay_lines

