const express = require("express");

const router = express.Router();

const posts = require("../models/posts");

router.get('/', (req, res)=>{
    res.send("my name is");
});

router.get('/article-1', (req, res)=>{
    res.send("Laurent");
});

router.post("/", (req, res) =>{
        console.log(req.body);
});


module.exports = router;