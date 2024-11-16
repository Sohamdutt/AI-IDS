import type { VulnerabilityResult, EmailConfig } from '../types/vulnerability';

export async function sendEmailAlert(vulnerability: VulnerabilityResult, config: EmailConfig) {
  // In a real implementation, this would use nodemailer or an email service API
  // For demo purposes, we'll just log the email content
  console.log('Email Alert:', {
    to: config.to,
    from: config.from,
    subject: config.subject,
    text: `
      Vulnerability Alert
      
      Type: ${vulnerability.type}
      Severity: ${vulnerability.severity}
      Description: ${vulnerability.description}
      Payload: ${vulnerability.payload}
      Timestamp: ${new Date(vulnerability.timestamp).toLocaleString()}
    `
  });
}