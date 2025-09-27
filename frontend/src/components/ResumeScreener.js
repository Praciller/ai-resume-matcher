import React, { useState, useEffect } from "react";
import ApiService from "../services/api";
import { Button } from "./ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Progress } from "./ui/progress";
import {
  Upload,
  FileText,
  BarChart3,
  CheckCircle,
  XCircle,
  Clock,
} from "lucide-react";

const ResumeScreener = () => {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState("checking");

  // Check backend health on component mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        await ApiService.checkHealth();
        setBackendStatus("connected");
      } catch (error) {
        setBackendStatus("disconnected");
        setError("BACKEND SERVER IS NOT RUNNING. PLEASE START THE BACKEND.");
      }
    };

    checkBackendHealth();
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      setResumeFile(file);
      setError(null);
    } else {
      setError("PLEASE SELECT A VALID PDF FILE");
      setResumeFile(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!resumeFile || !jobDescription.trim()) {
      setError("PLEASE PROVIDE BOTH JOB DESCRIPTION AND RESUME FILE");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await ApiService.screenResume(resumeFile, jobDescription);
      setResults(data);
    } catch (err) {
      setError(err.message.toUpperCase());
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusIcon = () => {
    switch (backendStatus) {
      case "connected":
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case "disconnected":
        return <XCircle className="h-4 w-4 text-red-600" />;
      default:
        return <Clock className="h-4 w-4 text-yellow-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="mb-8">
        <Card className="border-2">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl font-bold flex items-center justify-center gap-2">
              <BarChart3 className="h-8 w-8" />
              AI Resume Matcher
            </CardTitle>
            <CardDescription className="flex items-center justify-center gap-2 text-base">
              {getStatusIcon()}
              Backend Status:{" "}
              {backendStatus.charAt(0).toUpperCase() + backendStatus.slice(1)}
            </CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Panel - Input */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload & Analyze
            </CardTitle>
            <CardDescription>
              Upload your resume and job description to get an AI-powered match
              analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Job Description Input */}
              <div className="space-y-2">
                <Label
                  htmlFor="job-description"
                  className="text-base font-semibold"
                >
                  Job Description
                </Label>
                <Textarea
                  id="job-description"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the job description here..."
                  className="min-h-[200px] resize-none"
                  required
                />
              </div>

              {/* Resume File Input */}
              <div className="space-y-2">
                <Label
                  htmlFor="resume-file"
                  className="text-base font-semibold"
                >
                  Resume File (PDF)
                </Label>
                <Input
                  id="resume-file"
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="file:mr-4 file:py-2 file:px-4 h-14 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-primary file:text-primary-foreground hover:file:bg-primary/90"
                  required
                />
                {resumeFile && (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <FileText className="h-4 w-4" />
                    Selected: {resumeFile.name}
                  </div>
                )}
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full"
                size="lg"
              >
                {isLoading ? (
                  <>
                    <Clock className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <BarChart3 className="mr-2 h-4 w-4" />
                    Analyze Resume
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Right Panel - Results */}
        <div className="space-y-6">
          {/* Error Display */}
          {error && (
            <Card className="border-destructive">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-destructive">
                  <XCircle className="h-5 w-5" />
                  Error
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-destructive">{error}</p>
              </CardContent>
            </Card>
          )}

          {/* Match Score Display */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Match Score
              </CardTitle>
              <CardDescription>
                AI-powered compatibility analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center space-y-4">
                {results ? (
                  <>
                    <div className="text-4xl font-bold text-primary">
                      {results.match_score}/100
                    </div>
                    <Progress value={results.match_score} className="w-full" />
                  </>
                ) : (
                  <>
                    <div className="text-4xl font-bold text-muted-foreground">
                      --/100
                    </div>
                    <Progress value={0} className="w-full" />
                  </>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Analysis Details */}
          <Card className="flex-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Detailed Analysis
              </CardTitle>
              <CardDescription>
                Comprehensive breakdown of the match results
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="max-h-96 overflow-y-auto space-y-4">
                {results ? (
                  <div className="space-y-6">
                    <div>
                      <h3 className="font-semibold text-base mb-2 flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        Summary
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {results.match_summary}
                      </p>
                    </div>

                    {results.detailed_analysis && (
                      <>
                        {results.detailed_analysis.skill_matches && (
                          <div>
                            <h3 className="font-semibold text-base mb-2 flex items-center gap-2">
                              <CheckCircle className="h-4 w-4 text-green-600" />
                              Matched Skills
                            </h3>
                            <p className="text-sm text-muted-foreground">
                              {results.detailed_analysis.skill_matches.join(
                                ", "
                              ) || "None specified"}
                            </p>
                          </div>
                        )}

                        {results.detailed_analysis.skill_gaps && (
                          <div>
                            <h3 className="font-semibold text-base mb-2 flex items-center gap-2">
                              <XCircle className="h-4 w-4 text-orange-500" />
                              Skill Gaps
                            </h3>
                            <p className="text-sm text-muted-foreground">
                              {results.detailed_analysis.skill_gaps.join(
                                ", "
                              ) || "None identified"}
                            </p>
                          </div>
                        )}

                        {results.detailed_analysis.overall_recommendation && (
                          <div>
                            <h3 className="font-semibold text-base mb-2 flex items-center gap-2">
                              <BarChart3 className="h-4 w-4 text-blue-600" />
                              Recommendation
                            </h3>
                            <p className="text-sm text-muted-foreground">
                              {results.detailed_analysis.overall_recommendation}
                            </p>
                          </div>
                        )}

                        {/* Enhanced Detailed Recommendations */}
                        {results.detailed_analysis.detailed_recommendations && (
                          <div className="space-y-4 border-t pt-4">
                            <h3 className="font-semibold text-lg mb-3 flex items-center gap-2">
                              <CheckCircle className="h-5 w-5 text-green-600" />
                              Career Development Guidance
                            </h3>

                            {/* Primary Recommendation */}
                            {results.detailed_analysis.detailed_recommendations
                              .primary_recommendation && (
                              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                                <h4 className="font-semibold text-sm mb-2 text-blue-800">
                                  Primary Recommendation
                                </h4>
                                <p className="text-sm text-blue-700">
                                  {
                                    results.detailed_analysis
                                      .detailed_recommendations
                                      .primary_recommendation
                                  }
                                </p>
                              </div>
                            )}

                            {/* Improvement Areas */}
                            {results.detailed_analysis.detailed_recommendations
                              .improvement_areas &&
                              results.detailed_analysis.detailed_recommendations
                                .improvement_areas.length > 0 && (
                                <div>
                                  <h4 className="font-semibold text-sm mb-3 flex items-center gap-2">
                                    <XCircle className="h-4 w-4 text-orange-500" />
                                    Skills to Develop
                                  </h4>
                                  <div className="space-y-3">
                                    {results.detailed_analysis.detailed_recommendations.improvement_areas
                                      .sort(
                                        (a, b) =>
                                          (a.priority || 10) -
                                          (b.priority || 10)
                                      )
                                      .slice(0, 5)
                                      .map((area, index) => (
                                        <div
                                          key={index}
                                          className="bg-orange-50 p-3 rounded-lg border border-orange-200"
                                        >
                                          <div className="flex justify-between items-start mb-2">
                                            <h5 className="font-medium text-sm text-orange-800">
                                              {area.skill}
                                            </h5>
                                            <div className="flex gap-2">
                                              <span
                                                className={`px-2 py-1 text-xs rounded-full ${
                                                  area.importance === "high"
                                                    ? "bg-red-100 text-red-700"
                                                    : area.importance ===
                                                      "medium"
                                                    ? "bg-yellow-100 text-yellow-700"
                                                    : "bg-gray-100 text-gray-700"
                                                }`}
                                              >
                                                {area.importance || "medium"}{" "}
                                                priority
                                              </span>
                                              {area.estimated_timeline && (
                                                <span className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded-full">
                                                  {area.estimated_timeline}
                                                </span>
                                              )}
                                            </div>
                                          </div>
                                          {area.learning_path && (
                                            <p className="text-xs text-orange-700 mb-2">
                                              <strong>Learning Path:</strong>{" "}
                                              {area.learning_path}
                                            </p>
                                          )}
                                          {area.resources &&
                                            area.resources.length > 0 && (
                                              <div className="text-xs text-orange-700">
                                                <strong>Resources:</strong>{" "}
                                                {area.resources.join(", ")}
                                              </div>
                                            )}
                                        </div>
                                      ))}
                                  </div>
                                </div>
                              )}

                            {/* Strengths to Leverage */}
                            {results.detailed_analysis.detailed_recommendations
                              .strengths_to_leverage &&
                              results.detailed_analysis.detailed_recommendations
                                .strengths_to_leverage.length > 0 && (
                                <div>
                                  <h4 className="font-semibold text-sm mb-3 flex items-center gap-2">
                                    <CheckCircle className="h-4 w-4 text-green-600" />
                                    Your Strengths
                                  </h4>
                                  <div className="space-y-2">
                                    {results.detailed_analysis.detailed_recommendations.strengths_to_leverage.map(
                                      (strength, index) => (
                                        <div
                                          key={index}
                                          className="bg-green-50 p-3 rounded-lg border border-green-200"
                                        >
                                          <h5 className="font-medium text-sm text-green-800 mb-1">
                                            {strength.strength}
                                          </h5>
                                          <p className="text-xs text-green-700 mb-1">
                                            <strong>Relevance:</strong>{" "}
                                            {strength.relevance}
                                          </p>
                                          {strength.enhancement_tips && (
                                            <p className="text-xs text-green-700">
                                              <strong>Enhancement Tips:</strong>{" "}
                                              {strength.enhancement_tips}
                                            </p>
                                          )}
                                        </div>
                                      )
                                    )}
                                  </div>
                                </div>
                              )}

                            {/* Career Guidance */}
                            {results.detailed_analysis.detailed_recommendations
                              .career_guidance && (
                              <div>
                                <h4 className="font-semibold text-sm mb-3 flex items-center gap-2">
                                  <BarChart3 className="h-4 w-4 text-purple-600" />
                                  Career Guidance
                                </h4>
                                <div className="space-y-3">
                                  {results.detailed_analysis
                                    .detailed_recommendations.career_guidance
                                    .immediate_actions &&
                                    results.detailed_analysis
                                      .detailed_recommendations.career_guidance
                                      .immediate_actions.length > 0 && (
                                      <div className="bg-purple-50 p-3 rounded-lg border border-purple-200">
                                        <h5 className="font-medium text-sm text-purple-800 mb-2">
                                          Immediate Actions
                                        </h5>
                                        <ul className="text-xs text-purple-700 space-y-1">
                                          {results.detailed_analysis.detailed_recommendations.career_guidance.immediate_actions.map(
                                            (action, index) => (
                                              <li
                                                key={index}
                                                className="flex items-start gap-2"
                                              >
                                                <span className="text-purple-500 mt-1">
                                                  •
                                                </span>
                                                {action}
                                              </li>
                                            )
                                          )}
                                        </ul>
                                      </div>
                                    )}

                                  {results.detailed_analysis
                                    .detailed_recommendations.career_guidance
                                    .short_term_goals &&
                                    results.detailed_analysis
                                      .detailed_recommendations.career_guidance
                                      .short_term_goals.length > 0 && (
                                      <div className="bg-indigo-50 p-3 rounded-lg border border-indigo-200">
                                        <h5 className="font-medium text-sm text-indigo-800 mb-2">
                                          Short-term Goals (3-6 months)
                                        </h5>
                                        <ul className="text-xs text-indigo-700 space-y-1">
                                          {results.detailed_analysis.detailed_recommendations.career_guidance.short_term_goals.map(
                                            (goal, index) => (
                                              <li
                                                key={index}
                                                className="flex items-start gap-2"
                                              >
                                                <span className="text-indigo-500 mt-1">
                                                  •
                                                </span>
                                                {goal}
                                              </li>
                                            )
                                          )}
                                        </ul>
                                      </div>
                                    )}

                                  {results.detailed_analysis
                                    .detailed_recommendations.career_guidance
                                    .long_term_development &&
                                    results.detailed_analysis
                                      .detailed_recommendations.career_guidance
                                      .long_term_development.length > 0 && (
                                      <div className="bg-teal-50 p-3 rounded-lg border border-teal-200">
                                        <h5 className="font-medium text-sm text-teal-800 mb-2">
                                          Long-term Development
                                        </h5>
                                        <ul className="text-xs text-teal-700 space-y-1">
                                          {results.detailed_analysis.detailed_recommendations.career_guidance.long_term_development.map(
                                            (dev, index) => (
                                              <li
                                                key={index}
                                                className="flex items-start gap-2"
                                              >
                                                <span className="text-teal-500 mt-1">
                                                  •
                                                </span>
                                                {dev}
                                              </li>
                                            )
                                          )}
                                        </ul>
                                      </div>
                                    )}
                                </div>
                              </div>
                            )}

                            {/* Interview Preparation */}
                            {results.detailed_analysis.detailed_recommendations
                              .interview_preparation && (
                              <div>
                                <h4 className="font-semibold text-sm mb-3 flex items-center gap-2">
                                  <FileText className="h-4 w-4 text-pink-600" />
                                  Interview Preparation
                                </h4>
                                <div className="space-y-3">
                                  {results.detailed_analysis
                                    .detailed_recommendations
                                    .interview_preparation.talking_points &&
                                    results.detailed_analysis
                                      .detailed_recommendations
                                      .interview_preparation.talking_points
                                      .length > 0 && (
                                      <div className="bg-pink-50 p-3 rounded-lg border border-pink-200">
                                        <h5 className="font-medium text-sm text-pink-800 mb-2">
                                          Key Talking Points
                                        </h5>
                                        <ul className="text-xs text-pink-700 space-y-1">
                                          {results.detailed_analysis.detailed_recommendations.interview_preparation.talking_points.map(
                                            (point, index) => (
                                              <li
                                                key={index}
                                                className="flex items-start gap-2"
                                              >
                                                <span className="text-pink-500 mt-1">
                                                  •
                                                </span>
                                                {point}
                                              </li>
                                            )
                                          )}
                                        </ul>
                                      </div>
                                    )}

                                  {results.detailed_analysis
                                    .detailed_recommendations
                                    .interview_preparation
                                    .red_flags_to_address &&
                                    results.detailed_analysis
                                      .detailed_recommendations
                                      .interview_preparation
                                      .red_flags_to_address.length > 0 && (
                                      <div className="bg-red-50 p-3 rounded-lg border border-red-200">
                                        <h5 className="font-medium text-sm text-red-800 mb-2">
                                          Potential Concerns to Address
                                        </h5>
                                        <ul className="text-xs text-red-700 space-y-1">
                                          {results.detailed_analysis.detailed_recommendations.interview_preparation.red_flags_to_address.map(
                                            (flag, index) => (
                                              <li
                                                key={index}
                                                className="flex items-start gap-2"
                                              >
                                                <span className="text-red-500 mt-1">
                                                  •
                                                </span>
                                                {flag}
                                              </li>
                                            )
                                          )}
                                        </ul>
                                      </div>
                                    )}
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">
                      Upload a resume to see detailed analysis
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ResumeScreener;
