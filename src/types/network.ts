export interface NetworkPacket {
  id: string;
  timestamp: number;
  sourceIP: string;
  destinationIP: string;
  protocol: string;
  size: number;
  flags: string[];
}

export interface ThreatAlert {
  id: string;
  timestamp: number;
  severity: 'low' | 'medium' | 'high';
  description: string;
  sourceIP: string;
  destinationIP: string;
  action: string;
}

export interface NetworkStats {
  packetsAnalyzed: number;
  threatsDetected: number;
  lastUpdated: number;
}