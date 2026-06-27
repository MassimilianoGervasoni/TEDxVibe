const connect_to_db = require('./db');
const talk = require('./Talk');

module.exports.get_watch_next_by_idx = async (event, context) => {
  context.callbackWaitsForEmptyEventLoop = false;

  let body = {};
  if (event.body) {
    body = typeof event.body === 'string'
      ? JSON.parse(event.body)
      : event.body;
  }

  if (!body.talk_id) {
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'text/plain' },
      body: 'Could not fetch watch_next. talk_id is null.'
    };
  }

  try {
    await connect_to_db();

    const currentTalk = await talk.findOne({ _id: body.talk_id });
    if (!currentTalk) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Talk not found.' })
      };
    }

    const currentSpeaker = currentTalk.speakers;
    if (!currentSpeaker) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Speaker not found for this talk.' })
      };
    }

    const speakerTalks = await talk.find({
      speakers: currentSpeaker,
      _id: { $ne: body.talk_id }
    }).limit(5);

    if (!speakerTalks || speakerTalks.length === 0) {
      return {
        statusCode: 404,
        body: JSON.stringify({
          error: 'No other talks found for this speaker.',
          current_speaker: currentSpeaker
        })
      };
    }

    const moreTalks = speakerTalks.map(t => ({
      id: t._id,
      emotion: t.emotion,
      duration: t.duration,
      tags: t.tags
    }));

    const responseBody = {
      current_talk_id: body.talk_id,
      current_speaker: currentSpeaker,
      more_from_speaker: moreTalks,
      explanation: {
        description: `Hai apprezzato questo talk? Ecco altri ${moreTalks.length} talk di ${currentSpeaker}.`
      }
    };

    return {
      statusCode: 200,
      body: JSON.stringify(responseBody)
    };

  } catch (err) {
    console.error('Error:', err);
    return {
      statusCode: 500,
      body: 'Could not fetch watch_next.'
    };
  }
};