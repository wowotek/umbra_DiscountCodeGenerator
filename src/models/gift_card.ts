import {promisify} from "util";
import child_process from "child_process";

import { Schema, model } from "mongoose";
import crypto from "crypto";
import Utils from "../utilities";

async function _execute(command: string, callback: ((error: child_process.ExecException | null, stdout: string, stderr: string) => void)){
    child_process.exec(
        command,
        { maxBuffer: 1024 * 1024 * 10 },
        ( error, stdout, stderr ) => { callback(error, stdout, stderr) }
    )
}

const execute = promisify(_execute);

export interface IGiftCard {
    card_number: string;
    maximum_usage: number;
    expiration_date: Date;
    creator_admin_username: string;
}

export interface IGiftCardUsage {
    card_number: string;
    usage_admin_username: string;
    used_at: Date;
    user_identifier_username: string;
}

export interface IGiftCardExtension {
    card_number: string;
    extender_admin_username: string;
    usage_extension_count: number;
    expiration_date_add_seconds: number;
    extended_at: Date;
    reason: string;
}


const GiftCardSchema = new Schema({
    card_number: {
        type: String,
        required: true
    },
    maximum_usage: {
        type: Number,
        required: true
    },
    expiration_date: {
        type: Date,
        required: true
    },
    creator_admin_username: {
        type: String,
        required: true
    }
});

const GiftCardUsageSchema = new Schema({
    card_number: {
        type: String,
        required: true
    },
    usage_admin_username: {
        type: String,
        required: true
    },
    used_at: {
        type: Date,
        required: true
    },
    user_identifier_username: {
        type: String,
        required: true,
        default: ""
    }
});

const GiftCardExtensionSchema = new Schema({
    card_number: {
        type: String,
        required: true,
    },
    extender_admin_username: {
        type: String,
        required: true,
    },
    usage_extension_count: {
        type: Number,
        required: true
    },
    expiration_date_add_seconds: {
        type: Number,
        required: true
    },
    extended_at: {
        type: Date,
        required: true,
    },
    reason: {
        type: String,
        required: true,
    },
});

const GiftCardModel = model<IGiftCard>("GiftCard", GiftCardSchema);
const GiftCardUsageModel = model<IGiftCardUsage>("GiftCardUsageExtension", GiftCardUsageSchema);
const GiftCardExtensionModel = model<IGiftCardExtension>("GiftCardExtension", GiftCardExtensionSchema);

function generateGiftCardCardNumber() {
    const random = crypto.randomBytes(512).toString("hex");
    const hashed = crypto.createHash("sha256").update(random).digest("hex").substring(0, 24);

    const chunks = Utils.splitString(hashed, 4, "0", [(a: string) => parseInt(a, 16).toString()]);
    const nchunk = Utils.splitString(chunks.join(""), 5, "0");
    if(nchunk.length > 6) nchunk.pop();
    
    return nchunk.join(" ");
}

console.log(generateGiftCardCardNumber())

class GiftCard implements IGiftCard {
    _id: string;
    id: string;
    card_number: string;
    maximum_usage: number;
    expiration_date: Date;
    creator_admin_username: string;

    constructor(id: string, card_number: string, maximum_usage: number, expiration_date: Date, creator_admin_username: string = "") {
        this._id = id;
        this.id = id;
        this.card_number = card_number;
        this.maximum_usage = maximum_usage;
        this.expiration_date = expiration_date;
        this.creator_admin_username = creator_admin_username;
    }

    public get qrdata() {
        const num = this.card_number.split(" ");
        const hexes = []
        for(const i in num) {
            hexes.push(parseInt(i, 10).toString(16).padStart(5, "0"))
        }

        return hexes.join()
    }

    static async createNew(maximum_usage: number, expiration_date: Date, creator_admin_username: string) {
        const ngc = await new GiftCardModel({
            card_number: generateGiftCardCardNumber(),
            maximum_usage,
            expiration_date,
            creator_admin_username
        }).save();

        return new GiftCard(ngc._id.toString(), ngc.card_number, ngc.maximum_usage, ngc.expiration_date, ngc.creator_admin_username)
    }

    static async fetchOne(card_number: string) {
        const gcm = await GiftCardModel.findOne({card_number});
        if(!gcm) return null;
        const gc = new GiftCard(
            gcm._id.toString(),
            gcm.card_number,
            gcm.maximum_usage,
            gcm.expiration_date,
            gcm.creator_admin_username
        );

        const usages = await GiftCardUsageModel.find({ card_number });
        const extensions = await GiftCardExtensionModel.find({ card_number });

        for(const _ of usages) {
            gc.maximum_usage -= 1;
        }

        for(const extension of extensions) {
            gc.maximum_usage += extension.usage_extension_count;
            gc.expiration_date.setSeconds(gc.expiration_date.getSeconds() + extension.expiration_date_add_seconds);
        }

        return new GiftCard(
            gc._id.toString(),
            gc.card_number,
            gc.maximum_usage,
            gc.expiration_date,
            gc.creator_admin_username
        )
    }

    async extend(
        extender_admin_username: string,
        reason: string,
        seconds: number = 0,
        usage_count: number = 0
    ) {
        if(seconds == 0 && usage_count == 0) return this;
        await new GiftCardExtensionModel({
            card_number: this.card_number,
            extender_admin_username: extender_admin_username,
            usage_extension_count: usage_count,
            expiration_date_add_seconds: seconds,
            extended_at: new Date(),
            reason: reason
        }).save();

        return await GiftCard.fetchOne(this.card_number) as GiftCard
    }

    async use(
        usage_admin_username: string,
        user_identifier_username: string = ""
    ) {
        await new GiftCardUsageModel({
            card_number: this.card_number,
            usage_admin_username: usage_admin_username,
            used_at: new Date(),
            user_identifier_username: user_identifier_username
        }).save();

        return await GiftCard.fetchOne(this.card_number) as GiftCard
    }

    private __last_card_number: string | null = null;
    private __last_execute: Promise<string> | null = null;
    public get giftcardPNG() {
        if(this.__last_card_number == null) this.__last_card_number = this.card_number;
        if(this.card_number == this.__last_card_number && this.__last_execute != null) return this.__last_execute;
        this.__last_execute = execute("py card_png_generator/gen.py --giftcard" + this.card_number);

        return this.__last_execute
    }
}


export default GiftCard;