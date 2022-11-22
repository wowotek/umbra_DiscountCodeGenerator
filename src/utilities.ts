import crypto from "crypto";


function generateNewSalt() {
    const buf = new Array<string>();
    for(let j=0; j<32; j++) {
        const randoms = new Array<string>(); 
        for(let i=0; i<8192; i++) {
            randoms.push(crypto.randomBytes(8192).toString("hex"));
        }
        const random_data = randoms.join();

        buf.push(crypto.createHash("sha512").update(random_data).digest("hex"))
    }

    return buf.join("")
}

function hashPassword(password: string, salt: string) {
    return crypto.pbkdf2Sync(password, salt, 500000, 128, "sha512").toString("hex")
}

function comparePassword(savedPassword: string, savedSalt: string, plainTextPassword: string) {
    const hashedPlainPassword = await hashPassword(plainTextPassword, savedSalt);
    return hashedPlainPassword == savedPassword;
}


let LOG_ENABLED = false;
enum LOG_LEVEL {
    L_ERROR   = "ERROR",
    L_WARNING = "WARN ",
    L_DEBUG   = "DEBUG",
    L_SUCCESS = "INFO ",
}

function logEnable() {
    LOG_ENABLED = true;
}

function logDisable() {
    LOG_ENABLED = false;
}

function log(level: LOG_LEVEL, ...args: Array<string>) {
    if(!LOG_ENABLED) return;

    let str = "";
    str += level

    for(const i in args) {
        str += i + " ";
    }

    for(let i=0; i<str.length; i++) {
        process.stdout.write(str[i]);
    }

    process.stdout.write("\n");
}

export default {
    generateNewSalt,
    hashPassword,
    comparePassword,

    logEnable,
    logDisable,
    log
}