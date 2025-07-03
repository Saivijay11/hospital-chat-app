'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import useAuth from '@/hooks/useAuth'
import DashboardHeader from '@/components/DashboardHeader'
import axios from '@/utils/axiosInstance'

export default function DoctorDashboard() {
    const { user, loading } = useAuth()
    const router = useRouter()
    const [doctorInfo, setDoctorInfo] = useState(null)

    useEffect(() => {
        if (!loading) {
            if (!user || !user.is_doctor) {
                router.push('/unauthorized')
            } else {
                fetchDoctorProfile()
            }
        }
    }, [user, loading])

    const fetchDoctorProfile = async () => {
        try {
            const res = await axios.get('/users/profile/')
            setDoctorInfo(res.data)
        } catch (err) {
            console.error('Error fetching doctor info:', err)
        }
    }

    if (loading || !user) return <p>Loading...</p>

    return (
        <>
            <DashboardHeader role="doctor" />
            <div className="p-6">
                <h2 className="text-3xl font-semibold mb-4">Welcome Dr. {user.username}!</h2>

                {doctorInfo ? (
                    <div className="bg-gray-100 p-4 rounded-md shadow-md w-full max-w-lg">
                        <p><strong>Full Name:</strong> {doctorInfo.full_name || 'N/A'}</p>
                        <p><strong>Email:</strong> {doctorInfo.email}</p>
                        <p><strong>Address:</strong> {doctorInfo.address || 'N/A'}</p>
                        <p><strong>Doctor ID:</strong> {doctorInfo.doctor_id || 'N/A'}</p>
                        <p><strong>Role:</strong> Doctor</p>
                    </div>
                ) : (
                    <p>Loading doctor profile...</p>
                )}

                <div className="mt-6">
                    <ul className="list-disc pl-5 space-y-2 text-gray-700">
                        <li>View assigned patients - future</li>
                        <li>Access patient records - Not yet done</li>
                    </ul>
                </div>
            </div>
        </>
    )
}
