"use client"
import { useEffect, useState, useRef } from "react"
import axios from "axios"
import { toast } from "sonner"
import { useRouter } from "next/navigation"
import useUserStore from "@/store/userStore"
import Image from "next/image"
import { Button } from "./ui/button"
import { LogOut, Send, User } from "lucide-react"
import { Card, CardContent } from "./ui/card"
import { Input } from "./ui/input"

axios.defaults.withCredentials = true

export default function HomePage() {
const router = useRouter()
const isLoggingOutRef = useRef(false)

  const user = useUserStore((state) => state.user)
  const hasHydrated = useUserStore((state) => state.hasHydrated)
  const loggingOut = useUserStore((state) => state.loggingOut)
  const setUser = useUserStore((state) => state.setUser)
  const clearUser = useUserStore((state) => state.clearUser)
  const setLoggingOut = useUserStore((state) => state.setLoggingOut)

  const [messages, setMessages] = useState<
    Array<{ role: "user" | "assistant"; content: string }>
  >([])
  const [prompt, setPrompt] = useState("")

  // ✅ Session check effect
  useEffect(() => {
    if (!hasHydrated) return // wait for hydration

    const checkSession = async () => {
      try {
        const response = await axios.get("http://localhost:8000/auth/profile", {
          withCredentials: true,
        })
        if (response.data.profile == "success") {
          console.log(response.data.user)
          setUser(response.data.user)
        }
      } catch (err) {
        // Only show toast if we're not intentionally logging out
        if (!isLoggingOutRef.current) {
          toast("Not authenticated...")
          clearUser()
          router.push("/")
        }
      }
    }
    
    if (!user) {
      checkSession()
     console.log("calling api ")
    }
  }, [user, hasHydrated, setUser, clearUser, router])

  // ✅ Logout function
  const Logout = async () => {
    isLoggingOutRef.current = true 
    setLoggingOut(true)
    try {
      const response = await axios.get("http://localhost:8000/auth/logout-google", {
        withCredentials: true,
      })
      if (response.data.status === "success") {
        clearUser()
        toast("Logout successfully")
        router.push("/")
      }
    } catch (err) {
      console.log(err)
      toast("Logout failed")
    } finally {
      setLoggingOut(false)
      // Reset ref after a small delay to ensure all effects have settled
      setTimeout(() => {
        isLoggingOutRef.current = false
      }, 100)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return
    const newMessages = [...messages, { role: "user", content: prompt }]

    setTimeout(() => {
      setMessages([{ role: "assistant", content: "I'm here to help! How can I assist you today?" }])
    }, 1000)
    setPrompt("")
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border bg-card">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                <span className="text-accent-foreground font-bold text-lg">AI</span>
              </div>
              <span className="text-xl font-semibold text-foreground">Assistant</span>
            </div>

            <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-muted-foreground">
              {user?.profile_picture && (
                <Image
                  src={user.profile_picture}
                  alt="User Profile"
                  width={32}
                  height={32}
                  className="rounded-full"
                />
              )}
              <span className="text-sm">Welcome {user?.name}</span>
            </div>
              <Button variant="ghost" size="sm" onClick={Logout} className="text-muted-foreground hover:text-foreground">
                <LogOut className="w-4 h-4 mr-2" />
                Sign out
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-4 text-balance">AI here to Help You</h1>
          <p className="text-lg text-muted-foreground text-pretty">
            Ask me anything and I'll do my best to assist you with your questions and tasks.
          </p>
        </div>

        {/* Chat Messages */}
        <div className="space-y-4 mb-8 min-h-[300px]">
          {messages.length === 0 ? (
            <Card className="bg-card border-border">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl text-accent">🤖</span>
                </div>
                <p className="text-muted-foreground">Start a conversation by typing your question or request below.</p>
              </CardContent>
            </Card>
          ) : (
            messages.map((message, index) => (
              <Card key={index} className={`bg-card border-border ${message.role === "user" ? "ml-12" : "mr-12"}`}>
                <CardContent className="p-4">
                  <div className="flex items-start space-x-3">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        message.role === "user"
                          ? "bg-secondary text-secondary-foreground"
                          : "bg-accent text-accent-foreground"
                      }`}
                    >
                      {message.role === "user" ? (
                        <User className="w-4 h-4" />
                      ) : (
                        <span className="text-sm font-bold">AI</span>
                      )}
                    </div>
                    <div className="flex-1">
                      <p className="text-card-foreground leading-relaxed">{message.content}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Prompt Input */}
        <Card className="bg-card border-border">
          <CardContent className="p-4">
            <form onSubmit={handleSubmit} className="flex space-x-3">
              <Input
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Type your message here..."
                className="flex-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
              />
              <Button
                type="submit"
                className="bg-accent text-accent-foreground hover:bg-accent/90"
                disabled={!prompt.trim()}
              >
                <Send className="w-4 h-4" />
              </Button>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}