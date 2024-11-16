import * as tf from '@tensorflow/tfjs';
import type { NetworkPacket, ThreatAlert } from '../types/network';

export function generateNetworkPacket(): NetworkPacket {
  const protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS'];
  const flags = ['SYN', 'ACK', 'FIN', 'RST', 'PSH'];

  return {
    id: Math.random().toString(36).substring(2, 9),
    timestamp: Date.now(),
    sourceIP: `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
    destinationIP: `10.0.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
    protocol: protocols[Math.floor(Math.random() * protocols.length)],
    size: Math.floor(Math.random() * 1500),
    flags: [flags[Math.floor(Math.random() * flags.length)]]
  };
}

export async function initializeModel() {
  const model = tf.sequential({
    layers: [
      tf.layers.dense({ inputShape: [5], units: 32, activation: 'relu' }),
      tf.layers.dense({ units: 16, activation: 'relu' }),
      tf.layers.dense({ units: 8, activation: 'relu' }),
      tf.layers.dense({ units: 1, activation: 'sigmoid' })
    ]
  });

  model.compile({
    optimizer: tf.train.adam(0.001),
    loss: 'binaryCrossentropy',
    metrics: ['accuracy']
  });

  return model;
}

export function analyzePacket(packet: NetworkPacket): ThreatAlert | null {
  const isSuspicious = 
    packet.flags.includes('RST') || 
    packet.size > 1400 ||
    (packet.protocol === 'HTTP' && packet.flags.includes('SYN'));

  if (isSuspicious) {
    return {
      id: Math.random().toString(36).substring(2, 9),
      timestamp: Date.now(),
      severity: 'high',
      description: 'Suspicious network activity detected',
      sourceIP: packet.sourceIP,
      destinationIP: packet.destinationIP,
      action: 'Block connection'
    };
  }

  return null;
}