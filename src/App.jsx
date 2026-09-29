import React, { useEffect, useMemo, useRef, useState } from 'react'
import { MEMBERS, REN, TRIP, OTHER_TRIPS, ITINERARY, OPTIONS, EXPENSE, BALANCES, RAILS, PLACES, mapsUrl, directionsUrl } from './data.js'
import { Icon, StatusBar, TopBar, Avatar, AvatarStack, Pill, Chip, Row, TabBar, Sheet, Toast, Section, Photo, RailLogo } from './ui.jsx'

const byId = (list, id) => list.find((m) => m.id === id)
const names = (list, ids) => ids.map((id) => (id === 'A' ? 'You' : byId(list, id)?.name)).filter(Boolean)

export default function App() {
  const [screen, setScreen] = useState('home')
  const [dir, setDir] = useState('fwd')
  const [members, setMembers] = useState(MEMBERS)
  const [sheet, setSheet] = useState(null) // 'addRen' | 'notifications' | 'newTrip'
  const [toast, setToast] = useState('')
  const [pollStatus, setPollStatus] = useState('draft')
  const [options, setOptions] = useState(OPTIONS)
  const [votes, setVotes] = useState(() => Object.fromEntries(OPTIONS.map((o) => [o.id, o.votes])))
  const [wineOut, setWineOut] = useState(EXPENSE.items[1].excluded)
  const [paid, setPaid] = useState({})
  const [settle, setSettle] = useState(null)
  const [expenseLogged, setExpenseLogged] = useState(false)
  const toastTimer = useRef()

  const go = (s, back) => { setDir(back ? 'back' : 'fwd'); setScreen(s); setSheet(null) }
  const say = (t) => { setToast(t); clearTimeout(toastTimer.current); toastTimer.current = setTimeout(() => setToast(''), 1800) }

  const renIn = members.some((m) => m.id === 'R')
  const addRen = () => { if (!renIn) setMembers([...members, REN]); setSheet(null); say('Ren joined · 6 in Lisbon') }

  const v = (id) => votes[id] || []
  const totalVotes = options.reduce((n, o) => n + v(o.id).length, 0)
  const sorted = useMemo(() => [...options].sort((a, b) => (votes[b.id] || []).length - (votes[a.id] || []).length), [options, votes])
  const leader = sorted[0]
  const notVoted = members.filter((m) => !options.some((o) => v(o.id).includes(m.id)))
  const majority = v(leader.id).length > members.length / 2

  // Live poll simulation: Theo votes for the leader ~4s after the poll opens on screen.
  useEffect(() => {
    if (screen !== 'poll' || pollStatus !== 'live') return
    if (options.some((o) => v(o.id).includes('T'))) return
    const t = setTimeout(() => {
      setVotes((vv) => ({ ...vv, [leader.id]: [...(vv[leader.id] || []), 'T'] }))
      say('Theo voted · ' + leader.name)
    }, 4000)
    return () => clearTimeout(t)
  }, [screen, pollStatus]) // eslint-disable-line

  const castVote = (id) => {
    if (pollStatus !== 'live') return
    setVotes((vv) => {
      const next = {}
      for (const k of Object.keys(vv)) next[k] = vv[k].filter((m) => m !== 'A')
      next[id] = [...(next[id] || []), 'A']
      return next
    })
  }

  const onTab = (name) => {
    if (name === 'Trips') go('home', true)
    if (name === 'Polls') go(pollStatus === 'draft' ? 'polls' : 'poll')
    if (name === 'Plan') go('plan')
    if (name === 'Money') go('balances')
  }

  const markPaid = (rail) => {
    const next = { ...paid, [settle.id]: rail }
    setPaid(next)
    setSettle(null)
    say(`${byId(members, settle.from)?.name} · ${rail.name} · settled`)
    if (BALANCES.transfers.every((t) => next[t.id])) setTimeout(() => go('settled'), 900)
  }

  // Reset the whole scenario so the demo can be run again from the top.
  const restart = () => {
    setMembers(MEMBERS); setPollStatus('draft'); setOptions(OPTIONS)
    setVotes(Object.fromEntries(OPTIONS.map((o) => [o.id, o.votes])))
    setWineOut(EXPENSE.items[1].excluded); setPaid({}); setSettle(null); setExpenseLogged(false)
    go('home', true); say('Demo reset. Lisbon, day 4, 18:52')
  }

  const shared = { members, go, say, onTab, openSheet: setSheet, pollStatus }

  return (
    <div className="stage">
      <div className="phone">
        {screen === 'home' && <Home {...shared} pollStatus={pollStatus} />}
        {screen === 'trip' && <Trip {...shared} renIn={renIn} openAdd={() => setSheet('addRen')} pollStatus={pollStatus} />}
        {screen === 'ren' && <RenSide {...shared} onJoin={() => { addRen(); go('trip', true) }} />}
        {screen === 'createPoll' && <CreatePoll {...shared} options={options} setOptions={setOptions} onSend={() => { setPollStatus('live'); go('chat') }} />}
        {screen === 'chat' && <Chat {...shared} options={sorted} votes={votes} totalVotes={totalVotes} onOpen={() => go('poll')} />}
        {screen === 'poll' && <LivePoll {...shared} options={sorted} votes={votes} totalVotes={totalVotes} notVoted={notVoted} leader={leader} majority={majority} status={pollStatus} castVote={castVote} onClose={() => { setPollStatus('closed'); go('plan') }} />}
        {screen === 'polls' && <PollsStub {...shared} />}
        {screen === 'plan' && <Plan {...shared} leader={leader} totalVotes={totalVotes} pollStatus={pollStatus} expenseLogged={expenseLogged} onLog={() => go('expense')} />}
        {screen === 'expense' && <Expense {...shared} wineOut={wineOut} setWineOut={setWineOut} onSave={() => { setExpenseLogged(true); go('balances'); say(`${members.length} balances updated`) }} />}
        {screen === 'balances' && <Balances {...shared} paid={paid} onPick={(t) => setSettle(t)} />}
        {screen === 'settled' && <Settled {...shared} paid={paid} onNext={restart} />}

        {sheet === 'notifications' && <Notifications members={members} pollStatus={pollStatus} expenseLogged={expenseLogged} onClose={() => setSheet(null)} go={go} />}
        {sheet === 'newTrip' && <NewTrip onClose={() => setSheet(null)} say={say} />}
        {sheet === 'addRen' && <AddRen members={members} renIn={renIn} onClose={() => setSheet(null)} onAdd={addRen} onPreview={() => go('ren')} />}
        {settle && <SettleSheet t={settle} members={members} onClose={() => setSettle(null)} onPick={markPaid} />}
        <Toast text={toast} />
      </div>
    </div>
  )
}

