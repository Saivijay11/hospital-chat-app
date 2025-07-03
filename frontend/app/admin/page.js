'use client'

import useAuth from '@/hooks/useAuth'
import ProtectedRoute from '@/components/ProtectedRoute'
import { useRouter } from 'next/navigation'

export default function AdminDashboard() {
    const { user, logout } = useAuth()
    const router = useRouter()

    return (
        <ProtectedRoute role="admin">
            <div className="p-6">
                <h1 className="text-3xl font-semibold">Welcome Admin {user?.username}</h1>
                <p className="mt-2">Use this dashboard to manage users and doctor access.</p>

                <div className="mt-6 space-x-4">
                    <button
                        onClick={() => router.push('/admin/doctors')}
                        className="bg-blue-600 text-white px-4 py-2 rounded"
                    >
                        Manage Doctors
                    </button>
                    <button
                        onClick={() => router.push('/admin/patients')}
                        className="bg-green-600 text-white px-4 py-2 rounded"
                    >
                        View Patients
                    </button>
                    <button
                        onClick={logout}
                        className="bg-red-500 text-white px-4 py-2 rounded"
                    >
                        Logout
                    </button>
                </div>
            </div>
        </ProtectedRoute>
    )
}
