"use client"

import { create } from "zustand"
import { persist } from "zustand/middleware"

interface User {
  google_id: string
  email: string
  email_verified: boolean
  name: string
  profile_picture: string
}

interface UserState {
  user: User | null
  setUser: (user: User) => void
  clearUser: () => void
  hasHydrated: boolean
  setHydrated: () => void
  loggingOut: boolean
  setLoggingOut: (v: boolean) => void
}

const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      user: null,
      hasHydrated: false,
      loggingOut: false,
      setUser: (user) => set({ user }),
      clearUser: () => set({ user: null }),
      setHydrated: () => set({ hasHydrated: true }),
      setLoggingOut: (v) => set({ loggingOut: v }),
    }),
    {
      name: "user-storage",
      onRehydrateStorage: () => (state) => {
        state?.setHydrated()
      },
    }
  )
)

export default useUserStore
