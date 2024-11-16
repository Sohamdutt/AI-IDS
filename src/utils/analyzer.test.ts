import { expect, test } from 'vitest';
import { analyzeText } from './analyzer';

test('detects must instructions', () => {
  const text = 'You must follow these guidelines.';
  expect(analyzeText(text)).toContain('You must follow these guidelines');
});

test('detects critical instructions', () => {
  const text = 'This is a CRITICAL requirement.';
  expect(analyzeText(text)).toContain('This is a CRITICAL requirement');
});

test('detects multiple instructions', () => {
  const text = 'You must do this. Never do that. Always follow protocol.';
  const results = analyzeText(text);
  expect(results).toHaveLength(3);
});

test('ignores non-instruction text', () => {
  const text = 'This is a normal sentence without instructions.';
  expect(analyzeText(text)).toHaveLength(0);
});