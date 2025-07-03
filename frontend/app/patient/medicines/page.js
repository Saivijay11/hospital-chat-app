'use client'

export default function MedicinesPage() {
    const medicines = [
        { name: "Paracetamol", use: "Fever and pain relief" },
        { name: "Amoxicillin", use: "Bacterial infections" },
        { name: "Metformin", use: "Type 2 Diabetes" },
        { name: "Atorvastatin", use: "Cholesterol control" },
    ]

    return (
        <div className="p-6 max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold mb-4">Available Medicines</h2>
            <ul className="space-y-3">
                {medicines.map((med, idx) => (
                    <li key={idx} className="bg-gray-100 p-4 rounded-md shadow">
                        <p><strong>{med.name}</strong></p>
                        <p className="text-sm text-gray-600">Usage: {med.use}</p>
                    </li>
                ))}
            </ul>
        </div>
    )
}
