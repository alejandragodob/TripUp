import React from 'react'

export const Icon = ({ name, fill, className = '', style }) => (
  <span className={`ms ${fill ? 'fill' : ''} ${className}`} style={style} aria-hidden="true">{name}</span>
)

export function StatusBar({ light }) {
  return (
    <div className="status" style={light ? { color: '#fff' } : undefined}>
      <span className="time">9:41</span>
      <span className="island" />
      <span className="right">
        <span className="bars"><i style={{ height: 4 }} /><i style={{ height: 7 }} /><i style={{ height: 10 }} /><i style={{ height: 12 }} /></span>
        <span className="batt" />
      </span>
    </div>
  )
}

export function TopBar({ onBack, right, label, left }) {
  return (
    <div className="topbar">
      {left ?? (onBack ? <button className="circle-btn" onClick={onBack} aria-label="Back"><Icon name="arrow_back" /></button> : <span />)}
      {label ? <span className="label">{label}</span> : right}
    </div>
  )
}

// Photo avatar when the file exists (public/img/avatars/<name>.jpg), initials otherwise.
const missing = new Set()
export function Avatar({ m, size = 26, ring, dim, className = '' }) {
  const [broken, setBroken] = React.useState(() => !m.photo || missing.has(m.photo))
  return (
    <span className={`av ${dim ? 'dim' : ''} ${className}`} style={{ width: size, height: size, fontSize: size * 0.42, background: m.color, '--ring': ring, overflow: 'hidden' }}>
      {!broken && <img src={m.photo} alt={m.name} width={size} height={size} style={{ width: '100%', height: '100%', objectFit: 'cover' }} onError={() => { missing.add(m.photo); setBroken(true) }} />}
      {broken && m.initial}
    </span>
  )
}

// Photo with a graceful fallback (used for event thumbnails).
export function Photo({ src, alt = '', fallback, className = '', style }) {
  const [broken, setBroken] = React.useState(!src)
  if (broken) return fallback
  return <img src={src} alt={alt} className={className} style={style} onError={() => setBroken(true)} />
}

// Payment rail marks. Wordmarks and the Apple glyph are drawn inline so they render offline.
export function RailLogo({ id, size = 46 }) {
  const box = { width: size, height: size, borderRadius: '50%', display: 'grid', placeItems: 'center', flex: 'none' }
  if (id === 'applepay') return (
    <span style={{ ...box, background: '#000', color: '#fff' }} aria-label="Apple Pay">
      <svg width={size * 0.62} height={size * 0.3} viewBox="0 0 62 30" fill="none" aria-hidden="true">
        <path fill="#fff" d="M13.7 5.3c-.8 1-2.1 1.7-3.3 1.6-.2-1.3.5-2.6 1.2-3.4.8-1 2.2-1.7 3.3-1.7.1 1.3-.4 2.6-1.2 3.5Zm1.2 1.9c-1.8-.1-3.4 1-4.2 1-.9 0-2.2-1-3.6-.9-1.9 0-3.6 1.1-4.5 2.8-2 3.4-.5 8.4 1.4 11.1.9 1.3 2 2.8 3.5 2.8 1.4-.1 1.9-.9 3.6-.9s2.2.9 3.6.9c1.5 0 2.5-1.3 3.4-2.7 1.1-1.5 1.5-3 1.5-3.1 0 0-2.9-1.1-3-4.5 0-2.8 2.3-4.2 2.4-4.2-1.3-1.9-3.3-2.2-4.1-2.3Z"/>
        <text x="24" y="21" fill="#fff" fontFamily="Figtree, system-ui, sans-serif" fontSize="19" fontWeight="600" letterSpacing="-0.5">Pay</text>
      </svg>
    </span>
  )
  if (id === 'revolut') return (
    <span style={{ ...box, background: '#fff', boxShadow: 'inset 0 0 0 1px var(--hair)' }} aria-label="Revolut">
      <img src="img/revolut.png" alt="" width={size * 0.6} height={size * 0.6} style={{ width: size * 0.6, height: size * 0.6 }} />
    </span>
  )
  if (id === 'wise') return (
    <span style={{ ...box, background: '#9FE870', color: '#163300' }} aria-label="Wise">
      <svg width={size * 0.62} height={size * 0.3} viewBox="0 0 60 30" aria-hidden="true">
        <text x="30" y="22" textAnchor="middle" fill="#163300" fontFamily="Figtree, system-ui, sans-serif" fontSize="21" fontWeight="800" letterSpacing="-1">wise</text>
      </svg>
    </span>
  )
  if (id === 'bank') return <span style={{ ...box, background: 'var(--beige)' }}><Icon name="account_balance" style={{ fontSize: 22 }} /></span>
  return <span style={{ ...box, background: 'var(--beige)' }}><Icon name="payments" style={{ fontSize: 22 }} /></span>
}

