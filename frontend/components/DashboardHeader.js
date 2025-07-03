'use client'

import { useEffect, useState, useImperativeHandle, forwardRef } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import useAuth from '@/hooks/useAuth'
import axios from '@/utils/axiosInstance'

const DashboardHeader = forwardRef((props, ref) => {
    const { user, logout } = useAuth()
    const router = useRouter()
    const pathname = usePathname()
    const [unreadCount, setUnreadCount] = useState(0)

    const role = user?.is_admin
        ? 'admin'
        : user?.is_doctor
            ? 'doctor'
            : 'patient'

    const fetchUnread = async () => {
        try {
            const res = await axios.get('/chat/unread-counts/')
            const total = Object.values(res.data).reduce((sum, count) => sum + count, 0)
            setUnreadCount(total)
        } catch (err) {
            console.error("Failed to fetch unread count")
        }
    }

    useEffect(() => {
        if (user) fetchUnread()
    }, [user, pathname])

    useImperativeHandle(ref, () => ({
        refreshUnreadCount: fetchUnread,
    }))

    return (
        <header className="bg-gray-800 text-white px-4 py-3 flex justify-between items-center shadow">
            <h1 className="text-lg font-semibold">Hospital Chat Dashboard</h1>
            <nav className="space-x-4 flex items-center">
                <button onClick={() => router.push(`/${role}`)}>Home</button>

                <button onClick={() => router.push('/chat')} className="relative">
                    Chat
                    {unreadCount > 0 && (
                        <span className="absolute -top-2 -right-3 bg-red-500 text-white text-xs rounded-full px-2 py-0.5">
                            {unreadCount}
                        </span>
                    )}
                </button>

                {role === 'patient' && (
                    <>
                        <button onClick={() => router.push('/patient/contact')}>Contact Us</button>
                        <button onClick={() => router.push('/patient/medicines')}>Medicines</button>
                    </>
                )}

                {role === 'admin' && (
                    <>
                        <button onClick={() => router.push('/admin/contact')}>Contact Us</button>
                        <button onClick={() => router.push('/admin/medicines')}>Medicines</button>
                    </>
                )}

                {role === 'doctor' && (
                    <>
                        <button onClick={() => router.push('/doctor/patients')}>Patients</button>
                        <button onClick={() => router.push('/doctor/appointments')}>Appointments</button>
                    </>
                )}

                <button
                    onClick={logout}
                    className="bg-red-600 px-2 py-1 rounded ml-2"
                >
                    Logout
                </button>
            </nav>
        </header>
    )
})

export default DashboardHeader
