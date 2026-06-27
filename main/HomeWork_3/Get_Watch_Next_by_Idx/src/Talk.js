const mongoose = require('mongoose');

const talk_schema = new mongoose.Schema({
    _id: String, 
    title: String,
    url: String,
    slug: String,
    description: String,
    speakers: String,
    duration: String,
    watch_next: [String], 
    tags: [String],
    comprehend_analysis: mongoose.Schema.Types.Mixed
}, { collection: 'tedx_data' });

module.exports = mongoose.model('talk', talk_schema);