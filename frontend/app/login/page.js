'use client'

import { useState } from 'react'
import axios from '../../utils/axiosInstance'
import { useRouter } from 'next/navigation'
import { jwtDecode } from 'jwt-decode'
import styles from '../../styles/form.module.css'

export default function LoginPage() {
    const [form, setForm] = useState({ identifier: '', password: '' })
    const [error, setError] = useState('')
    const router = useRouter()

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const payload = {
                username: form.identifier,
                password: form.password
            }
            const res = await axios.post('/users/login/', payload)
            const access = res.data.access
            const refresh = res.data.refresh

            localStorage.setItem('access_token', access)
            localStorage.setItem('refresh_token', refresh)
            console.log('🔐 Response Data:', res.data)
            if (res.data?.is_admin === true) {
                setTimeout(() => router.push('/admin'), 0)
            } else if (res.data?.is_doctor === true) {
                setTimeout(() => router.push('/doctor'), 0)
            } else if (res.data?.is_patient === true) {
                setTimeout(() => router.push('/patient'), 0)
            } else {
                console.log("🚫 Unrecognized role in login response", res.data)
                setTimeout(() => router.push('/unauthorized'), 0)
            }

        } catch (err) {
            console.error('Login error:', err.response?.data || err.message)
            setError('Invalid credentials')
        }
    }

    return (
        <div className={styles.formContainer}>
            <h2 className={styles.formTitle}>Login</h2>
            {error && <p className={styles.errorMsg}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    className={styles.inputField}
                    name="identifier"
                    placeholder="Username or Email"
                    onChange={handleChange}
                    required
                />
                <input
                    className={styles.inputField}
                    name="password"
                    type="password"
                    placeholder="Password"
                    onChange={handleChange}
                    required
                />
                <button type="submit" className={styles.submitButton}>Login</button>
            </form>
        </div>
    )
}
