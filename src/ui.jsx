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

export function Avatar({ m, size = 26, ring, dim, className = '' }) {
  return (
    <span className={`av ${dim ? 'dim' : ''} ${className}`} style={{ width: size, height: size, fontSize: size * 0.42, background: m.color, '--ring': ring }}>
      {m.initial}
    </span>
  )
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

export function Row({ icon, iconText, bg, fg, label, title, meta, onClick, selected, right, avatar }) {
  return (
    <button className={`card row ${selected ? 'selected' : ''}`} onClick={onClick}>
      {avatar ? <Avatar m={avatar} size={46} ring="#fff" /> : (
        <span className="ic" style={{ background: bg, color: fg }}>
          {icon ? <Icon name={icon} /> : iconText}
        </span>
      )}
      <span className="txt">
        {label && <span className="l">{label}</span>}
        <span className="t" style={{ display: 'block' }}>{title}</span>
        {meta && <span className="m" style={{ display: 'block' }}>{meta}</span>}
      </span>
      {right ?? <span className="arrow"><Icon name="arrow_forward" /></span>}
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
