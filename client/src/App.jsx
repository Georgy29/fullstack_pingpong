import { useState } from 'react'

export default function App() {
  const [msg, setMsg] = useState('...')

  const ping = async () => {
    const t = await (await fetch('/api/ping')).text()
    setMsg(t)
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Ping-Pong App</h1>
      <button onClick={ping}>Ping API</button>
      <p>Response: {msg}</p>
    </div>
  )
}
