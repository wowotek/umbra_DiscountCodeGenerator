import { Schema } from "mongoose";


export interface IGiftCard {
    card_number: string;
    maximum_usage: number;
    expiration_date: Date;
    creator_admin_username: string;
}

export interface IGiftCardUsage {
    giftcard_card_number: string;
    usage_admin_username: string;
    used_at: Date;
    user_identifier_username: string;
}

export interface IGiftCardExtension {
    giftcard_card_number: string;
    extender_admin_username: string;
    extended_at: Date;
    reason: string;
}

