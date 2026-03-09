const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

mongoose.connect('mongodb://localhost:27017/parking_system');

const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});

userSchema.pre('save', async function(next){
    if(!this.isModified('password')) return next();
    this.password = await
     bcrypt.hash(this.password, 10);
    next();
});

const User = mongoose.model('User', userSchema);

app.post('/register', async (req,res)=>{
    try{
        const {username,password} = req.body;

        const existingUser = await User.findOne({username});
        if(existingUser) return res.status(400).send("User already exists");

        const user = new User({username,password});
        await user.save();

        res.send("User registered successfully");
    }
    catch(err){
        res.status(500).send(err.message);
    }
});

app.post('/login', async (req,res)=>{
    try{
        const {username,password} = req.body;
        const user = await User.findOne({username});
        if(!user) return res.status(400).send("Invalid username");

        const valid = await bcrypt.compare(password,user.password);
        if(!valid) return res.status(400).send("Invalid password");

        const token = jwt.sign({id:user._id},
            'secret_key',{expiresIn:"1h"});

        res.header("Authorization", `Bearer ${token}`)
           .send({token});
    }
    const stripe = require('stripe');
    const stripe = new
    stripe('your_stripe_secret_key');
});

app.listen(3000,()=>{
    console.log("Server running on port 3000");
});