/* ---------- 01 Home ---------- */
function Home({ members, go, onTab, pollStatus, openSheet, say }) {
  return (
    <div className="screen back">
      <StatusBar />
      <TopBar left={<span className="hi">Hi Ari</span>} right={<button className="circle-btn" aria-label="Notifications" onClick={() => openSheet('notifications')}><Icon name="notifications" /></button>} />
      <div className="scroll has-tabs">
        <h1 className="title">Your trips<span className="sub">one happening now</span></h1>
        <div className="panel" style={{ padding: 12 }}>
          <img src={TRIP.hero} alt="Lisbon" style={{ width: '100%', height: 110, objectFit: 'cover', borderRadius: 16 }} />
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', margin: '12px 4px 4px' }}>
            <span style={{ fontFamily: 'var(--display)', fontSize: 28 }}>Lisbon</span>
            <AvatarStack members={members} size={26} ring="var(--beige)" />
          </div>
          <div className="meta" style={{ margin: '0 4px 10px' }}>{TRIP.dates} · Day {TRIP.day} of {TRIP.days} · {members.length} friends</div>
          <div className="chips" style={{ marginBottom: 12 }}>
            <Chip soft onClick={() => go(pollStatus === 'draft' ? 'trip' : pollStatus === 'live' ? 'poll' : 'plan')}>{pollStatus === 'closed' ? 'Tonight: Ramiro at 19:30' : 'Tonight: dinner still open'}</Chip>
            <Chip soft onClick={() => go('balances')}>You're owed €42</Chip>
          </div>
          <Pill onClick={() => go('trip')}>Open trip</Pill>
        </div>
        <Section>Coming up</Section>
        <div className="stack">
          {OTHER_TRIPS.map((t) => (
            <button key={t.id} className="card row" onClick={() => say(t.id === 'primavera' ? 'Primavera opens Jun 3. Nothing to decide yet' : 'New York is settled. Archive opens here')}>
              <Photo src={t.photo} className="event-thumb" fallback={<span className="ic" style={{ background: t.bg, color: t.fg }}><Icon name={t.icon} /></span>} />
              <span className="txt"><span className="l">{t.tag}</span><span className="t" style={{ display: 'block' }}>{t.title}</span><span className="m" style={{ display: 'block' }}>{t.meta}</span></span>
              <span className="arrow"><Icon name="arrow_forward" /></span>
            </button>
          ))}
          <div className="chips">
            <Chip icon="add" onClick={() => openSheet('newTrip')}>New trip</Chip>
            <Chip onClick={() => say('Reads your Splitwise groups. Mocked in this demo')}>Import from Splitwise</Chip>
          </div>
        </div>
      </div>
      <TabBar active="Trips" onTab={onTab} badge={pollStatus === 'live' ? 'Polls' : null} />
    </div>
  )
}

