'use client'

import { useRouter } from 'next/navigation'

export default function HomePage() {
    const router = useRouter()

    return (
        <main style={{ textAlign: 'center', paddingTop: '4rem' }}>
            <h1>Welcome to HIPAA-Compliant Hospital Chat System</h1>
            <p>Select your login type:</p>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '2rem' }}>
                <button onClick={() => router.push('/login')} style={btnStyle}>Patient/Doctor Login</button>
                <button onClick={() => router.push('/admin/login')} style={btnStyle}>Admin Login</button>
            </div>
        </main>
    )
}

const btnStyle = {
    padding: '0.8rem 2rem',
    backgroundColor: '#0070f3',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer'
}
