from __future__ import annotations
from hashlib import shake_256
import datetime
import multiprocessing as mp
import time


DIFFICULTY = 4
HASH_BIT_LENGTH = 32
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

class GiftCard:
    def __init__(self,
        card_number: str,
        use_count: int,
        nonce: int,
        created: float,
        found_nonce_timestamp: float,
        last_signature: str,
        last_found_nonce_timestamp: float,
        last_difficulty: int
    ):

        self.card_number = card_number
        self.use_count = use_count

        self.nonce = hex(nonce).replace("0x", "")
        self.created = time.time() if created == -1 else created

        self.found_nonce_timestamp = found_nonce_timestamp
        self.last_signature = last_signature
        self.last_found_nonce_timestamp = last_found_nonce_timestamp
        self.last_difficulty = last_difficulty
    
    @property
    def signature(self):
        return self.trynonce(self.nonce)[1]

    @property
    def is_valid(self):
        eq = self.signature[-self.difficulty:] == ("0"*self.difficulty)
        mo = self.signature[-(self.difficulty + 1):] == ("0"*(self.difficulty + 1))

        return mo != eq and self.found_nonce_timestamp != -1

    @property
    def difficulty(self):
        if self.created - self.last_found_nonce_timestamp <= 10:
            return self.last_difficulty + 1
        
        if self.created - self.last_found_nonce_timestamp >= 60:
            return self.last_difficulty - 1
        
        if self.created - self.last_found_nonce_timestamp >= 60 * 5:
            return 2
        
        return 1

    def trynonce(self, nonce: int):
        nonce_hex = hex(nonce).replace("0x", "")
        sig = shake_256(bytes(f"{self.last_signature}{self.last_found_nonce_timestamp}{self.last_difficulty}{self.created}{self.card_number}{nonce_hex}", "utf-8")).hexdigest(32)

        eq = sig[-self.difficulty:] == ("0"*self.difficulty)
        mo = sig[-(self.difficulty + 1):] == ("0"*(self.difficulty + 1))

        return eq != mo, sig
    
    def sign(self, nonce: int):
        t = self.trynonce(nonce)
        if t[0]:
            self.nonce = nonce
            self.found_nonce_timestamp = time.time()
            return True, t[1]
        return False, t[1]

    def __str__(self):
        hexint = hex(self.nonce).replace("0x", "")
        x = ["|                    Gift Card",
            f"| DATA ---",
            f"|   Card Number : {self.card_number}",
            f"|   Use Count   : {self.use_count}",
            f"|",
            f"| METADATA ---",
            f"|   nonce       : {hexint}",
            f"|   is valid    : {self.is_valid}",
            f"|   signature   : {self.signature}",
            f"|   prev sign   : {self.last_signature}",
            f"|   difficulty  : {self.difficulty}",
            f"|   sign t      : {datetime.datetime.fromtimestamp(int(self.found_nonce_timestamp), LOCAL_TIMEZONE)}",
            f"|   prev sign t : {self.last_found_nonce_timestamp}",
            f"|   prev diff   : {self.last_difficulty}",
        ]
        m = max([len(i) for i in x])
        pad = ["+"] + [i for i in "-"* (m + 3)] + ["+"]
        for i in range(len(x)):
            d = x[i]
            d = d.ljust(m + 4, " ")
            d += "|"
            x[i] = d
        x.insert(0, "".join(pad))
        x.append("".join(pad))

        return "\n".join(x)
    
    def __repr__(self):
        return self.__str__()


def job_sign(nonce: int): pass



print()
gc = GiftCard("__INIT__", -1, 0, time.time(), -1, "__INIT__", -1, 2)
n = 0
while True:
    r = gc.sign(n)
    t2 = time.time()
    print(*r, n, end="                               \r")

    if r[0]:
        break
    n += 1
print()

print(gc)