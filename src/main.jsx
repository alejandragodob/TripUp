import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './styles.css'

// Material Symbols renders ligature names as plain text until the font arrives.
// Keep icons invisible until it loads (or 3 s pass), so nothing flashes "arrow_forward".
const ready = () => document.documentElement.classList.add('icons-ready')
if (document.fonts?.load) {
  Promise.race([
    document.fonts.load('20px "Material Symbols Rounded"'),
    new Promise((r) => setTimeout(r, 3000)),
  ]).then(ready, ready)
} else ready()

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
