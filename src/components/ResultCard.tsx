import React from 'react';
import clsx from 'clsx';

interface ResultCardProps {
  instruction: string;
}

export default function ResultCard({ instruction }: ResultCardProps) {
  const severity = instruction.toLowerCase().includes('critical') ? 'high' : 'medium';

  return (
    <div className={clsx(
      'p-4 rounded-lg border',
      severity === 'high' ? 'bg-red-50 border-red-200' : 'bg-yellow-50 border-yellow-200'
    )}>
      <div className="flex items-start">
        <div className={clsx(
          'w-2 h-2 rounded-full mt-2 mr-2',
          severity === 'high' ? 'bg-red-500' : 'bg-yellow-500'
        )} />
        <p className="text-gray-700">{instruction}</p>
      </div>
    </div>
  );
}