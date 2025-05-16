// frontend/src/app/page.tsx

async function getF1Events() {
  const res = await fetch('http://localhost:8000/events', {
    next: { revalidate: 60 }, // Optional: cache revalidation
  })

  if (!res.ok) throw new Error('Failed to fetch events')

  const data = await res.json()
  return data.events
}

export default async function Home() {
  const events = await getF1Events()

  return (
    <main className="p-4">
      <h1 className="text-2xl font-bold mb-4">F1 Events (Current Season)</h1>
      <ul className="space-y-2">
        {events.map((event: any) => (
          event.status === 'passed' ? (
          <li key={event.id} className="p-4 border rounded shadow">
            <h2 className="text-xl font-semibold">{event.name}</h2>
            <p>{event.session5_date}</p>
            <p>{event.location} {event.country}</p>
          </li>)
          : (
          <li key={event.id} className="p-4 border rounded shadow">
            <h3 className="text-xl font-semibold">{event.name}</h3>
            <p>{event.session5_date}</p>
            <p>{event.location} {event.country}</p>
          </li>)
        ))}
      </ul>
    </main>
  )
}
