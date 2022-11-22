import { Schema } from "mongoose";


export interface IUser {
    username: string;
    is_admin: boolean;
    registered_at: Date;
}

export interface IUserPasswordSet {
    username: string;
    salt: string;
    password: string;
}

