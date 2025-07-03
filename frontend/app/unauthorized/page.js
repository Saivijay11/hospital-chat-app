export default function Unauthorized() {
    return (
        <div style={{ textAlign: 'center', marginTop: '5rem' }}>
            <h2>Unauthorized Access</h2>
            <p>You must be logged in to view this page.</p>
            <a href="/login">Go to Login</a>
        </div>
    )
}
