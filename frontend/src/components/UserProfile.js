import React from 'react'
import { useAuth } from '../contexts/AuthContext'

const UserProfile = () => {
  const { user, signOut } = useAuth()

  const handleSignOut = async () => {
    try {
      await signOut()
    } catch (error) {
      console.error('Error signing out:', error.message)
    }
  }

  if (!user) return null

  return (
    <div className="border-4 border-black bg-white p-4 mb-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {user.user_metadata?.avatar_url && (
            <img
              src={user.user_metadata.avatar_url}
              alt="Profile"
              className="w-12 h-12 border-2 border-black"
            />
          )}
          <div>
            <p className="font-mono font-bold text-black">
              {user.user_metadata?.full_name || user.email}
            </p>
            <p className="font-mono text-sm text-gray-600">
              @{user.user_metadata?.user_name || 'user'}
            </p>
          </div>
        </div>
        <button
          onClick={handleSignOut}
          className="bg-red-500 text-white font-mono px-4 py-2 border-2 border-black hover:bg-red-600 transition-colors"
        >
          SIGN OUT
        </button>
      </div>
    </div>
  )
}

export default UserProfile
