export default function Message({ msg, currentUser }) {
    const isOwn = msg.sender === currentUser;

    return (
        <div className={`mb-2 ${isOwn ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block px-4 py-2 rounded ${isOwn ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
                <strong>{msg.sender}</strong><br />
                {msg.message} <br />
                <small className="text-xs">{msg.timestamp}</small>
            </div>
        </div>
    )
}
