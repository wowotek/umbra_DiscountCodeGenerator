import User, { UserLevel } from "../models/user";
import express from "express";
import Utils from "../utilities";
import Auth, { setUserLevelAccess } from "../auth";
import * as Session from "../sessions"

const UserRouter = express.Router();

async function createNewUser(username: string, plainTextPassword: string, full_name: string, user_level: number) {
    const salt = Utils.generateNewSalt();
    const password = Utils.hashPassword(plainTextPassword, salt);
    const user = new User({
        username,
        salt,
        password,
        full_name,
        user_level
    });

    return user;
}

UserRouter.post("/new_employee", Auth.requireApiKey, Auth.requireSession, Auth.setUserLevelAccess([UserLevel.SUPER_ADMIN, UserLevel.ADMIN]), async (req, res) => {
    const username = req.body.username;
    const plainTextPassword = req.body.plainTextPassword;
    const fullname = req.body.fullname;

    const user = (await createNewUser(username, plainTextPassword, fullname, 2)).save();
    res.status(201).json({
        status: "success",
        content: user
    });
});

UserRouter.post("/new_admin", Auth.requireApiKey, Auth.requireSession, Auth.setUserLevelAccess([UserLevel.SUPER_ADMIN]), async (req, res) => {
    const username = req.body.username;
    const plainTextPassword = req.body.plainTextPassword;
    const fullname = req.body.fullname;

    const user = (await createNewUser(username, plainTextPassword, fullname, 1)).save();
    res.status(201).json({
        status: "success",
        content: user
    });
});

UserRouter.post("/new_superadmin", Auth.requireApiKey, Auth.requireSession, Auth.setUserLevelAccess([UserLevel.SUPER_ADMIN]), async (req, res) => {
    const username = req.body.username;
    const plainTextPassword = req.body.plainTextPassword;
    const fullname = req.body.fullname;

    const user = (await createNewUser(username, plainTextPassword, fullname, 0)).save();
    res.status(201).json({
        status: "success",
        content: user
    });
});

UserRouter.post("/register", Auth.requireApiKey, async (req, res) => {
    const username = req.body.username;
    const plainTextPassword = req.body.plainTextPassword;
    const fullname = req.body.fullname;

    const user = (await createNewUser(username, plainTextPassword, fullname, 3)).save();
    res.status(201).json({
        status: "success",
        content: user
    });
})

UserRouter.post("/login", Auth.requireApiKey, async (req, res) => {
    const username = req.body.username;
    const plainTextPassword = req.body.plainTextPassword;

    const user = await User.findOne({ username });
    if(!user) return res.status(401).json({
        status: "user_not_found",
        content: null
    });

    const login = await Session.login(username, plainTextPassword);
    if(!login) return res.status(401).json({
        status: "credentials_invalid",
        content: null
    });

    res.status(200).json({
        status: "success",
        content: {
            session_id: login
        }
    });
});