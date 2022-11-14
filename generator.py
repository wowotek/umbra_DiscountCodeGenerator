import hashlib as HL
import uuid, base64, datetime
import time


def generate_code(previous_card_id: str, *data: list[str]) -> str:
    created = str(datetime.datetime.now().strftime("%d%m%yT%H:%M:%S"))
    uid = str(uuid.uuid4()).replace("-", "")
    joined_data = previous_card_id + uid + "." + created + "." + ".".join(data)

    s = HL.shake_256(bytes(joined_data, "utf-8")).hexdigest(8)
    for _ in range(100000):
        s = HL.shake_256(bytes(s, "utf-8")).hexdigest(8)
        s = HL.shake_256(bytes(s + previous_card_id + time.time(), "utf-8"))

    n = 4
    sliced = [str(int(s[i:i+n], 16)).rjust(5, "0") for i in range(0, len(s), n)]
    return sliced, s
