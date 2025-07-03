'use client'

import { useState, useEffect, useRef } from 'react'
import useAuth from '@/hooks/useAuth'
import axios from '@/utils/axiosInstance'
import Message from './Message'

export default function ChatBox({ targetUsername }) {
    const { user } = useAuth()
    const [messages, setMessages] = useState([])
    const [newMessage, setNewMessage] = useState('')
    const [unreadCount, setUnreadCount] = useState(0)
    const socketRef = useRef(null)
    const messageEndRef = useRef(null)
    const chatFocusedRef = useRef(true)

    useEffect(() => {
        const token = localStorage.getItem('access_token')

        if (!user || !user.username || !token || !targetUsername) {
            console.log("⏳ Waiting for user to load...")
            return
        }

        console.log("✅ WebSocket connecting with:", {
            token: token,
            user: user.username,
            target: targetUsername
        })

        fetchMessages()
        initWebSocket(token)

        window.addEventListener('focus', handleFocus)
        window.addEventListener('blur', handleBlur)

        return () => {
            if (socketRef.current) socketRef.current.close()
            window.removeEventListener('focus', handleFocus)
            window.removeEventListener('blur', handleBlur)
        }
    }, [targetUsername, user])

    const handleFocus = () => {
        chatFocusedRef.current = true
        setUnreadCount(0)
    }

    const handleBlur = () => {
        chatFocusedRef.current = false
    }

    const fetchMessages = async () => {
        try {
            const res = await axios.get(`/chat/history/${targetUsername}/`)
            const formatted = res.data.map(msg => ({
                sender: msg.sender_username,
                message: msg.content,
                timestamp: msg.timestamp
            }))
            setMessages(formatted)
        } catch (err) {
            console.error("Failed to fetch messages:", err)
        }
    }


    const initWebSocket = (token) => {
        const ws = new WebSocket(`ws://localhost:8000/ws/chat/${targetUsername}/?token=${token}`)
        socketRef.current = ws

        ws.onopen = () => {
            console.log("WebSocket connected")
        }

        ws.onmessage = (e) => {
            const data = JSON.parse(e.data)
            setMessages(prev => [...prev, data])
            if (!chatFocusedRef.current) setUnreadCount(prev => prev + 1)
            scrollToBottom()
        }

        ws.onerror = (err) => {
            console.error("WebSocket error:", err)
        }

        ws.onclose = () => {
            console.log("WebSocket closed")
        }
    }

    const handleSend = (e) => {
        e.preventDefault()
        if (!newMessage.trim()) return
        if (socketRef.current?.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify({ message: newMessage }))
            setNewMessage('')
        }
    }

    const scrollToBottom = () => {
        messageEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    return (
        <div className="flex flex-col h-[80vh] w-full max-w-2xl mx-auto">
            <div className="flex items-center justify-between bg-blue-100 p-2">
                <h2 className="text-lg font-semibold">Chat with {targetUsername}</h2>
                {unreadCount > 0 && (
                    <span className="bg-red-600 text-white text-xs px-2 py-1 rounded-full">{unreadCount} unread</span>
                )}
            </div>

            <div className="flex-1 overflow-y-auto p-4 bg-gray-100 rounded-t-lg">
                {messages.map((msg, idx) => (
                    <Message key={idx} msg={msg} currentUser={user?.username} />
                ))}
                <div ref={messageEndRef} />
            </div>

            <form onSubmit={handleSend} className="flex items-center p-2 border-t bg-white rounded-b-lg">
                <input
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Type a message"
                    className="flex-1 border rounded px-4 py-2 mr-2"
                />
                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Send</button>
            </form>
        </div>
    )
}
