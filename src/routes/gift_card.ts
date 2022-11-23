import { Router } from "express";
import GiftCard from "../models/gift_card";
import * as Auth from "../auth";
import Utils from "../utilities";

const GiftCardRoute = Router()

GiftCardRoute.post("/generate", Auth.requireApiKey, Auth.requireSession, Auth.setUserLevelAccess([0, 1]), async (req, res) => {
    if(!req.session) return res.status(501).json({ status: "internal_server_error", content: null });
    
    const maximum_usage = req.body.maximum_usage;
    const expiration_date = req.body.expiration_date;
    if(Utils.anyIsNotExist([maximum_usage, expiration_date])) return res.status(400).json({
        status: "field_not_found",
        content: null
    });

    GiftCard
        .createNew(parseInt(maximum_usage), expiration_date, req.session.user_id)
        .then(gc => res.status(201).json({
                status: "success",
                content: {
                    card_number: gc.card_number,
                    maximum_usage: gc.maximum_usage,
                    expiration_date: gc.expiration_date,
                    qrdata: gc.qrdata
                }
            })
        )
});

GiftCardRoute.post("/use", Auth.requireApiKey, Auth.requireSession, Auth.setUserLevelAccess([0, 1, 2]), async (req, res) => {
    if(!req.session) return res.status(501).json({ status: "internal_server_error", content: null });

    const card_number = req.body.card_number;
    const usage_admin_username = req.session.user_id;
    const user_identifier_username = req.body.user_identifier_username ?? "";
    if(Utils.anyIsNotExist([card_number])) return res.status(400).json({
        status: "field_not_found",
        content: null
    });

    const gc = await GiftCard.fetchOne(card_number);
    if(!gc) return res.status(404).json({
        status: "not_found:giftcard",
        content: null
    })

    gc
        .use(usage_admin_username, user_identifier_username)
        .then(gc => res.status(201).json({
            status: "success",
            content: {
                card_number: gc.card_number,
                maximum_usage: gc.maximum_usage,
                expiration_date: gc.expiration_date,
                qrdata: gc.qrdata
            }
        }));
});

GiftCardRoute.post("/extend", Auth.requireApiKey, Auth.requireSession, Auth.setUserLevelAccess([0, 1]), async (req, res) => {
    if(!req.session) return res.status(501).json({ status: "internal_server_error", content: null });

    const card_number = req.body.card_number;
    const extender_admin_username = req.session.user_id;     // Implement after Authentication
    const usage_extension_count = req.body.usage_extension_count
    const expiration_date_add_seconds = req.body.expiration_date_add_seconds
    const reason = req.body.reason;
    if(Utils.anyIsNotExist([card_number, extender_admin_username, usage_extension_count, expiration_date_add_seconds, reason])) return res.status(400).json({
        status: "field_not_found",
        content: null
    });


    const gc = await GiftCard.fetchOne(card_number);
    if(!gc) return res.status(404).json({
        status: "not_found:giftcard",
        content: null
    });

    gc
        .extend(extender_admin_username, reason, parseInt(expiration_date_add_seconds), parseInt(usage_extension_count))
        .then(gc => res.status(201).json({
            status: "success",
            content: {
                card_number: gc.card_number,
                maximum_usage: gc.maximum_usage,
                expiration_date: gc.expiration_date,
                qrdata: gc.qrdata
            }
        }));
});

GiftCardRoute.get("/png/:qrdata", Auth.requireApiKey, async (req, res) => {

});