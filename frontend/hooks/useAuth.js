'use client'

import { useEffect, useState } from 'react'
import { jwtDecode } from 'jwt-decode'
import { useRouter } from 'next/navigation'

export default function useAuth() {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const router = useRouter()

    useEffect(() => {
        const token = localStorage.getItem('access_token')
        if (token) {
            try {
                const decoded = jwtDecode(token)
                setUser(decoded)
            } catch (err) {
                console.error('Invalid token:', err)
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                router.push('/login')
            }
        } else {
            router.push('/login')
        }
        setLoading(false)
    }, [])

    const logout = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
    }

    return { user, loading, logout }
}
