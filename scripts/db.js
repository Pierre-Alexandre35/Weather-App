const express = require("express");

const app = express();


const mongoose = require("mongoose");


require('dotenv/config');


const postsRout = require("../routes/posts");

app.use('/posts',postsRout);

app.use("/users", ()=>{
    console.log("sss");
})

app.get("/", (req,res) =>{
    res.send("ehehehh")
    console.log("we are here");
});



mongoose.connect(
    process.env.DB_CONNECTION,  
    { useNewUrlParser: true }, ()=> 
    console.log('connected to db')
);


app.listen(3000);