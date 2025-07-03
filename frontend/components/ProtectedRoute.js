'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import useAuth from '../hooks/useAuth'

export default function ProtectedRoute({ children, role }) {
    const { user, loading } = useAuth()
    const router = useRouter()

    useEffect(() => {
        if (!loading) {
            if (!user) {
                router.push('/unauthorized')
            } else if (role) {
                if (
                    (role === 'doctor' && !user.is_doctor) ||
                    (role === 'patient' && !user.is_patient) ||
                    (role === 'admin' && !user.is_admin)
                ) {
                    router.push('/unauthorized')
                }
            }
        }
    }, [loading, user, role])

    if (loading || !user) return <p>Loading...</p>

    return children
}
