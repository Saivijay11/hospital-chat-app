'use client'

import { useState, useEffect, useRef } from 'react'
import useAuth from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'
import DashboardHeader from '@/components/DashboardHeader'
import axios from '@/utils/axiosInstance'
import ChatBox from '@/components/ChatBox'

export default function ChatPage() {
    const { user } = useAuth()
    const router = useRouter()
    const [selectedUser, setSelectedUser] = useState(null)
    const [availableUsers, setAvailableUsers] = useState([])
    const [unreadCounts, setUnreadCounts] = useState({})
    const headerRef = useRef()

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const token = localStorage.getItem('access_token')
                if (!token || !user) {
                    console.warn('No token or user found')
                    return
                }

                const [usersRes, unreadRes] = await Promise.all([
                    axios.get('/users/all-users/'),
                    axios.get('/chat/unread-counts/')
                ])

                setAvailableUsers(usersRes.data)
                setUnreadCounts(unreadRes.data)
            } catch (err) {
                if (err.response?.status === 401) {
                    localStorage.removeItem('access_token')
                    router.push('/login')
                } else {
                    console.error('Error fetching users/unread counts:', err)
                }
            }
        }

        if (user) fetchUsers()
    }, [user])

    const handleUserClick = async (u) => {
        setSelectedUser(u)
        if (unreadCounts[u.username] > 0) {
            setUnreadCounts(prev => ({
                ...prev,
                [u.username]: 0
            }))
        }
        try {
            await axios.post(`/chat/mark-read/${u.username}/`)
            if (headerRef.current?.refreshUnreadCount) {
                headerRef.current.refreshUnreadCount()
            }
        } catch (err) {
            console.error('Failed to mark messages as read:', err)
        }
    }

    if (!user) return <p>Loading...</p>

    return (
        <>
            <DashboardHeader ref={headerRef} />
            <div className="p-6">
                <h1 className="text-2xl font-bold mb-4">Chat</h1>

                <div className="flex">
                    <div className="w-1/4 border-r pr-4">
                        <h2 className="text-lg font-semibold mb-2">Available Users</h2>
                        {availableUsers.map((u) => (
                            <div
                                key={u.username}
                                className={`cursor-pointer p-2 rounded hover:bg-gray-200 ${selectedUser?.username === u.username ? 'bg-gray-300' : ''}`}
                                onClick={() => handleUserClick(u)}
                            >
                                {u.full_name} ({u.username})
                                {unreadCounts[u.username] > 0 && (
                                    <span className="ml-2 bg-red-500 text-white px-2 py-0.5 text-xs rounded-full">
                                        {unreadCounts[u.username]}
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>

                    <div className="w-3/4 pl-4">
                        {selectedUser ? (
                            <ChatBox targetUsername={selectedUser.username} />
                        ) : (
                            <p className="text-gray-600">Select a user to start chatting.</p>
                        )}
                    </div>
                </div>
            </div>
        </>
    )
}
