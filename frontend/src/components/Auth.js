import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'

const Auth = () => {
  const { signInWithGitHub } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGitHubSignIn = async () => {
    try {
      setLoading(true)
      setError(null)
      await signInWithGitHub()
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white flex items-center justify-center">
      <div className="max-w-md w-full space-y-8 p-8">
        <div className="text-center">
          <h1 className="text-4xl font-mono font-bold text-black border-4 border-black p-4 bg-white">
            AI RESUME MATCHER
          </h1>
          <p className="mt-4 text-lg font-mono text-black">
            SIGN IN TO ACCESS THE APPLICATION
          </p>
        </div>

        <div className="space-y-4">
          {error && (
            <div className="border-4 border-red-500 bg-red-50 p-4">
              <p className="font-mono text-red-700 text-sm">
                ERROR: {error}
              </p>
            </div>
          )}

          <button
            onClick={handleGitHubSignIn}
            disabled={loading}
            className="w-full bg-black text-white font-mono text-lg py-4 px-6 border-4 border-black hover:bg-white hover:text-black transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'SIGNING IN...' : 'SIGN IN WITH GITHUB'}
          </button>

          <div className="text-center">
            <p className="font-mono text-sm text-gray-600">
              SECURE AUTHENTICATION VIA GITHUB OAUTH
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Auth
