const mongoose = require("mongoose");


const PostSchema = mongoose.Schema({
    title: String,
    article:{
        type: String,
        required: true
    }
})

module.exports = mongoose.model("Posts", PostSchema);