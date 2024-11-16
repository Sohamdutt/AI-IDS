import React, { useState } from 'react';
import { analyzeText } from '../utils/analyzer';
import ResultCard from './ResultCard';

export default function TextAnalyzer() {
  const [text, setText] = useState('');
  const [results, setResults] = useState<string[]>([]);

  const handleAnalyze = () => {
    const detectedInstructions = analyzeText(text);
    setResults(detectedInstructions);
  };

  return (
    <div className="space-y-4">
      <textarea
        className="w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500"
        placeholder="Enter text to analyze..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        onClick={handleAnalyze}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Analyze Text
      </button>
      {results.length > 0 && (
        <div className="space-y-2">
          {results.map((result, index) => (
            <ResultCard key={index} instruction={result} />
          ))}
        </div>
      )}
    </div>
  );
}