/* ---------- 02 Trip group view ---------- */
function Trip({ members, go, onTab, openAdd, renIn, pollStatus, openSheet }) {
  return (
    <div className="screen">
      <StatusBar />
      <TopBar onBack={() => go('home', true)} right={<button className="circle-btn" aria-label="Notifications" onClick={() => openSheet('notifications')}><Icon name="notifications" /></button>} />
      <div className="scroll has-tabs">
        <h1 className="title">Last night in<span className="sub">Lisbon</span></h1>
        <div style={{ position: 'relative', height: 104, borderRadius: 20, overflow: 'hidden' }}>
          <img src={TRIP.photo} alt="Lisbon" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(20,20,20,0) 20%, rgba(20,20,20,.75))' }} />
          <div style={{ position: 'absolute', left: 14, right: 14, bottom: 10, color: '#fff', fontSize: 13, fontWeight: 500 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
              <span style={{ fontSize: 11, opacity: .8 }}>{members.length} friends{renIn ? '' : ' · Ren joins tonight'}</span>
              <AvatarStack members={members} size={26} ring="#4A4038" onAdd={renIn ? undefined : openAdd} />
            </div>
            <div style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              <b>Nic</b> <span style={{ background: '#fff', color: 'var(--ink)', fontSize: 9, fontWeight: 700, letterSpacing: .6, borderRadius: 4, padding: '2px 5px', margin: '0 4px' }}>ORGANIZER</span>
              · Ari · Maya · Theo · Sam{renIn ? ' · Ren' : ''}
            </div>
          </div>
        </div>
        <div className="panel" style={{ marginTop: 12 }}>
          {pollStatus === 'draft' && <>
            <h3>Dinner tonight is still open</h3>
            <p>Three places from the group's wishlist, ready to poll.</p>
            <Pill onClick={() => go('createPoll')}>Start the poll</Pill>
          </>}
          {pollStatus === 'live' && <>
            <h3>Dinner poll is live</h3>
            <p>Votes are coming in. Close it once a majority agrees.</p>
            <Pill onClick={() => go('poll')}>Open the poll</Pill>
          </>}
          {pollStatus === 'closed' && <>
            <h3>Ramiro at 19:30</h3>
            <p>Won tonight's poll. Directions and booking are in the plan.</p>
            <Pill onClick={() => go('plan')}>See tonight's plan</Pill>
          </>}
        </div>
        <Section right="Full plan" onRight={() => go('plan')}>Today</Section>
        <div className="stack">
          {ITINERARY.map((i) => <Row key={i.id} iconText={i.time} bg={i.bg} fg={i.fg} photo={i.photo} label={i.label} title={i.title} meta={i.id === 'lx' ? i.meta : undefined} onClick={() => go('plan')} />)}
          <Row iconText="€" bg="var(--peri)" fg="var(--peri-fg)" label="Trip money" title="You're owed €42" meta="Settle with Apple Pay or Revolut" onClick={() => go('balances')} />
        </div>
      </div>
      <TabBar active="Trips" onTab={onTab} badge={pollStatus === 'live' ? 'Polls' : null} />
    </div>
  )
}

/* ---------- 03 Add Ren (sheet) ---------- */
function AddRen({ onClose, onAdd, onPreview, renIn }) {
  const [tonightOnly, setTonightOnly] = useState(true)
  return (
    <Sheet onClose={onClose}>
      <h1 className="title sm" style={{ margin: '6px 0 14px' }}>Add someone<span className="sub">to Lisbon</span></h1>
      <div className="stack">
        <Row icon="chat" bg="var(--mint)" fg="var(--mint-fg)" title="Share the join link" meta="Sends tripup.app/j/lisbon to your group chat" onClick={onPreview} />
        <div className="card steps">
          <div className="step"><span className="n">1</span><div><b>They tap the link</b><span>Opens in the browser, nothing to install</span></div></div>
          <div className="step"><span className="n">2</span><div><b>They confirm their number</b><span>We text a 4-digit code. No password, no profile</span></div></div>
          <div className="step"><span className="n">3</span><div><b>They're in</b><span>They can vote and pay from the chat right away</span></div></div>
        </div>
        <div className="or">or add from contacts</div>
        <Row avatar={REN} title="Ren Okafor" meta="+351 ··· 42 18 · joining for dinner tonight" selected right={<Icon name="check_circle" fill style={{ fontSize: 24 }} />} />
        <button className="card row" onClick={() => setTonightOnly(!tonightOnly)}>
          <span className="txt"><span className="t" style={{ display: 'block' }}>Joining tonight only</span><span className="m" style={{ display: 'block' }}>Skips the earlier expenses automatically</span></span>
          <span className={`toggle ${tonightOnly ? '' : 'off'}`} />
        </button>
        <Pill onClick={onAdd} disabled={renIn}>{renIn ? 'Ren is already in' : 'Add Ren'}</Pill>
        <button className="caption tap" style={{ justifyContent: 'center', width: '100%' }} onClick={onPreview}>See what Ren sees</button>
      </div>
    </Sheet>
  )
}

/* ---------- 03b Ren's side (mobile web) ---------- */
function RenSide({ members, go, onJoin }) {
  return (
    <div className="screen">
      <StatusBar />
      <div className="addr"><Icon name="lock" /> <span style={{ flex: 1 }}>tripup.app/j/lisbon</span><Icon name="more_horiz" /></div>
      <div className="scroll">
        <div className="hero-photo">
          <img src={TRIP.photo} alt="Lisbon" />
          <div className="avs"><AvatarStack members={members.filter((m) => m.id !== 'R')} size={28} ring="#4A4038" /></div>
        </div>
        <h1 className="title">Ari added you<span className="sub">to Lisbon</span></h1>
        <p className="meta" style={{ margin: '-6px 0 16px', lineHeight: 1.5, color: 'var(--muted)' }}>{TRIP.dates} · you're joining for dinner tonight. Confirm your number and you're in. No app, no password.</p>
        <div className="field"><span className="cc">+351</span><span style={{ flex: 1 }}>912 ··· 42 18</span><Icon name="sim_card" style={{ color: 'var(--grey)' }} /></div>
        <div style={{ margin: '14px 0 8px' }}><Pill onClick={onJoin}>Join as Ren</Pill></div>
        <p className="caption" style={{ textAlign: 'center', margin: '0 0 8px' }}>We text a 4-digit code. That's the whole sign-up.</p>
        <Section>What you can do from here</Section>
        <div className="stack">
          {[['how_to_vote', 'var(--peach)', 'var(--peach-fg)', "Vote on tonight's dinner", 'The poll is live now'],
            ['account_balance_wallet', 'var(--mint)', 'var(--mint-fg)', 'Pay your share', 'Apple Pay, Revolut or your bank'],
            ['download', 'var(--peri)', 'var(--peri-fg)', 'Get the app later', 'Optional']].map(([ic, bg, fg, t, m]) => (
            <Row key={t} icon={ic} bg={bg} fg={fg} title={t} meta={m} right={<span />} />
          ))}
        </div>
        <button className="caption tap" style={{ display: 'flex', margin: '12px auto 30px', padding: '0 12px' }} onClick={() => go('trip', true)}>Back to Ari's phone</button>
      </div>
    </div>
  )
}

/* ---------- 04 Create poll ---------- */
function CreatePoll({ go, options, setOptions, onSend, say }) {
  const [src, setSrc] = useState('wishlist')
  const [q, setQ] = useState('')
  const inPoll = (pl) => options.some((o) => o.id === pl.id)
  const add = (pl) => { if (inPoll(pl)) return; if (options.length >= 4) { say('Four options is plenty for one poll'); return } setOptions([...options, pl]); say(`${pl.name} added to the poll`) }
  const remove = (o) => setOptions(options.filter((x) => x.id !== o.id))
  const wishlist = PLACES.filter((pl) => pl.saved.length > 0)
  const near = PLACES.filter((pl) => pl.open && pl.walk <= 15).sort((x, y) => x.walk - y.walk)
  const found = q.trim().length ? PLACES.filter((pl) => (pl.name + ' ' + pl.meta).toLowerCase().includes(q.trim().toLowerCase())) : []
  const list = src === 'near' ? near.filter((pl) => !inPoll(pl)) : src === 'search' ? found : wishlist.filter((pl) => !inPoll(pl))
  return (
    <div className="screen">
      <StatusBar />
      <TopBar onBack={() => go('trip', true)} label="Draft · edit anything" />
      <div className="scroll has-sticky">
        <h1 className="title">Where for<span className="sub">dinner?</span></h1>
        <div className="stack">
          {options.map((o) => (
            <div key={o.id} className="card draft">
              <Photo src={o.photo} fallback={<span className="ph"><Icon name="restaurant" /></span>} />
              <div className="txt">
                <div className="n">{o.name}</div>
                <div className="m">{o.meta}</div>
                <div className="src"><span className="gbadge">G</span>{o.source}</div>
              </div>
              <div className="acts">
                <a className="icon-btn" href={mapsUrl(o.name)} target="_blank" rel="noreferrer" aria-label={`Open ${o.name} in Google Maps`}><Icon name="map" /></a>
                <button className="icon-btn" onClick={() => remove(o)} aria-label={`Remove ${o.name}`}><Icon name="close" /></button>
              </div>
            </div>
          ))}
          {options.length === 0 && <div className="empty"><Icon name="how_to_vote" />Add two or more places below.</div>}
        </div>

        <Section>Add a place</Section>
        <div className="chips scroll-x" style={{ marginBottom: 12 }}>
          <Chip icon="bookmark" solid={src === 'wishlist'} onClick={() => setSrc('wishlist')}>Wishlist · {wishlist.length}</Chip>
          <Chip icon="near_me" solid={src === 'near'} onClick={() => setSrc('near')}>Near me</Chip>
          <Chip icon="search" solid={src === 'search'} onClick={() => setSrc('search')}>Search Maps</Chip>
        </div>
        {src === 'search' && (
          <div className="search">
            <Icon name="search" style={{ color: 'var(--grey)' }} />
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search Google Maps in Lisbon" autoFocus aria-label="Search Google Maps" />
            {q && <button onClick={() => setQ('')} aria-label="Clear"><Icon name="close" style={{ fontSize: 18, color: 'var(--grey)' }} /></button>}
          </div>
        )}
        <p className="caption" style={{ margin: '0 0 12px' }}>
          {src === 'wishlist' && "Places your group saved in Google Maps. Ranked by how many of you saved them, then walking time."}
          {src === 'near' && 'Open now and within a 15 minute walk of the house.'}
          {src === 'search' && (q ? `${found.length} result${found.length === 1 ? '' : 's'} on Google Maps` : 'Anything you add joins the wishlist for next time.')}
        </p>
        <div className="stack">
          {list.map((pl) => (
            <div key={pl.id} className="card result">
              <Photo src={pl.photo} fallback={<span className="ph" style={{ width: 44, height: 44, borderRadius: 12, background: 'var(--beige)', display: 'grid', placeItems: 'center', color: 'var(--grey)', flex: 'none' }}><Icon name="restaurant" style={{ fontSize: 20 }} /></span>} style={{ width: 44, height: 44, borderRadius: 12, objectFit: 'cover', flex: 'none' }} />
              <div className="txt">
                <div className="n">{pl.name}{inPoll(pl) && <span className="in">IN THE POLL</span>}</div>
                <div className="m">{src === 'near' ? `${pl.walk} min walk · ${pl.short.split(' · ')[0]} · ${pl.source}` : pl.meta}</div>
              </div>
              <a className="icon-btn" href={mapsUrl(pl.name)} target="_blank" rel="noreferrer" aria-label={`Open ${pl.name} in Google Maps`}><Icon name="map" /></a>
              {!inPoll(pl) && <button className="icon-btn add" onClick={() => add(pl)} aria-label={`Add ${pl.name}`}><Icon name="add" /></button>}
            </div>
          ))}
          {src === 'search' && q && found.length === 0 && <div className="empty">No match in Lisbon. Try a dish or a neighbourhood.</div>}
        </div>

        <Section>Settings</Section>
        <div className="card">
          <div className="row" style={{ justifyContent: 'space-between', padding: '14px 16px' }}><span className="t">Closes</span><span className="meta" style={{ color: 'var(--ink)', fontWeight: 600 }}>when everyone has voted</span></div>
          <div style={{ height: 1, background: 'var(--hair)', margin: '0 16px' }} />
          <div className="row" style={{ justifyContent: 'space-between', padding: '14px 16px' }}><span className="t">Winner goes into tonight's plan</span><span className="meta" style={{ color: 'var(--ink)', fontWeight: 600 }}>19:30</span></div>
        </div>
      </div>
      <div className="sticky"><Pill onClick={onSend} disabled={options.length < 2}>{options.length < 2 ? 'Add at least two places' : 'Send to the group'}</Pill></div>
    </div>
  )
}

/* ---------- 05 Push + group chat ---------- */
function Chat({ members, options, votes, totalVotes, onOpen, go }) {
  const [push, setPush] = useState(true)
  useEffect(() => { const t = setTimeout(() => setPush(false), 6000); return () => clearTimeout(t) }, [])
  return (
    <div className="screen chat" style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,.22), rgba(255,255,255,.22)), url(img/chat-wallpaper.jpg)' }}>
      <StatusBar />
      {push && (
        <button className="push" onClick={onOpen}>
          <span className="app">t</span>
          <span style={{ flex: 1 }}>
            <span className="t">TripUp <span>now</span></span>
            <span className="b">Ari asks: Where for dinner? Ramiro · Taberna · Time Out. Tap to vote</span>
          </span>
        </button>
      )}
      <div className="head">
        <button onClick={() => go('createPoll', true)} aria-label="Back"><Icon name="arrow_back_ios" style={{ color: 'var(--blue)' }} /></button>
        <img className="gp" src={TRIP.group} alt="Lisboa group" />
        <div style={{ flex: 1 }}><div className="t">Lisboa</div><div className="s">{members.map((m) => m.name).join(', ')}</div></div>
        <Icon name="videocam" style={{ color: 'var(--blue)' }} /><Icon name="call" style={{ color: 'var(--blue)' }} />
      </div>
      <div className="body">
        {members.some((m) => m.id === 'R') && <div className="sys">Ren joined the trip via Ari's link</div>}
        <div className="bub"><div className="who m">Maya</div>ok back at the house, dinner?? I'm starving<div className="time">18:47</div></div>
        <div className="bub"><div className="who t">Theo</div>anything but a tourist trap pls<div className="time">18:49</div></div>
        <div className="bub out" style={{ padding: 6 }}>
          <div className="pollcard">
            <div className="k"><span>TRIPUP · LIVE POLL</span><b>{totalVotes} of {members.length} voted</b></div>
            <h4>Where for dinner?</h4>
            <p className="sub">Tap to vote · no app needed</p>
            {options.map((o, i) => (
              <div key={o.id} className={`o ${i === 0 && (votes[o.id] || []).length ? 'lead' : ''}`}>
                <Photo src={o.photo} fallback={<span style={{ width: 40, height: 40, borderRadius: 10, background: 'var(--beige)', display: 'grid', placeItems: 'center', color: 'var(--grey)', flex: 'none' }}><Icon name="restaurant" style={{ fontSize: 18 }} /></span>} />
                <div><div className="n">{o.name}</div><div className="m">{o.short}</div></div>
                <span className={`c ${(votes[o.id] || []).length ? '' : 'zero'}`}>{(votes[o.id] || []).length}</span>
              </div>
            ))}
            <button className="vote" onClick={onOpen}>Vote</button>
          </div>
          <div className="time">18:53 ✓✓</div>
        </div>
        <div className="bub"><div className="who s">Sam</div>voted, ramiro obviously<div className="time">18:54</div></div>
      </div>
      <div className="input"><Icon name="add" /><div className="box" /><Icon name="photo_camera" /><Icon name="mic" /></div>
      <span className="home-indicator" style={{ background: '#111' }} />
    </div>
  )
}

