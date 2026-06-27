const mongoose = require('mongoose');

const talk_schema = new mongoose.Schema({
    _id: String,
    emotion: String,
    tags: [String],
    description: String,
    duration: String,
    publishedAt: String,
    watch_next: [String]
}, { collection: 'tedx_watch_next' });

module.exports = mongoose.model('talk_emotion', talk_schema);