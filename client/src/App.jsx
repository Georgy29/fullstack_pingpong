import { useEffect, useState } from 'react'
import { apiFetch } from './api' 

export default function App() {
  const [msg, setMsg] = useState('...')
  const [todos, setTodos] = useState([])
  const [title, setTitle] = useState('')

  const ping = async () => {
    const t = await (await apiFetch('/api/ping')).text()
    setMsg(t)
  }

  useEffect(() => {
    apiFetch('/api/todos').then(r => r.json()).then(setTodos)
  }, [])

  const addTodo = async (e) => {
    e.preventDefault()
    if (!title.trim()) return
    const res = await apiFetch('/api/todos', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ title })
    })
    const created = await res.json()
    setTodos(v => [...v, created])
    setTitle('')
  }

  const toggle = async (id) => {
    const r = await apiFetch(`/api/todos/${id}`, { method:'PATCH' })
    const upd = await r.json()
    setTodos(v => v.map(t => t.id === id ? upd : t))
  }

  const remove = async (id) => {
    await apiFetch(`/api/todos/${id}`, { method:'DELETE' })
    setTodos(v => v.filter(t => t.id !== id))
  }

  return (
    <div style={{ padding: 24, fontFamily: 'system-ui, sans-serif', maxWidth: 640, margin: '0 auto' }}>
      <h1>Mini Full-Stack</h1>

      <button onClick={ping}>Ping API</button>
      <p>Response: {msg}</p>

      <form onSubmit={addTodo} style={{ margin: '16px 0' }}>
        <input
          value={title}
          onChange={e=>setTitle(e.target.value)}
          placeholder="New todo..."
          style={{ padding: 8, width: '70%' }}
        />
        <button type="submit" style={{ padding: 8, marginLeft: 8 }}>Add</button>
      </form>

      <ul style={{ listStyle:'none', padding:0 }}>
        {todos.map(t => (
          <li key={t.id} style={{ display:'flex', alignItems:'center', gap:8, borderBottom:'1px solid #eee', padding:'8px 0' }}>
            <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} />
            <span style={{ flex:1, textDecoration: t.done ? 'line-through' : 'none' }}>{t.title}</span>
            <button onClick={() => remove(t.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
