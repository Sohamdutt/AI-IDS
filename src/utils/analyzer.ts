const INSTRUCTION_PATTERNS = [
  /\b(must|should|shall|required|mandatory|critical)\b/i,
  /\b(always|never|do not|cannot|can't)\b/i,
  /\b(important|note|warning|caution)\b/i,
  /\b(follow|ensure|make sure|verify)\b/i
];

export function analyzeText(text: string): string[] {
  const instructions: string[] = [];
  const sentences = text.split(/[.!?]+/).filter(Boolean);

  sentences.forEach(sentence => {
    const trimmedSentence = sentence.trim();
    if (INSTRUCTION_PATTERNS.some(pattern => pattern.test(trimmedSentence))) {
      instructions.push(trimmedSentence);
    }
  });

  return instructions;
}