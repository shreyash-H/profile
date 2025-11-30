import React, { useState } from 'react';
import '../styles/main.css';

const mockProjects = [
  { id: 1, title: 'Nebula Player', subtitle: 'Mobile streaming UI', description: 'A lightweight streaming player.', price: '$19', tags: ['React','Tailwind'] },
  { id: 2, title: 'Astro Pivot Tool', subtitle: 'Trading analytics', description: 'Combines Gann windows and planetary pivots.', price: '$49', tags: ['FastAPI','Mongo'] },
  { id: 3, title: 'Seniors Directory', subtitle: 'Instagram-first directory', description: 'Responsive directory focused on seniors.', price: 'Free', tags: ['React','Accessibility'] }
];

export default function Portfolio3D(){
  const [selected,setSelected]=useState(null);
  const [query,setQuery]=useState('');
  const filtered = mockProjects.filter(p=>p.title.toLowerCase().includes(query.toLowerCase()));
  const handleBuy = (p)=> alert(`Buy: ${p.title}`);

  return (
    <main className="container">
      <header className="header">
        <div>
          <h1 className="title">Hey bodixif554 — 3D Portfolio</h1>
          <p className="subtitle">Quick input needed</p>
        </div>
        <div>
          <button className="btn" onClick={()=>alert('Buy clicked')}>Buy →</button>
        </div>
      </header>

      <section className="quick">
        <input value={query} onChange={(e)=>setQuery(e.target.value)} placeholder="Search projects..." />
        <button onClick={()=>alert('Saved')}>Save</button>
      </section>

      <section className="grid">
        {filtered.map(p=>(
          <article key={p.id} className="card" onMouseEnter={()=>setSelected(p.id)} onMouseLeave={()=>setSelected(null)} tabIndex={0} role="article" aria-labelledby={`project-${p.id}`}>
            <div className="card-inner">
              <div className="card-front">
                <h3 id={`project-${p.id}`}>{p.title}</h3>
                <p>{p.subtitle}</p>
                <p>{p.description}</p>
                <div className="card-footer">
                  <span>{p.price}</span>
                  <button onClick={()=>handleBuy(p)}>Buy</button>
                </div>
              </div>
              <div className="card-back" aria-hidden>
                <h4>Details</h4>
                <p>Tags: {p.tags.join(', ')}</p>
                <button onClick={()=>alert('Open')}>Open</button>
              </div>
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}
