import time

from model import *
import sqlite3


def get_initial_block():
    block = Block(0, "8a8db1f8901145a6", "__INIT__", ["USER_REGISTRATION(id=8a8db1f8901145a6,username=wowotek,register_date=1668527397.5080652,salt=bc526d36b40ecd5f231c0e893497f302,password=f10bb5ff2c1fc647050df75ae1548c45fd31edc1e58a7d6ec0a20b872b2b412c62af53502c9679309cbb0c035ee81d20a313626f326b7a5b3fb62700711b2a7c)"])
    block.created_date = -1
    block.nonce = 2683781
    
    return block

con = sqlite3.connect("BLOCKCHAIN.DBBC")
cur = con.cursor()
print("Initializing Giftcard Database...")
try:
    cur.execute("SELECT * FROM block")
    print("Database Found !")
except sqlite3.OperationalError:
    print("Database Does Not Exist! Creating One...")
    cur.execute("CREATE TABLE block(index_number, signature, miner_id, created_date, activities, nonce, last_block_signature, mined_date)")

if len(cur.execute("SELECT * FROM block").fetchall()) <= 0:
    print("Blockchain is not initialized, Initializing...")
    cur.execute("INSERT INTO block VALUES (?, ?, ?, ?, ?, ?, ?, ?)", get_initial_block().get_query_safe_data())
else:
    print("Blockchain is initialized with", len(all), "data count")


__LOGGED_IN_USER: None | SavedUser = None
__ACTIVITY_POOL: list[str] = []
__STATUS = "idle"
__LAST_BLOCK = None
__CURRENT_CHALLANGE_BLOCK = None
__IS_MINING = False

def activity_user_registration(username: str, password: str):
    for i in get_all_user():
        if i.username == username:
            return False
    
    a = Activity_UserRegistration(username, password)
    __ACTIVITY_POOL.append(a.get_stringed_data())
    return True

def activity_user_password_change(username: str, old_password: str, new_password: str):
    for i in get_all_user():
        if i.username == username:
            if not utils.check_password(i.password, i.salt, old_password):
                return False
            a = Activity_UserPasswordChange(i.id, new_password)
            __ACTIVITY_POOL.append(a.get_stringed_data())
            return True
    return False

def activity_giftcard_creation(maximum_usage: int, expiration_date: float):
    a = Activity_GiftCardCreation(maximum_usage, expiration_date)
    __ACTIVITY_POOL.append(a.get_stringed_data())

    return SavedGiftcard.parse_giftcard_creation(a.get_stringed_data())

def activity_giftcard_usage(id: str):
    gcu = []
    for i in get_all_activities():
        if "GIFTCARD_USE" in i:
            gcu.append(i)
    
def log_in(username: str, password: str):
    global __LOGGED_IN_USER
    for i in get_all_user():
        if i.username == username:
            if utils.check_password(i.password, i.salt, password):
                return True, i
    return False, None

def get_all_giftcard():
    activities = get_all_activities()
    giftcards: list[SavedGiftcard] = []
    use_giftcard: list[SavedGiftcardUsage] = []

    for i in activities:
        if "GIFTCARD_CREATE" in i:
            giftcards.append(SavedGiftcard.parse_giftcard_creation(i))
        if "GIFTCARD_USE" in i:
            use_giftcard.append(SavedGiftcardUsage.parse_giftcard_usage(i))

    for i in giftcards:
        for j in use_giftcard:
            if i.id == j.id:
                i.maximum_usage -= 1
    
    return giftcards

def get_all_user() -> list[SavedUser]:
    activities = get_all_activities()
    user_registrations: list[SavedUser] = []
    user_pass_wchanges: list[SavedUserPasswordChange] = []
    for j in activities:
        if "USER_REGISTRATION" in j:
            user_registrations.append(SavedUser.parse_user_registration(j))
        if "USER_PASSWORD_CHANGE" in j:
            user_pass_wchanges.append(SavedUserPasswordChange.parse_user_password_change(j))
    
    for i in user_registrations:
        for j in user_pass_wchanges:
            if j.user_id == i.id:
                i.change_password(j)
    
    return user_registrations

def get_last_block() -> Block:
    lb = cur.execute("SELECT * FROM block ORDER BY index_number DESC LIMIT 1").fetchone()
    return Block.parse_saved_block(*lb)

def get_all_block() -> list[Block]:
    blockchain = cur.execute("SELECT * FROM block").fetchall()
    return [Block.parse_saved_block(*i) for i in blockchain]

def get_all_activities() -> list[str]:
    blockchain = get_all_block()
    activities: list[str] = []
    for i in blockchain:
        if not i.valid: continue
        for j in i.activities:
            activities.append(j)
    
    return activities

def get_challange() -> Block:
    global __STATUS
    __STATUS = "[0][0] Checking User"
    time.sleep(0.5)
    if __LOGGED_IN_USER == None:
        raise Exception("User not logged in")
    
    __STATUS = "[0][1] Getting Last Block"
    time.sleep(0.5)
    lb = get_last_block()

    __STATUS = "[0][2] Pooling all Activities"
    time.sleep(0.5)
    activities: list[str] = []
    while len(__ACTIVITY_POOL) > 0:
        activities.append(__ACTIVITY_POOL.pop())
    
    __STATUS = "[0][3] Generating Challange Block"
    time.sleep(0.5)
    challange = Block(lb.index_number + 1, __LOGGED_IN_USER.id, lb.signature, activities)

    return challange

def add_to_blockchain(block: Block):
    if not block.valid:
        raise Exception("Block is still invalid!")
    
    cur.execute("INSERT INTO block VALUES (?, ?, ?, ?, ?, ?, ?, ?)", block.get_query_safe_data())

def mining():
    global __STATUS
    while True:
        if not __IS_MINING:
            __STATUS = "[-][-] Idling..."
            time.sleep(2)
            continue

        if __LOGGED_IN_USER == None:
            __STATUS = "[-][-] No User Detected"
            time.sleep(2)
            continue

        __STATUS = "[0][-] Getting Challange Block"
        challange = get_challange()
        time.sleep(0.5)
        
        __STATUS = "[1][0] Mining..."
        nonce = 0
        while not challange.valid:
            __STATUS = "[1][0] Mining... | nonce : " + hex(nonce).replace("0x", "")
            res = challange.try_nonce(nonce)
            if res[0]:
                __STATUS = f"[1][1] Nonce Found at {nonce}, Signing Challange..."
                time.sleep(0.5)
                challange.sign(nonce)
                __STATUS = f"[1][2] Adding {challange.signature[6:]} to Blockchain"
                time.sleep(0.5)
                add_to_blockchain(challange)
                __STATUS = f"[1][3] Waiting for next Challange"
                time.sleep(5)
                break

def start_mining():
    global __IS_MINING
    __IS_MINING = True

def stop_mining():
    global __IS_MINING
    __IS_MINING = False

def get_statuses():
    return __LOGGED_IN_USER, __STATUS, __LAST_BLOCK, __CURRENT_CHALLANGE_BLOCK
