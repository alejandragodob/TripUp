// Mock data for the Lisbon scenario. Everything the prototype shows comes from here.

export const MEMBERS = [
  { id: 'A', name: 'Ari', initial: 'A', color: '#FFB48A', you: true },
  { id: 'N', name: 'Nic', initial: 'N', color: '#FFD9A8', organizer: true },
  { id: 'M', name: 'Maya', initial: 'M', color: '#BFE6D2' },
  { id: 'T', name: 'Theo', initial: 'T', color: '#C9D8FF' },
  { id: 'S', name: 'Sam', initial: 'S', color: '#F9C4DF' },
]

export const REN = { id: 'R', name: 'Ren', initial: 'R', color: '#E8DDF5', joinedFor: 'tonight' }

export const TRIP = {
  city: 'Lisbon',
  dates: 'Sep 24 – 28',
  day: 4,
  days: 4,
  photo: 'img/group.jpg',
}

export const OTHER_TRIPS = [
  { id: 'primavera', tag: 'Festival', title: 'Primavera Sound, Barcelona', meta: 'Jun 3 – 6, 2027 · 8 friends', icon: 'festival', bg: '#E3E9FF', fg: '#3452A3' },
  { id: 'dolomites', tag: 'Past · settled', title: 'Dolomites hut-to-hut', meta: 'Aug 2026 · 4 friends · €2,140', icon: 'hiking', bg: '#DDEFE4', fg: '#276A4D' },
]

export const ITINERARY = [
  { id: 'belem', time: '10:00', label: 'Sightseeing', title: 'Torre de Belém', meta: 'Done · 5 went', bg: '#DDEFE4', fg: '#276A4D' },
  { id: 'lx', time: '14:00', label: 'Lunch', title: 'LX Factory', meta: '€86 · logged by Maya', bg: '#FFE2C9', fg: '#A63C18' },
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
  { id: 'applepay', name: 'Apple Pay', meta: 'Instant', icon: 'contactless' },
  { id: 'revolut', name: 'Revolut · Wise', meta: 'Opens the app', icon: 'currency_exchange' },
  { id: 'bank', name: 'Bank transfer', meta: 'IBAN copied', icon: 'account_balance' },
  { id: 'cash', name: 'Paid in cash', meta: 'Mark as settled', icon: 'payments' },
]
