// Mock data for the Lisbon scenario. Everything the prototype shows comes from here.

export const MEMBERS = [
  { id: 'A', name: 'Ari', initial: 'A', color: '#FFB48A', you: true, photo: 'img/avatars/ari.jpg' },
  { id: 'N', name: 'Nic', initial: 'N', color: '#FFD9A8', organizer: true, photo: 'img/avatars/nic.jpg' },
  { id: 'M', name: 'Maya', initial: 'M', color: '#BFE6D2', photo: 'img/avatars/maya.jpg' },
  { id: 'T', name: 'Theo', initial: 'T', color: '#C9D8FF', photo: 'img/avatars/theo.jpg' },
  { id: 'S', name: 'Sam', initial: 'S', color: '#F9C4DF', photo: 'img/avatars/sam.jpg' },
]

export const REN = { id: 'R', name: 'Ren', initial: 'R', color: '#E8DDF5', joinedFor: 'tonight', photo: 'img/avatars/ren.jpg' }

export const TRIP = {
  city: 'Lisbon',
  dates: 'Sep 24 – 28',
  day: 4,
  days: 4,
  photo: 'img/lisbon-bridge.jpg',
  hero: 'img/lisbon-bridge.jpg',
  group: 'img/group.jpg',
}

export const OTHER_TRIPS = [
  { id: 'primavera', tag: 'Festival', title: 'Primavera Sound, Barcelona', meta: 'Jun 3 – 6, 2027 · 8 friends', icon: 'festival', bg: '#E3E9FF', fg: '#3452A3', photo: 'img/events/primavera.jpg' },
  { id: 'newyork', tag: 'Past · settled', title: 'New York, Christmas markets', meta: 'Dec 2025 · 4 friends · €2,140', icon: 'storefront', bg: '#DDEFE4', fg: '#276A4D', photo: 'img/events/newyork.jpg' },
]

export const ITINERARY = [
  { id: 'belem', time: '10:00', label: 'Sightseeing', title: 'Torre de Belém', meta: 'Done · 5 went', bg: '#DDEFE4', fg: '#276A4D', photo: 'img/lisbon.jpg' },
  { id: 'lx', time: '14:00', label: 'Lunch', title: 'LX Factory', meta: '€86 · logged by Maya', bg: '#FFE2C9', fg: '#A63C18', photo: 'img/lx.jpg' },
]

export const OPTIONS = [
  {
    id: 'ramiro',
    name: 'Cervejaria Ramiro',
    meta: 'Seafood · €€ · 12 min walk · open till 00:30',
    short: 'Seafood · €€ · 12 min',
    pollMeta: 'Seafood · €€ · 12 min · open late',
    source: 'Saved by Maya & Theo',
    photo: 'img/ramiro.jpg',
    votes: ['A', 'N', 'S'],
  },
  {
    id: 'taberna',
    name: 'Taberna da Rua das Flores',
    meta: 'Petiscos · €€ · 6 min walk · no bookings',
    short: 'Petiscos · €€ · 6 min',
    pollMeta: 'Petiscos · €€ · 6 min · no bookings',
    source: 'Saved by Nic',
    photo: 'img/taberna.jpg',
    votes: ['M'],
  },
  {
    id: 'timeout',
    name: 'Time Out Market',
    meta: 'Food hall · € · 15 min · something for everyone',
    short: 'Food hall · € · 15 min',
    pollMeta: 'Food hall · € · 15 min',
    source: 'Pasted in chat by Sam',
    photo: 'img/timeout.jpg',
    votes: [],
  },
]

export const EXPENSE = {
  title: 'Dinner at Ramiro',
  total: 214,
  items: [
    { id: 'food', label: 'Food', amount: 166, everyone: true },
    { id: 'wine', label: 'Wine', amount: 48, excluded: ['N', 'R'], note: 'Nic and Ren usually skip wine, so they are left out. Tap a name to change.' },
  ],
}

export const BALANCES = {
  total: 1284,
  perPerson: 214,
  youPaid: 402,
  youOwed: 188,
  transfers: [
    { id: 't1', from: 'N', to: 'A', amount: 96, label: 'Nic pays you' },
    { id: 't2', from: 'T', to: 'A', amount: 92, label: 'Theo pays you' },
    { id: 't3', from: 'R', to: 'M', amount: 28, label: 'Ren pays Maya', why: 'Instead of paying you, one transfer fewer' },
  ],
  explainer: 'Ren owes you €28 and you owe Maya €28, so Ren pays Maya directly. Nobody pays more than they owe.',
}

