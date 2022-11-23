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
    const hashedPlainPassword = hashPassword(plainTextPassword, savedSalt);
    return hashedPlainPassword == savedPassword;
}

function anyIsNotExist(datas: Array<unknown | null | undefined>) {
    return datas.includes(null) || datas.includes(undefined)
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


function splitString(target_string: string, every_n_char: number, filler: string = "0", filters: Array<(a:string) => string> = [(a) => a]){
    const slen = target_string.length;
    const n = Math.floor(slen / every_n_char);
    const remainder = slen - n;
    const strings = new Array<string>();

    let last_start = 0;
    for(let i=0; i<n; i++){
        strings.push(target_string.substring(last_start, last_start + every_n_char));
        last_start += every_n_char;
    }

    let lastsub = target_string.substring(last_start, last_start + remainder)
    const last_remainder_length = every_n_char - lastsub.length;
    for(let i=0; i<last_remainder_length; i++) {
        lastsub += filler;
    }

    strings.push(lastsub);

    const filtered = new Array<string>();
    for(const filter of filters){
        for(const string of strings) {
            filtered.push(filter(string))
        }
    }

    return filtered;
}

export default {
    generateNewSalt,
    hashPassword,
    comparePassword,
    anyIsNotExist,

    logEnable,
    logDisable,
    log,

    splitString
}