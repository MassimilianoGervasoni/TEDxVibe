const nlp = require('compromise');

module.exports = extractTopics = (description) => {
  if (!description || description.trim() === '') {
    return [];
  }

  const doc = nlp(description);

  // Estrai sostantivi chiave (i temi principali del talk)
  const nouns = doc.nouns().out('array')
    .map(n => n.toLowerCase().trim())
    .filter(n => n.length > 3)           // scarta parole troppo corte
    .filter(n => !stopWords.includes(n)) // scarta parole comuni
    .slice(0, 5);                        // massimo 5 temi

  return [...new Set(nouns)]; // rimuovi duplicati
};

const stopWords = [
  'talk', 'world', 'people', 'thing', 'time', 'year', 'life',
  'way', 'part', 'place', 'case', 'point', 'fact', 'idea',
  'work', 'hand', 'kind', 'side', 'head', 'group', 'word'
];