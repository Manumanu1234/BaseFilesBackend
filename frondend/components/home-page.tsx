"use client"

import type React from "react"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Send, User, LogOut } from "lucide-react"
import { useRouter } from "next/navigation"
import axios from "axios"
import { toast } from "sonner"
axios.defaults.withCredentials = true  


export function HomePage() {
  const [prompt, setPrompt] = useState("")
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([])
  const [Image,setImage]=useState("")
  const router=useRouter()
  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await axios.get("http://localhost:8000/auth/profile", {
          withCredentials: true, 
        })
        if(response.data.profile=="sucess"){
          console.log(response.data.user)
          setImage(response.data.user.profile_picture)
          router.push("/home")
        }
      } catch (error) {
        toast("not authenticated...")
        router.push("/") // redirect to login page
      }
    }

    checkSession()
  }, [router])
  const Logout=()=>{
       axios.get("http://localhost:8000/auth/logout-google",{ withCredentials: true })
       .then(function (response) {
            console.log(response);
            if(response.data.status="sucess"){
                toast("logout sucessfully")
                router.push("/")
            }
        })
        .catch(function (error) {
            console.log(error);
        });

  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    // Add user message
    const newMessages = [...messages, { role: "user" as const, content: prompt }]
    setMessages(newMessages)

    // Simulate AI response
    setTimeout(() => {
      setMessages([
        ...newMessages,
        {
          role: "assistant" as const,
          content: "I'm here to help! How can I assist you today?",
        },
      ])
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
                {Image && (
                  <img src={Image} alt="User Profile" className="w-8 h-8 rounded-full" />
                )}
                <span className="text-sm">Welcome back!</span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={Logout}
                className="text-muted-foreground hover:text-foreground"
              >
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
