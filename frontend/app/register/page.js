'use client'

import { useState } from 'react'
import axios from '../../utils/axiosInstance'
import { useRouter } from 'next/navigation'
import styles from '../../styles/form.module.css'

export default function RegisterPage() {
    const [form, setForm] = useState({
        username: '', email: '', password: '', full_name: '',
        address: '', blood_type: '', role: 'patient', doctor_id: ''
    })
    const [error, setError] = useState('')
    const router = useRouter()

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        try {
            await axios.post('/users/register/', form)
            alert('Registered successfully!')
            router.push('/login')
        } catch (err) {
            console.error('Registration error:', err?.response?.data || err.message)
            if (err?.response?.data) {
                const firstErrorKey = Object.keys(err.response.data)[0]
                const firstErrorMsg = err.response.data[firstErrorKey][0]
                setError(firstErrorMsg)
            } else {
                setError('Registration failed')
            }
        }

    }


    return (
        <div className={styles.formContainer}>
            <h2 className={styles.formTitle}>Register</h2>
            {error && <p className={styles.errorMsg}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input className={styles.inputField} name="username" placeholder="Username" onChange={handleChange} required />
                <input className={styles.inputField} name="email" type="email" placeholder="Email" onChange={handleChange} required />
                <input className={styles.inputField} name="password" type="password" placeholder="Password" onChange={handleChange} required />
                <input className={styles.inputField} name="full_name" placeholder="Full Name" onChange={handleChange} />
                <input className={styles.inputField} name="address" placeholder="Address" onChange={handleChange} />
                <input className={styles.inputField} name="blood_type" placeholder="Blood Type (e.g. A+)" onChange={handleChange} />

                <select name="role" className={styles.selectField} onChange={handleChange} value={form.role}>
                    <option value="patient">Patient</option>
                    <option value="doctor">Doctor</option>
                </select>

                {form.role === 'doctor' && (
                    <input className={styles.inputField} name="doctor_id" placeholder="Doctor ID" onChange={handleChange} required />
                )}

                <button type="submit" className={styles.submitButton}>Register</button>
            </form>
        </div>
    )
}
