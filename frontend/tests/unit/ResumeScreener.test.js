/**
 * Unit tests for ResumeScreener component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import ResumeScreener from '../../src/components/ResumeScreener';
import ApiService from '../../src/services/api';

// Mock the API service
jest.mock('../../src/services/api');

// Mock lucide-react icons
jest.mock('lucide-react', () => ({
  Upload: () => <div data-testid="upload-icon" />,
  FileText: () => <div data-testid="file-text-icon" />,
  BarChart3: () => <div data-testid="bar-chart-icon" />,
  CheckCircle: () => <div data-testid="check-circle-icon" />,
  XCircle: () => <div data-testid="x-circle-icon" />,
  Clock: () => <div data-testid="clock-icon" />,
}));

describe('ResumeScreener Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders main components correctly', () => {
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    
    render(<ResumeScreener />);
    
    expect(screen.getByText('AI Resume Matcher')).toBeInTheDocument();
    expect(screen.getByText('Upload & Analyze')).toBeInTheDocument();
    expect(screen.getByText('Match Score')).toBeInTheDocument();
    expect(screen.getByText('Detailed Analysis')).toBeInTheDocument();
  });

  test('displays backend status correctly', async () => {
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    
    render(<ResumeScreener />);
    
    await waitFor(() => {
      expect(screen.getByText(/Backend Status: Connected/)).toBeInTheDocument();
    });
  });

  test('handles backend connection failure', async () => {
    ApiService.checkHealth.mockRejectedValue(new Error('Connection failed'));
    
    render(<ResumeScreener />);
    
    await waitFor(() => {
      expect(screen.getByText(/Backend Status: Disconnected/)).toBeInTheDocument();
    });
  });

  test('allows user to input job description', async () => {
    const user = userEvent.setup();
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    
    render(<ResumeScreener />);
    
    const textarea = screen.getByLabelText(/Job Description/i);
    await user.type(textarea, 'Software Engineer position');
    
    expect(textarea).toHaveValue('Software Engineer position');
  });

  test('handles file selection', async () => {
    const user = userEvent.setup();
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    
    render(<ResumeScreener />);
    
    const file = new File(['test content'], 'test-resume.pdf', {
      type: 'application/pdf',
    });
    
    const fileInput = screen.getByLabelText(/Resume File/i);
    await user.upload(fileInput, file);
    
    expect(screen.getByText('Selected: test-resume.pdf')).toBeInTheDocument();
  });

  test('rejects non-PDF files', async () => {
    const user = userEvent.setup();
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    
    render(<ResumeScreener />);
    
    const file = new File(['test content'], 'test-resume.txt', {
      type: 'text/plain',
    });
    
    const fileInput = screen.getByLabelText(/Resume File/i);
    await user.upload(fileInput, file);
    
    expect(screen.getByText(/PLEASE SELECT A VALID PDF FILE/)).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    const user = userEvent.setup();
    const mockResponse = {
      match_score: 85,
      match_summary: 'Good match',
      detailed_analysis: {
        skill_matches: ['JavaScript'],
        skill_gaps: ['Python'],
        overall_recommendation: 'Recommended'
      }
    };
    
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    ApiService.screenResume.mockResolvedValue(mockResponse);
    
    render(<ResumeScreener />);
    
    // Fill form
    const textarea = screen.getByLabelText(/Job Description/i);
    await user.type(textarea, 'Software Engineer position');
    
    const file = new File(['test content'], 'test-resume.pdf', {
      type: 'application/pdf',
    });
    const fileInput = screen.getByLabelText(/Resume File/i);
    await user.upload(fileInput, file);
    
    // Submit form
    const submitButton = screen.getByRole('button', { name: /Analyze Resume/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(ApiService.screenResume).toHaveBeenCalledWith(file, 'Software Engineer position');
    });
  });

  test('displays results after successful submission', async () => {
    const user = userEvent.setup();
    const mockResponse = {
      match_score: 85,
      match_summary: 'Good match for the position',
      detailed_analysis: {
        skill_matches: ['JavaScript', 'React'],
        skill_gaps: ['Python'],
        overall_recommendation: 'Recommended for interview'
      }
    };
    
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    ApiService.screenResume.mockResolvedValue(mockResponse);
    
    render(<ResumeScreener />);
    
    // Fill and submit form
    const textarea = screen.getByLabelText(/Job Description/i);
    await user.type(textarea, 'Software Engineer position');
    
    const file = new File(['test content'], 'test-resume.pdf', {
      type: 'application/pdf',
    });
    const fileInput = screen.getByLabelText(/Resume File/i);
    await user.upload(fileInput, file);
    
    const submitButton = screen.getByRole('button', { name: /Analyze Resume/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('85/100')).toBeInTheDocument();
      expect(screen.getByText('Good match for the position')).toBeInTheDocument();
      expect(screen.getByText('JavaScript, React')).toBeInTheDocument();
      expect(screen.getByText('Python')).toBeInTheDocument();
      expect(screen.getByText('Recommended for interview')).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    const user = userEvent.setup();
    
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    ApiService.screenResume.mockRejectedValue(new Error('API Error'));
    
    render(<ResumeScreener />);
    
    // Fill and submit form
    const textarea = screen.getByLabelText(/Job Description/i);
    await user.type(textarea, 'Software Engineer position');
    
    const file = new File(['test content'], 'test-resume.pdf', {
      type: 'application/pdf',
    });
    const fileInput = screen.getByLabelText(/Resume File/i);
    await user.upload(fileInput, file);
    
    const submitButton = screen.getByRole('button', { name: /Analyze Resume/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/API ERROR/)).toBeInTheDocument();
    });
  });

  test('shows loading state during submission', async () => {
    const user = userEvent.setup();
    
    ApiService.checkHealth.mockResolvedValue({ status: 'healthy' });
    ApiService.screenResume.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 1000)));
    
    render(<ResumeScreener />);
    
    // Fill and submit form
    const textarea = screen.getByLabelText(/Job Description/i);
    await user.type(textarea, 'Software Engineer position');
    
    const file = new File(['test content'], 'test-resume.pdf', {
      type: 'application/pdf',
    });
    const fileInput = screen.getByLabelText(/Resume File/i);
    await user.upload(fileInput, file);
    
    const submitButton = screen.getByRole('button', { name: /Analyze Resume/i });
    await user.click(submitButton);
    
    expect(screen.getByText(/Analyzing.../)).toBeInTheDocument();
    expect(submitButton).toBeDisabled();
  });
});