export function AvatarStack({ members, size = 26, ring, dim = [], onAdd }) {
  return (
    <span className="av-stack">
      {members.map((m) => <Avatar key={m.id} m={m} size={size} ring={ring} dim={dim.includes(m.id)} />)}
      {onAdd && <button className="av add" style={{ width: size, height: size, marginLeft: -10 }} onClick={onAdd} aria-label="Add someone"><Icon name="add" style={{ fontSize: 16 }} /></button>}
    </span>
  )
}

export function Pill({ children, onClick, disabled, icon = 'arrow_forward' }) {
  return (
    <button className="pill" onClick={onClick} disabled={disabled}>
      <span>{children}</span>
      <span className="go"><Icon name={icon} /></span>
    </button>
  )
}

export function Chip({ children, icon, solid, soft, beige, strike, onClick, className = '' }) {
  return (
    <button className={`chip ${solid ? 'solid' : ''} ${soft ? 'soft' : ''} ${beige ? 'beige' : ''} ${strike ? 'outline-strike' : ''} ${className}`} onClick={onClick}>
      {icon && <Icon name={icon} />}
      {children}
    </button>
  )
}

export function Row({ icon, iconText, bg, fg, label, title, meta, onClick, selected, right, avatar, photo }) {
  return (
    <button className={`card row ${selected ? 'selected' : ''}`} onClick={onClick} disabled={!onClick} style={!onClick ? { cursor: 'default' } : undefined}>
      {avatar ? <Avatar m={avatar} size={46} ring="#fff" /> : photo ? (
        <span className="thumb" style={{ background: bg }}>
          <Photo src={photo} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} fallback={<span className="ic" style={{ background: bg, color: fg, width: 46, height: 46 }}>{icon ? <Icon name={icon} /> : iconText}</span>} />
          {iconText && <span className="thumb-tag">{iconText}</span>}
        </span>
      ) : (
        <span className="ic" style={{ background: bg, color: fg }}>
          {icon ? <Icon name={icon} /> : iconText}
        </span>
      )}
      <span className="txt">
        {label && <span className="l">{label}</span>}
        <span className="t" style={{ display: 'block' }}>{title}</span>
        {meta && <span className="m" style={{ display: 'block' }}>{meta}</span>}
      </span>
      {right ?? (onClick ? <span className="arrow"><Icon name="arrow_forward" /></span> : null)}
    </button>
  )
}

export function TabBar({ active, onTab, badge }) {
  const tabs = [
    ['Trips', 'home'],
    ['Polls', 'how_to_vote'],
    ['Plan', 'calendar_month'],
    ['Money', 'account_balance_wallet'],
  ]
  return (
    <nav className="tabs">
      {tabs.map(([name, icon]) => (
        <button key={name} className={active === name ? 'on' : ''} onClick={() => onTab(name)}>
          {badge === name && <span className="badge" />}
          <Icon name={icon} fill={active === name} />
          {name}
        </button>
      ))}
      <span className="home-indicator" />
    </nav>
  )
}

export function Sheet({ children, onClose }) {
  return (
    <>
      <div className="dim" onClick={onClose} />
      <div className="sheet" role="dialog">
        <div className="grab" />
        <div className="body">{children}</div>
      </div>
    </>
  )
}

export function Toast({ text }) {
  return text ? <div className="toast" key={text}>{text}</div> : null
}

export function Section({ children, right, onRight }) {
  return (
    <div className="section">
      <span>{children}</span>
      {right && <button className="right" onClick={onRight}>{right}</button>}
    </div>
  )
}
