import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { format } from 'date-fns';
import { generateNetworkPacket, analyzePacket } from '../utils/networkAnalyzer';
import type { NetworkPacket, ThreatAlert, NetworkStats } from '../types/network';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function NetworkDashboard() {
  const [packets, setPackets] = useState<NetworkPacket[]>([]);
  const [alerts, setAlerts] = useState<ThreatAlert[]>([]);
  const [stats, setStats] = useState<NetworkStats>({
    packetsAnalyzed: 0,
    threatsDetected: 0,
    lastUpdated: Date.now()
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const newPacket = generateNetworkPacket();
      const threat = analyzePacket(newPacket);

      setPackets(prev => [...prev.slice(-50), newPacket]);
      if (threat) {
        setAlerts(prev => [...prev.slice(-10), threat]);
      }
      setStats(prev => ({
        packetsAnalyzed: prev.packetsAnalyzed + 1,
        threatsDetected: threat ? prev.threatsDetected + 1 : prev.threatsDetected,
        lastUpdated: Date.now()
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: packets.map(p => format(p.timestamp, 'HH:mm:ss')),
    datasets: [
      {
        label: 'Packet Size',
        data: packets.map(p => p.size),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Network Traffic Analysis'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Packets Analyzed</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.packetsAnalyzed}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Threats Detected</h3>
          <p className="text-3xl font-bold text-red-600">{stats.threatsDetected}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Last Updated</h3>
          <p className="text-lg text-gray-600">
            {format(stats.lastUpdated, 'HH:mm:ss')}
          </p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow">
        <div style={{ height: '400px' }}>
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Recent Alerts</h3>
        <div className="space-y-2">
          {alerts.map(alert => (
            <div
              key={alert.id}
              className="p-3 rounded-lg bg-red-50 border border-red-200"
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-semibold text-red-700">{alert.description}</p>
                  <p className="text-sm text-gray-600">
                    Source: {alert.sourceIP} → Destination: {alert.destinationIP}
                  </p>
                </div>
                <span className="px-2 py-1 text-xs font-semibold rounded bg-red-200 text-red-800">
                  {alert.severity}
                </span>
              </div>
            </div>
          ))}
          {alerts.length === 0 && (
            <p className="text-gray-500 text-center py-4">No alerts detected</p>
          )}
        </div>
      </div>
    </div>
  );
}