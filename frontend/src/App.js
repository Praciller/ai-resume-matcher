import React from "react";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import ResumeScreener from "./components/ResumeScreener";
import Auth from "./components/Auth";

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="border-4 border-black p-8 bg-white">
            <h1 className="text-2xl font-mono font-bold text-black mb-4">
              AI RESUME MATCHER
            </h1>
            <p className="font-mono text-black">LOADING...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Auth />;
  }

  return (
    <div className="App">
      <ResumeScreener />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
