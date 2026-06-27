const connect_to_db = require('./db');
const talk = require('./Talk');

module.exports.get_talks_by_emotion = async (event, context) => {
  context.callbackWaitsForEmptyEventLoop = false;

  let body = {};
  if (event.body) {
    body = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
  }

  if (!body.emotion) {
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'text/plain' },
      body: 'Could not fetch talks. emotion is null.'
    };
  }

  const limit = parseInt(body.limit) || 10;

  try {
    await connect_to_db();

    const results = await talk
      .find({ emotion: body.emotion })
      .limit(limit);

    if (!results || results.length === 0) {
      return {
        statusCode: 404,
        body: JSON.stringify({
          error: 'No talks found for this emotion',
          emotion: body.emotion
        })
      };
    }

    // Per ogni talk, risolvo il primo suggerimento watch_next
    const talksWithSuggestion = await Promise.all(results.map(async t => {
      let suggestion = null;
      if (t.watch_next && t.watch_next.length > 0) {
        const suggested = await talk.findOne({ _id: t.watch_next[0] });
        if (suggested) {
          suggestion = {
            id: suggested._id,
            description: suggested.description,
            duration: suggested.duration,
            emotion: suggested.emotion
          };
        }
      }
      return {
        id: t._id,
        emotion: t.emotion,
        description: t.description,
        duration: t.duration,
        tags: t.tags
      };
    }));

    const responseBody = {
      emotion: body.emotion,
      count: talksWithSuggestion.length,
      talks: talksWithSuggestion
    };

    return {
      statusCode: 200,
      body: JSON.stringify(responseBody)
    };

  } catch (err) {
    console.error('Error fetching talks by emotion:', err);
    return {
      statusCode: 500,
      body: 'Could not fetch talks by emotion.'
    };
  }
};