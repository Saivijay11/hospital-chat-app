'use client'

import { useEffect, useState } from 'react'
import useAuth from '@/hooks/useAuth'
import ProtectedRoute from '@/components/ProtectedRoute'
import axios from '@/utils/axiosInstance'
import { useRouter } from 'next/navigation'
import DashboardHeader from '@/components/DashboardHeader'

export default function PatientDashboard() {
    const { user } = useAuth()
    const router = useRouter()
    const [patientDetails, setPatientDetails] = useState(null)

    useEffect(() => {
        if (user && user.is_patient) {
            fetchDetails()
        }
    }, [user])

    const fetchDetails = async () => {
        try {
            const res = await axios.get('/users/profile/')
            setPatientDetails(res.data)
        } catch (err) {
            console.error('Error fetching patient info:', err)
        }
    }

    return (
        <ProtectedRoute>
            <DashboardHeader />
            <div className="p-6">
                <h1 className="text-3xl font-semibold mb-4">Welcome, {user?.username}!</h1>

                {patientDetails ? (
                    <div className="bg-gray-100 p-4 rounded-md shadow-md w-full max-w-lg">
                        <p><strong>Full Name:</strong> {patientDetails.full_name || 'N/A'}</p>
                        <p><strong>Email:</strong> {patientDetails.email}</p>
                        <p><strong>Address:</strong> {patientDetails.address || 'N/A'}</p>
                        <p><strong>Blood Type:</strong> {patientDetails.blood_type || 'N/A'}</p>
                        <p><strong>Role:</strong> Patient</p>
                    </div>
                ) : (
                    <p>Loading profile...</p>
                )}

                <div className="mt-6 space-x-4">
                    <button
                        onClick={() => router.push('/chat')}
                        className="bg-blue-600 text-white px-4 py-2 rounded"
                    >
                        Go to Chat
                    </button>
                    <button
                        onClick={() => router.push('/patient/medicines')}
                        className="bg-green-600 text-white px-4 py-2 rounded"
                    >
                        View Medicines
                    </button>
                    <button
                        onClick={() => router.push('/patient/contact')}
                        className="bg-yellow-500 text-white px-4 py-2 rounded"
                    >
                        Contact Doctor
                    </button>
                </div>
            </div>
        </ProtectedRoute>
    )
}
