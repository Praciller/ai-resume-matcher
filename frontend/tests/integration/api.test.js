/**
 * Integration tests for API service
 * These tests verify the API service functionality
 */

import ApiService from '../../src/services/api';

// Mock fetch for testing
global.fetch = jest.fn();

describe('ApiService Integration Tests', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('checkHealth', () => {
    test('should return health status when backend is available', async () => {
      const mockResponse = {
        status: 'healthy',
        gemini_ai: 'connected'
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await ApiService.checkHealth();
      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/health')
      );
    });

    test('should throw error when backend is unavailable', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      await expect(ApiService.checkHealth()).rejects.toThrow('BACKEND UNAVAILABLE');
    });
  });

  describe('screenResume', () => {
    test('should successfully screen resume with valid inputs', async () => {
      const mockFile = new File(['test content'], 'test-resume.pdf', {
        type: 'application/pdf',
      });
      const jobDescription = 'Software Engineer position';
      const mockResponse = {
        match_score: 85,
        match_summary: 'Good match for the position',
        detailed_analysis: {
          skill_matches: ['JavaScript', 'React'],
          skill_gaps: ['Python'],
          overall_recommendation: 'Recommended for interview'
        }
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await ApiService.screenResume(mockFile, jobDescription);
      
      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/screen-resume'),
        expect.objectContaining({
          method: 'POST',
          body: expect.any(FormData),
        })
      );
    });

    test('should handle API errors gracefully', async () => {
      const mockFile = new File(['test content'], 'test-resume.pdf', {
        type: 'application/pdf',
      });
      const jobDescription = 'Software Engineer position';

      fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({ detail: 'Invalid file format' }),
      });

      await expect(
        ApiService.screenResume(mockFile, jobDescription)
      ).rejects.toThrow('Invalid file format');
    });

    test('should handle network errors', async () => {
      const mockFile = new File(['test content'], 'test-resume.pdf', {
        type: 'application/pdf',
      });
      const jobDescription = 'Software Engineer position';

      fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));

      await expect(
        ApiService.screenResume(mockFile, jobDescription)
      ).rejects.toThrow('UNABLE TO CONNECT TO SERVER');
    });
  });

  describe('extractResumeData', () => {
    test('should extract resume data successfully', async () => {
      const mockFile = new File(['test content'], 'test-resume.pdf', {
        type: 'application/pdf',
      });
      const mockResponse = {
        extracted_data: {
          name: 'John Doe',
          email: 'john@example.com',
          skills: ['JavaScript', 'React']
        },
        raw_text_preview: 'John Doe Software Engineer...'
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await ApiService.extractResumeData(mockFile);
      
      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/extract-resume'),
        expect.objectContaining({
          method: 'POST',
          body: expect.any(FormData),
        })
      );
    });

    test('should handle extraction errors', async () => {
      const mockFile = new File(['test content'], 'test-resume.pdf', {
        type: 'application/pdf',
      });

      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({ detail: 'Failed to process PDF' }),
      });

      await expect(
        ApiService.extractResumeData(mockFile)
      ).rejects.toThrow('Failed to process PDF');
    });
  });

  describe('API URL Configuration', () => {
    test('should use environment variable for API URL', () => {
      // This test verifies that the API service uses the correct base URL
      const originalEnv = process.env.REACT_APP_API_URL;
      process.env.REACT_APP_API_URL = 'https://test-api.example.com';

      // Re-import to get updated environment variable
      jest.resetModules();
      const ApiServiceWithNewEnv = require('../../src/services/api').default;

      // The actual URL construction happens inside the methods,
      // so we need to test it indirectly through a mock call
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'healthy' }),
      });

      ApiServiceWithNewEnv.checkHealth();

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('https://test-api.example.com')
      );

      // Restore original environment
      process.env.REACT_APP_API_URL = originalEnv;
    });
  });
});
