from __future__ import annotations
from hashlib import shake_256
import datetime
import time
import uuid, datetime
import os
import utils

import settings as SETTINGS


def generate_code(*data: list[str]) -> str:
    created = str(datetime.datetime.now().strftime("%d%m%yT%H:%M:%S"))
    uid = str(uuid.uuid4()).replace("-", "")
    joined_data = uid + "." + created + "." + ".".join(data)

    s = shake_256(bytes(joined_data, "utf-8")).hexdigest(8)
    for _ in range(1000000):
        s = shake_256(bytes(s, "utf-8")).hexdigest(8)

    n = 4
    sliced = [str(int(s[i:i+n], 16)).rjust(5, "0") for i in range(0, len(s), n)]
    return sliced, s

class SavedUserPasswordChange:
    def parse_user_password_change(user_password_change: str):
        upc = [i for i in user_password_change.replace("USER_PASSWORD_CHANGE", "").replace("(", "")]
        upc.pop()
        upc = [i.split("=")[1] for i in "".join(upc).split(",")]
        upc.pop(0)

        return SavedUser(*upc)
    
    def __init__(self, user_id: str, salt: str, password: str):
        self.user_id = user_id
        self.salt = salt
        self.password = password

class SavedUser:
    def parse_user_registration(user_registration: str):
        ur = [i for i in user_registration.replace("USER_REGISTRATION", "").replace("(", "")]
        ur.pop()
        ur = [i.split("=")[1] for i in "".join(ur).split(",")]

        return SavedUser(*user_registration)
    
    def __init__(self, id: str, username: str, register_date: float, salt: str, password: str):
        self.id = id
        self.username = username
        self.register_date = register_date
        self.salt = salt
        self.password = password

    def change_password(self, saved_user_password_change: SavedUserPasswordChange):
        if saved_user_password_change.user_id != self.id:
            raise Exception("Invalid User ID Provided")
        
        self.salt = saved_user_password_change.salt
        self.password = saved_user_password_change.password

        return True
    
    def __str__(self):
        j = [
            f"",
            f"Saved User",
            f"| id              : {self.id}",
            f"| username        : {self.username}",
            f"| register_date   : {self.register_date}",
            f"| salt            : {self.salt}",
            f"| password        : {self.password}",
            f"+------------------",
        ]

        return "\n".join(j)
    
    def __repr__(self):
        return self.__str__()

class SavedGiftcard:
    def parse_giftcard_creation(gift_card_creation: str):
        gcc = [i for i in gift_card_creation.replace("GIFTCARD_CREATE(", "")]
        gcc.pop()
        gcc = [i.split("=")[1] for i in "".join(gcc).split(",")]

        return SavedGiftcard(*gcc)

    def __init__(self, id: str, card_number: str, maximum_usage: int, creation_date: float, expiration_date: float):
        self.id = id
        self.card_number = card_number
        self.maximum_usage = maximum_usage
        self.creation_date = creation_date
        self.expiration_date = expiration_date
    
    def __str__(self):
        maximum_len = max([len(self.id), len(self.card_number), len(str(self.maximum_usage)), len(str(self.creation_date)), len(str(self.expiration_date))])
        d = [
            "╭―Giftcard――――――――――" + "―"*(60 - maximum_len) + "╮",
            "│ ID              : " + str(self.id)              + " "*(60 - maximum_len - len(str(self.id))) + "│",
            "│ Card Number     : " + str(self.card_number)     + " "*(60 - maximum_len - len(str(self.card_number))) + "│",
            "│ Maximum Usage   : " + str(self.maximum_usage)   + " "*(60 - maximum_len - len(str(self.maximum_usage))) + "│",
            "│ Creation Date   : " + str(self.creation_date)   + " "*(60 - maximum_len - len(str(self.creation_date))) + "│",
            "│ Expiration Date : " + str(self.expiration_date) + " "*(60 - maximum_len - len(str(self.expiration_date))) + "│",
            "╰―――――――――――――――――――" + "―"*(60 - maximum_len) + "╯"
        ]

        return "\n".join(d)
    
    def __repr__(self):
        return self.__str__()

# print(SavedGiftcard.parse_giftcard_creation())
class SavedGiftcardUsage:
    def parse_giftcard_usage(giftcard_usage: str):
        gu = [i for i in giftcard_usage.replace("GIFTCARD_USE(")]
        gu.pop()
        gu = [i.split("=")[1] for i in "".join(gu).split(",")]

        return SavedGiftcardUsage(*gu)
    
    def __init__(self, id: str, used_on: float):
        self.id = id
        self.used_on = used_on

class Activity_UserRegistration:
    def __init__(self, username: str, password: str):
        self.username = username
        self.register_date = time.time()
        self.salt = utils.generate_salt()
        self.password = utils.hash_password(password, self.salt)
        self.id = shake_256(bytes("".join([self.username, self.salt, self.password, str(self.register_date)]), "utf-8")).hexdigest(8)
    
    def get_stringed_data(self):
        return f"USER_REGISTRATION(id={self.id},username={self.username},register_date={self.register_date},salt={self.salt},password={self.password})"

    def __str__(self):
        j = [
            f"USER CREATION",
            f"| id              : {self.id}",
            f"| username        : {self.username}",
            f"| register_date   : {self.register_date}",
            f"| salt            : {self.salt}",
            f"| password        : {self.password}"
        ]

        return "\n".join(j)
    
    def __repr__(self):
        return self.__str__()

