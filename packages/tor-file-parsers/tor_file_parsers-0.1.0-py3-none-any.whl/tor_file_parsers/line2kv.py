from datetime import datetime



class KeyValuePairException(Exception):
    pass



def line_to_kv_pairs(line):

    result = {}

    kv_pairs = line.split()

    for kv_pair in kv_pairs:

        kv = kv_pair.split('=')

        if len(kv) != 2:
            raise KeyValuePairException(f"Unexpected number of tokens ({len(kv)}, should be 2) after splitting by '=', in line: {line}")

        k = kv[0]
        v_ = kv[1]  # Untyped string value.


        # Try to convert v_ to the right type.
        if v_ == "True":
            result[k] = True
            continue
        elif v_ == "False":
            result[k] = False
            continue
        try:
            result[k] = int(v_)
            continue
        except ValueError:
            pass
        try:
            result[k] = float(v_)
            continue
        except ValueError:
            pass
        try:
            result[k] = datetime.fromisoformat(v_)
            continue
        except ValueError:
            pass

        result[k] = v_
        continue

    return result