export const RAILS = [
  { id: 'applepay', name: 'Apple Pay', meta: 'Instant, no fees' },
  { id: 'revolut', name: 'Revolut', meta: 'Opens the Revolut app' },
  { id: 'wise', name: 'Wise', meta: 'Opens the Wise app' },
  { id: 'bank', name: 'Bank transfer', meta: 'IBAN copied to clipboard', icon: 'account_balance' },
  { id: 'cash', name: 'Paid in cash', meta: 'Mark as settled', icon: 'payments' },
]

// Places the group could pull into a poll. `saved` = who has it in their Google Maps lists.
export const PLACES = [
  { id: 'ramiro', name: 'Cervejaria Ramiro', meta: 'Seafood · €€ · 12 min walk · open till 00:30', short: 'Seafood · €€ · 12 min', pollMeta: 'Seafood · €€ · 12 min · open late', source: 'Saved by Maya & Theo', photo: 'img/ramiro.jpg', saved: ['M', 'T'], walk: 12, open: true },
  { id: 'taberna', name: 'Taberna da Rua das Flores', meta: 'Petiscos · €€ · 6 min walk · no bookings', short: 'Petiscos · €€ · 6 min', pollMeta: 'Petiscos · €€ · 6 min · no bookings', source: 'Saved by Nic', photo: 'img/taberna.jpg', saved: ['N'], walk: 6, open: true },
  { id: 'timeout', name: 'Time Out Market', meta: 'Food hall · € · 15 min · something for everyone', short: 'Food hall · € · 15 min', pollMeta: 'Food hall · € · 15 min', source: 'Pasted in chat by Sam', photo: 'img/timeout.jpg', saved: ['S'], walk: 15, open: true },
  { id: 'prado', name: 'Prado', meta: 'Modern Portuguese · €€€ · 9 min walk · book ahead', short: 'Portuguese · €€€ · 9 min', pollMeta: 'Portuguese · €€€ · 9 min · book ahead', source: 'Saved by Maya', saved: ['M'], walk: 9, open: true },
  { id: 'cevicheria', name: 'A Cevicheria', meta: 'Peruvian · €€ · 18 min walk · queue likely', short: 'Peruvian · €€ · 18 min', pollMeta: 'Peruvian · €€ · 18 min · queue likely', source: 'Saved by Theo', saved: ['T'], walk: 18, open: true },
  { id: 'zedamouraria', name: 'Zé da Mouraria', meta: 'Tasca · € · 10 min walk · lunch only', short: 'Tasca · € · 10 min', pollMeta: 'Tasca · € · 10 min · closed tonight', source: 'Saved by Nic & Sam', saved: ['N', 'S'], walk: 10, open: false },
  { id: 'pontofinal', name: 'Ponto Final', meta: 'Riverside · €€ · ferry + 20 min · sunset views', short: 'Riverside · €€ · 35 min', pollMeta: 'Riverside · €€ · ferry · sunset', source: 'Saved by Ari', saved: ['A'], walk: 35, open: true },
  { id: 'belcanto', name: 'Belcanto', meta: 'Tasting menu · €€€€ · 7 min walk', short: 'Tasting menu · €€€€ · 7 min', pollMeta: 'Tasting menu · €€€€ · 7 min', source: 'Google Maps', saved: [], walk: 7, open: true },
  { id: 'solar', name: 'Solar dos Presuntos', meta: 'Classic Portuguese · €€€ · 14 min walk', short: 'Portuguese · €€€ · 14 min', pollMeta: 'Portuguese · €€€ · 14 min', source: 'Google Maps', saved: [], walk: 14, open: true },
  { id: 'ochurrasco', name: 'O Churrasco', meta: 'Grill · €€ · 11 min walk', short: 'Grill · €€ · 11 min', pollMeta: 'Grill · €€ · 11 min', source: 'Google Maps', saved: [], walk: 11, open: true },
]

export const mapsUrl = (name) => 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(name + ', Lisboa')
export const directionsUrl = (name) => 'https://www.google.com/maps/dir/?api=1&destination=' + encodeURIComponent(name + ', Lisboa') + '&travelmode=walking'

// The default poll options are the first three wishlist places; give them the same fields (saved, walk, open).
for (const o of OPTIONS) Object.assign(o, PLACES.find((p) => p.id === o.id) || {}, { votes: o.votes })