class Activity_UserPasswordChange:
    def __init__(self, user_id: str, new_password: str):
        self.user_id = user_id
        self.created = time.time()
        self.new_salt = utils.generate_salt()
        self.new_password = utils.hash_password(new_password, self.new_salt)
    
    def get_stringed_data(self):
        return f"USER_PASSWORD_CHANGE(user_id={self.user_id},created={self.created},new_salt={self.new_salt},new_password={self.new_password})"

    def __str__(self):
        j = [
            f"USER PASSWORD CHANGE",
            f"| user_id         : {self.user_id}",
            f"| created         : {self.created}",
            f"| new_salt        : {self.new_salt}",
            f"| new_password    : {self.new_password}" 
        ]

class Activity_GiftCardCreation:
    def __init__(self, maximum_usage: int, expiration_date: float):
        gc = generate_code()
        self.id = gc[1]
        self.card_number = "-".join(gc[0])
        self.maximum_usage = maximum_usage
        self.creation_date = time.time()
        self.expiration_date = expiration_date
    
    def get_stringed_data(self):
        return f"GIFTCARD_CREATE(id={self.id},card_number={self.card_number},maximum_usage={self.maximum_usage},creation_date={self.creation_date},expiration_date={self.expiration_date})"
    
    def __str__(self):
        j = [
            f"Gift Card Creation",
            f"| id              : {self.id}",
            f"| card_number     : {self.card_number}",
            f"| maximum_usage   : {self.maximum_usage}",
            f"| creation_date   : {self.creation_date}",
            f"| expiration_date : {self.expiration_date}"
        ]

        return "\n".join(j)
    
    def __repr__(self):
        return self.__str__()

class Activity_GiftCardUsage:
    def __init__(self, id: str):
        self.id = id
        self.used_on = time.time()

    def get_stringed_data(self):
        return f"GIFTCARD_USE(id={self.id},used_on={self.used_on})"
    
    def __str__(self):
        j = [
            f"Gift Card Usage",
            f"| id              : {self.id}",
            f"| used_on         : {self.used_on}"
        ]

        return "\n".join(j)
    
    def __repr__(self):
        return self.__str__()

class Block:
    def parse_saved_block(index_number, signature, miner_id, created_date, activities, nonce, last_block_signature, mined_date):
        b = Block(index_number, miner_id, last_block_signature, activities.split("_#_"))
        b.created_date = created_date
        b.nonce = nonce
        b.mined_date = mined_date

        if signature != b.signature:
            raise Exception("Saved signature is not valid with newly created signature")
        
        return b

    def __init__(self, index_number: int, miner_id: str, last_block_signature: str, activities: list[str]):
        self.index_number = index_number
        self.miner_id = miner_id
        self.last_block_signature = last_block_signature
        self.activities = activities
        self.created_date = time.time()
        self.nonce = 0

        self.mined_date = -1

    def get_stringed_data(self, nonce):
        noncehex = hex(nonce).replace("0x", "")
        joined_activities = "_#_".join(self.activities)
        return f"BLOCK(index_number={self.index_number},miner_id={self.miner_id},created={self.created_date},activities={joined_activities},nonce={noncehex},last_block_signature={self.last_block_signature})"
    
    def get_query_safe_data(self):
        return (self.index_number, self.signature, self.miner_id, self.created_date, "_#_".join(self.activities), self.nonce, self.last_block_signature, self.mined_date)

    def get_signature_with_nonce(self, target_nonce: int):
        stringed_data = self.get_stringed_data(target_nonce)
        return shake_256(bytes(stringed_data, "utf-8")).hexdigest(48)

    @property
    def signature(self):
        return self.get_signature_with_nonce(self.nonce)

    @property
    def valid(self):
        return self.try_nonce(self.nonce)[0]
    
    def try_nonce(self, nonce):
        sig = self.get_signature_with_nonce(nonce)
        sig1 = sig[-SETTINGS.DIFFICULTY:]
        sig2 = sig[-(SETTINGS.DIFFICULTY+1):]
        return sig1 == ("0"*SETTINGS.DIFFICULTY) and sig2 != ("0"*(SETTINGS.DIFFICULTY+1)), sig

    def sign(self, nonce):
        if self.try_nonce(nonce)[0]:
            self.nonce = nonce
            self.mined_date = time.time()
            return True
        return False
    
    def __str__(self):
        j = [
            f"Block " + ("- Valid" if self.valid else "- Challange"),
            f"| index_number    : {self.index_number}",
            f"| miner_id        : {self.miner_id}",
            f"| activities      :",
          *[f"|      + " + i.split(",")[0] + ")" for i in self.activities],
            f"| created         : {self.created_date}",
            f"| last_block_sign : {self.last_block_signature}",
            f"| signature       : {self.signature}",
            f"| nonce           : {self.nonce}",
            f"| mined_date      : {self.mined_date}"
        ]
        
        return "\n".join(j)

    def __repr__(self):
        return self.__str__()