/* ---------- 06 Live poll ---------- */
function LivePoll({ members, go, onTab, options, votes, totalVotes, notVoted, leader, majority, status, castVote, onClose, say }) {
  const closed = status === 'closed'
  return (
    <div className="screen">
      <StatusBar />
      <TopBar onBack={() => go('trip', true)} right={<button className="circle-btn" aria-label="Share" onClick={() => go('chat')}><Icon name="ios_share" /></button>} />
      <div className="scroll has-sticky">
        <div className="card" style={{ padding: '14px 14px 14px', marginTop: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span className="ic" style={{ width: 46, height: 46, borderRadius: '50%', background: 'var(--peach)', color: 'var(--peach-fg)', display: 'grid', placeItems: 'center' }}><Icon name="restaurant" style={{ fontSize: 22 }} /></span>
            <span style={{ fontFamily: 'var(--display)', fontSize: 26 }}>Where for dinner?</span>
          </div>
          <div className="meta" style={{ margin: '12px 0 12px' }}>Tonight 19:30 · asked by Ari · <b style={{ color: 'var(--ink)' }}>{closed ? 'closed' : `${totalVotes} of ${members.length} voted`}</b></div>
          <div className="chips">
            <Chip icon="chat" onClick={() => go('chat')}>Share to chat</Chip>
            {notVoted.length > 0 && !closed && <Chip icon="notifications_active" onClick={() => say(`Nudged ${names(members, notVoted.map((m) => m.id)).join(' & ')}`)}>Nudge {names(members, notVoted.map((m) => m.id)).join(' & ')}</Chip>}
          </div>
        </div>
        <Section>Options</Section>
        <div className="stack">
          {options.map((o, i) => {
            const n = (votes[o.id] || []).length
            const lead = i === 0 && n > 0
            const pct = totalVotes ? (n / Math.max(totalVotes, members.length)) * 100 : 0
            return (
              <div key={o.id} role="button" tabIndex={0} className={`card opt ${lead ? 'lead' : ''} ${(votes[o.id] || []).includes('A') ? 'you' : ''}`} onClick={() => castVote(o.id)} onKeyDown={(e) => e.key === 'Enter' && castVote(o.id)}>
                <div className="head">
                  <Photo src={o.photo} fallback={<span className="ph" style={{ width: 56, height: 56, borderRadius: 14, background: 'var(--beige)', display: 'grid', placeItems: 'center', color: 'var(--grey)', flex: 'none' }}><Icon name="restaurant" /></span>} />
                  <div className="txt"><div className="n">{o.name}</div><div className="m">{o.pollMeta} · <a href={mapsUrl(o.name)} target="_blank" rel="noreferrer" onClick={(e) => e.stopPropagation()} style={{ color: 'var(--ink)', fontWeight: 700, textDecoration: 'none' }}>Maps</a></div></div>
                  <div><div className={`count ${n ? '' : 'zero'}`}>{n}</div>{lead && <div className="leading">LEADING</div>}</div>
                </div>
                <div className={`bar ${lead ? 'lead' : ''}`}><i style={{ width: `${pct}%` }} /></div>
                <div className="voters">{n ? names(members, votes[o.id] || []).join(', ') : 'No votes yet'}</div>
              </div>
            )
          })}
        </div>
        <Section>Group</Section>
        <div className="card row" style={{ cursor: 'default' }}>
          <AvatarStack members={members} size={26} ring="#fff" dim={notVoted.map((m) => m.id)} />
          <span className="txt meta">{totalVotes} voted{notVoted.length ? <> · <b style={{ color: 'var(--ink)' }}>{notVoted.map((m) => m.name).join(' and ')}</b> {notVoted.length > 1 ? "haven't" : "hasn't"} yet</> : ' · everyone is in'}</span>
        </div>
        <p className="caption" style={{ margin: '10px 0 0' }}>{closed ? `Closed. ${leader.name} is in tonight's plan at 19:30.` : 'Closes when everyone has voted, or when you close it.'}</p>
      </div>
      <div className="sticky">
        {closed
          ? <Pill onClick={() => go('plan')}>See tonight's plan</Pill>
          : <Pill onClick={onClose} disabled={!majority}>{majority ? `Close poll · ${leader.name.split(' ').pop()} wins` : 'Close poll · needs a majority'}</Pill>}
      </div>
    </div>
  )
}

function PollsStub({ go, onTab, say }) {
  return (
    <div className="screen">
      <StatusBar />
      <TopBar left={<span className="hi">Polls</span>} />
      <div className="scroll has-tabs">
        <h1 className="title">Nothing open<span className="sub">ask the group</span></h1>
        <div className="empty"><Icon name="how_to_vote" />Polls work for any decision. Where to eat, where to stay, what to do.</div>
        <div className="chips" style={{ justifyContent: 'center' }}>
          <Chip icon="restaurant" solid onClick={() => go('createPoll')}>Where for dinner?</Chip>
          <Chip icon="hotel" onClick={() => say('Same flow as dinner: options from the wishlist')}>Where to stay</Chip>
          <Chip icon="explore" onClick={() => say('Same flow as dinner: options from the wishlist')}>What to do</Chip>
        </div>
      </div>
      <TabBar active="Polls" onTab={onTab} />
    </div>
  )
}

/* ---------- 07 Plan updated ---------- */
function Plan({ members, go, onTab, leader, totalVotes, pollStatus, expenseLogged, onLog, say }) {
  const won = pollStatus === 'closed'
  return (
    <div className="screen">
      <StatusBar />
      <TopBar onBack={() => go('trip', true)} right={<button className="circle-btn" aria-label="Share" onClick={() => say('Shared to the group chat')}><Icon name="ios_share" /></button>} />
      <div className="scroll has-tabs">
        {won ? (
          <>
            <h1 className="title">Ramiro it is.<span className="sub">Added to tonight</span></h1>
            <div className="card winner">
              <Photo className="strip" src={leader.photo || 'img/ramiro-wide.jpg'} alt={leader.name} fallback={<div className="strip" style={{ background: 'var(--beige)' }} />} />
              <div className="h">
                <div className="txt"><div style={{ fontWeight: 700, fontSize: 15 }}>{leader.name}</div><div className="meta">Won {totalVotes} of {members.length} · 19:30 · 12 min walk</div></div>
                <img src="img/map.jpg" alt="Map" />
              </div>
              <div className="chips">
                <a className="chip" href={directionsUrl(leader.name)} target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}><Icon name="directions_walk" />Directions</a>
                <Chip icon="restaurant" onClick={() => say('Table for 6 requested')}>Book a table</Chip>
              </div>
            </div>
          </>
        ) : (
          <h1 className="title">Today<span className="sub">Sat 27 · day 4 of 4</span></h1>
        )}
        <Section>Today · Sat 27</Section>
        <div className="stack">
          <Row iconText="10:00" bg="var(--mint)" fg="var(--mint-fg)" photo="img/lisbon.jpg" title="Torre de Belém" meta="Done · 5 went" right={<span />} />
          <Row iconText="14:00" bg="var(--peach)" fg="var(--peach-fg)" photo="img/lx.jpg" title="LX Factory" meta="€86 · logged by Maya" right={<span />} />
          {won ? (
            <Row iconText="19:30" bg="var(--pink)" fg="var(--pink-fg)" photo={leader.photo} title={`Dinner · ${leader.name}`} meta={`From tonight's poll · ${members.length} going`} selected right={<span className="tag">poll</span>} />
          ) : (
            <Row iconText="19:30" bg="var(--beige)" fg="var(--grey)" title="Dinner · still open" meta="Poll the group" onClick={() => go(pollStatus === 'live' ? 'poll' : 'createPoll')} />
          )}
          <div className="suggest">
            <img src="img/miradouro.jpg" alt="" />
            <div><div className="k">AFTER DINNER · SUGGESTION</div><div className="t">Miradouro da Graça · 8 min</div><div className="s">Saved by Sam</div></div>
            <Chip onClick={() => say('Poll drafted for after dinner')}>Poll it</Chip>
          </div>
          {won && !expenseLogged && (
            <div className="panel" style={{ marginTop: 4 }}>
              <h3>Back from dinner?</h3>
              <p>Scan the receipt and TripUp splits it by item.</p>
              <Pill onClick={onLog} icon="receipt_long">Log the dinner</Pill>
            </div>
          )}
        </div>
      </div>
      <TabBar active="Plan" onTab={onTab} />
    </div>
  )
}

/* ---------- 08 Log expense ---------- */
function Expense({ members, go, wineOut, setWineOut, onSave }) {
  const wine = EXPENSE.items[1]
  const payers = members.filter((m) => !wineOut.includes(m.id))
  const each = (wine.amount / Math.max(payers.length, 1)).toFixed(0)
  const toggle = (id) => setWineOut(wineOut.includes(id) ? wineOut.filter((x) => x !== id) : [...wineOut, id])
  return (
    <div className="screen">
      <StatusBar />
      <TopBar onBack={() => go('plan', true)} label="Receipt scanned" />
      <div className="scroll has-sticky">
        <h1 className="title">Dinner at<span className="sub">Ramiro</span></h1>
        <div className="card total">
          <div><div className="k">TOTAL</div><div className="v">€{EXPENSE.total}.00</div><div className="meta">Paid by you · {members.length} people</div></div>
          <img src="img/ramiro.jpg" alt="Receipt" />
        </div>
        <Section>Split by item</Section>
        <div className="stack">
          <div className="card item">
            <div className="h"><span>Food</span><span>€166</span></div>
            <div className="s">Everyone · €{(166 / members.length).toFixed(2)} each</div>
          </div>
          <div className="card item active">
            <div className="h"><span>Wine</span><span>€48</span></div>
            <div className="s">{payers.length} people · €{each} each</div>
            <div className="people">
              {members.map((m) => {
                const out = wineOut.includes(m.id)
                return (
                  <Chip key={m.id} className="person" solid={!out} strike={out} onClick={() => toggle(m.id)}>
                    <Avatar m={m} size={22} />{m.name}
                  </Chip>
                )
              })}
            </div>
            <div className="note">{wine.note}</div>
          </div>
        </div>
      </div>
      <div className="sticky"><Pill onClick={onSave}>Save · updates {members.length} balances</Pill></div>
    </div>
  )
}

/* ---------- 09 Balances ---------- */
function Balances({ members, go, onTab, paid, onPick, say }) {
  const [why, setWhy] = useState(true)
  const unpaid = BALANCES.transfers.filter((t) => !paid[t.id])
  const toYou = unpaid.filter((t) => t.to === 'A')
  return (
    <div className="screen">
      <StatusBar />
      <TopBar onBack={() => go('trip', true)} right={<button className="circle-btn" aria-label="Share" onClick={() => say('Balances shared to the chat')}><Icon name="ios_share" /></button>} />
      <div className="scroll has-tabs">
        <h1 className="title">Trip money<span className="sub">€{BALANCES.total.toLocaleString('en')} total</span></h1>
        <div className="stats">
          <div><div className="v">€{BALANCES.perPerson}</div><div className="k">per person</div></div>
          <div><div className="v">€{BALANCES.youPaid}</div><div className="k">you paid</div></div>
          <div><div className="v pos">+€{BALANCES.youOwed}</div><div className="k">you're owed</div></div>
        </div>
        <Section>3 transfers instead of 7<button className="help" onClick={() => setWhy(!why)} aria-label="Why">?</button></Section>
        <div className="stack">
          {BALANCES.transfers.map((t) => {
            const done = paid[t.id]
            return (
              <button key={t.id} className={`card transfer ${done ? 'done' : ''}`} onClick={() => !done && onPick(t)}>
                <span className="pair"><Avatar m={byId(members, t.from) || REN} size={30} ring="#fff" /><Icon name="arrow_forward" /><Avatar m={byId(members, t.to)} size={30} ring="#fff" /></span>
                <span className="txt"><div className="t">{t.label} €{t.amount}</div>{t.why && <div className="w">{t.why}</div>}{done && <div className="paid"><Icon name="check_circle" fill style={{ fontSize: 14 }} /> Paid · {done.name}</div>}</span>
                {!done && <span className="amt">€{t.amount}</span>}
              </button>
            )
          })}
          {why && <div className="panel" style={{ padding: '12px 14px' }}><p style={{ margin: 0, textAlign: 'left', fontSize: 12 }}>{BALANCES.explainer}</p></div>}
          <div className="chips">
            {toYou.length > 0 && <Chip icon="notifications_active" onClick={() => say(`Nudged ${toYou.map((t) => byId(members, t.from)?.name).join(' & ')}`)}>Nudge {toYou.map((t) => byId(members, t.from)?.name).join(' & ')}</Chip>}
            <Chip onClick={() => unpaid[0] && onPick(unpaid[0])}>Paid in cash?</Chip>
          </div>
          <p className="caption">Friends pay you with Apple Pay, Revolut or a bank transfer. Nothing to top up.</p>
        </div>
      </div>
      <TabBar active="Money" onTab={onTab} />
    </div>
  )
}

function SettleSheet({ t, members, onClose, onPick }) {
  const from = byId(members, t.from) || REN
  const to = byId(members, t.to)
  return (
    <Sheet onClose={onClose}>
      <h1 className="title sm" style={{ margin: '6px 0 4px' }}>{from.name} pays {t.to === 'A' ? 'you' : to.name}<span className="sub">€{t.amount}</span></h1>
      <p className="meta" style={{ margin: '0 0 14px' }}>Pick how it was paid. TripUp never holds the money.</p>
      <div className="stack">
        {RAILS.map((r) => (
          <button key={r.id} className="card row" onClick={() => onPick(r)}>
            <RailLogo id={r.id} />
            <span className="txt"><span className="t" style={{ display: 'block' }}>{r.name}</span><span className="m" style={{ display: 'block' }}>{r.meta}</span></span>
            <span className="arrow"><Icon name="arrow_forward" /></span>
          </button>
        ))}
      </div>
    </Sheet>
  )
}

/* ---------- 10 Settled ---------- */
function Settled({ members, paid, onNext }) {
  const received = BALANCES.transfers.filter((t) => t.to === 'A')
  return (
    <div className="screen">
      <StatusBar />
      <TopBar left={<span />} right={<button className="circle-btn" aria-label="Close" onClick={onNext}><Icon name="close" /></button>} />
      <div className="scroll has-sticky">
        <div className="settled-card">
          <img src="img/lisbon.jpg" alt="Lisbon" />
          <h1 className="title">Lisbon is<span className="sub">squared up.</span></h1>
          <div className="meta">{members.length} of {members.length} settled · €{BALANCES.total.toLocaleString('en')} across 4 days</div>
          <div className="avs"><AvatarStack members={members} size={26} ring="var(--beige)" /></div>
        </div>
        <Section>Received</Section>
        <div className="stack">
          {received.map((t, i) => (
            <div key={t.id} className="card transfer done" style={{ opacity: 1 }}>
              <Avatar m={byId(members, t.from)} size={46} ring="#fff" />
              <span className="txt"><div className="t">€{t.amount} from {byId(members, t.from).name}</div><div className="w" style={{ display: 'flex', alignItems: 'center', gap: 6 }}><RailLogo id={paid[t.id]?.id || 'applepay'} size={18} />{paid[t.id]?.name || 'Apple Pay'} · {i === 0 ? 'just now' : '2 min ago'}</div></span>
              <span className="paid"><Icon name="check_circle" fill style={{ fontSize: 16 }} /> Paid</span>
            </div>
          ))}
          <Row icon="chat" bg="var(--mint)" fg="var(--mint-fg)" title="Posted to the group chat" meta="“All settled, ready for the next one”" right={<span />} />
        </div>
      </div>
      <div className="sticky"><Pill onClick={onNext}>Plan the next trip</Pill></div>
    </div>
  )
}


/* ---------- Notifications sheet ---------- */
function Notifications({ members, pollStatus, expenseLogged, onClose, go }) {
  const items = []
  if (expenseLogged) items.push(['receipt_long', 'var(--peri)', 'var(--peri-fg)', 'Dinner at Ramiro logged', `€214 split ${members.length} ways · just now`, 'balances'])
  if (pollStatus === 'closed') items.push(['calendar_month', 'var(--pink)', 'var(--pink-fg)', 'Ramiro is in tonight\'s plan', '19:30 · from the poll', 'plan'])
  if (pollStatus === 'live') items.push(['how_to_vote', 'var(--peach)', 'var(--peach-fg)', 'Where for dinner? is live', `${members.length} people asked · vote now`, 'poll'])
  if (members.some((m) => m.id === 'R')) items.push(['person_add', 'var(--mint)', 'var(--mint-fg)', 'Ren joined Lisbon', 'via your link · dinner tonight only', 'trip'])
  items.push(['euro', 'var(--peri)', 'var(--peri-fg)', 'Maya logged LX Factory', '€86 · you owe €14.33 · 14:20', 'balances'])
  items.push(['photo_camera', 'var(--beige)', 'var(--ink)', 'Sam added 12 photos', 'Torre de Belém · 11:40', 'plan'])
  return (
    <Sheet onClose={onClose}>
      <h1 className="title sm" style={{ margin: '6px 0 14px' }}>Notifications<span className="sub">today</span></h1>
      <div className="stack">
        {items.map(([ic, bg, fg, t, m, dest]) => <Row key={t} icon={ic} bg={bg} fg={fg} title={t} meta={m} onClick={() => go(dest)} />)}
      </div>
    </Sheet>
  )
}

/* ---------- New trip sheet ---------- */
function NewTrip({ onClose, say }) {
  return (
    <Sheet onClose={onClose}>
      <h1 className="title sm" style={{ margin: '6px 0 14px' }}>New trip<span className="sub">where and when</span></h1>
      <div className="stack">
        <div className="field"><Icon name="location_on" style={{ color: 'var(--grey)' }} /><span style={{ flex: 1, color: 'var(--grey)' }}>City</span></div>
        <div className="field"><Icon name="calendar_month" style={{ color: 'var(--grey)' }} /><span style={{ flex: 1, color: 'var(--grey)' }}>Dates</span></div>
        <div className="field"><Icon name="hotel" style={{ color: 'var(--grey)' }} /><span style={{ flex: 1, color: 'var(--grey)' }}>Stay (optional)</span></div>
        <p className="caption" style={{ margin: 0 }}>Creating the trip makes you the organizer. Anyone can still add anything.</p>
        <Pill onClick={() => { onClose(); say('Trip creation is mocked in this demo') }}>Create and invite</Pill>
      </div>
    </Sheet>
  )
}
