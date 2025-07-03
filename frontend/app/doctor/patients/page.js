'use client'

import { useEffect, useState } from 'react'
import DashboardHeader from '@/components/DashboardHeader'
import axios from '@/utils/axiosInstance'

export default function DoctorPatientsPage() {
    const [patients, setPatients] = useState([])

    useEffect(() => {
        const fetchPatients = async () => {
            try {
                const res = await axios.get('/users/patients/')
                setPatients(res.data)
            } catch (err) {
                console.error("Failed to load patients:", err)
            }
        }

        fetchPatients()
    }, [])

    return (
        <>
            <DashboardHeader />
            <div className="p-6 max-w-4xl mx-auto">
                <h2 className="text-2xl font-bold mb-4">My Patients</h2>
                <ul className="list-disc pl-6 space-y-2">
                    {patients.map((patient) => (
                        <li key={patient.username}>
                            {patient.full_name || patient.username} – Blood Type: {patient.blood_type || 'N/A'}
                        </li>
                    ))}
                </ul>
                <p className="mt-4 text-gray-500">Fetched from system based on role-based registration.</p>
            </div>
        </>
    )
}
