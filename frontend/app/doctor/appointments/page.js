'use client'

import DashboardHeader from '@/components/DashboardHeader'

export default function DoctorAppointmentsPage() {
    return (
        <>
            <DashboardHeader />
            <div className="p-6 max-w-4xl mx-auto">
                <h2 className="text-2xl font-bold mb-4">Upcoming Appointments</h2>
                <ul className="list-none space-y-3">
                    <li className="bg-gray-100 p-3 rounded shadow">
                        📅 <strong>July 3rd</strong> – Ravi Kumar @ 10:00 AM
                    </li>
                    <li className="bg-gray-100 p-3 rounded shadow">
                        📅 <strong>July 3rd</strong> – Padmavathi @ 2:00 PM
                    </li>
                    <li className="bg-gray-100 p-3 rounded shadow">
                        📅 <strong>July 4th</strong> – Vijay @ 11:30 AM
                    </li>
                </ul>
            </div>
        </>
    )
}
