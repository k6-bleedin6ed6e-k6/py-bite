// circadian.js — Rose Pine Moon × Phosphor Noir
// Four named themes. No noise. Updates every 60s.

const PHASES = {
  rose: {
    range:      [5, 11],
    bg:         '#1a1826',
    surface:    '#232136',
    overlay:    '#2a273f',
    accent:     '#ea9a97',
    accentDark: '#c47a77',
    accentRgb:  '234,154,151',
    muted:      '#6e6a86',
    label:      'rose-pine-rose',
  },
  ocean: {
    range:      [11, 17],
    bg:         '#090f1a',
    surface:    '#0f1926',
    overlay:    '#162233',
    accent:     '#5ec8ed',
    accentDark: '#3aa8cc',
    accentRgb:  '94,200,237',
    muted:      '#3d6a80',
    label:      'midnight-ocean',
  },
  gold: {
    range:      [17, 21],
    bg:         '#1f1d2e',
    surface:    '#26233a',
    overlay:    '#312e4a',
    accent:     '#f6c177',
    accentDark: '#d4a356',
    accentRgb:  '246,193,119',
    muted:      '#908caa',
    label:      'rose-pine-gold',
  },
  iris: {
    range:      [21, 29],  // 21–04 (hours <5 get +24)
    bg:         '#191724',
    surface:    '#1f1d2e',
    overlay:    '#26233a',
    accent:     '#c4a7e7',
    accentDark: '#9c7dc7',
    accentRgb:  '196,167,231',
    muted:      '#6e6a86',
    label:      'rose-pine-iris',
  },
}

function getPhase(h) {
  const hour = h < 5 ? h + 24 : h
  for (const [name, p] of Object.entries(PHASES)) {
    if (hour >= p.range[0] && hour < p.range[1]) return { name, ...p }
  }
  return { name: 'iris', ...PHASES.iris }
}

function apply(phase) {
  const r = document.documentElement
  r.style.setProperty('--bg',           phase.bg)
  r.style.setProperty('--surface',      phase.surface)
  r.style.setProperty('--surface-light', phase.overlay)
  r.style.setProperty('--accent',       phase.accent)
  r.style.setProperty('--accent-dark',  phase.accentDark)
  r.style.setProperty('--accent-rgb',   phase.accentRgb)
  r.style.setProperty('--accent-glow',  `rgba(${phase.accentRgb}, 0.14)`)
  r.style.setProperty('--text-muted',   phase.muted)
  r.dataset.phase = phase.name

  const dot   = document.getElementById('phase-dot')
  const label = document.getElementById('phase-label')
  if (dot) {
    dot.style.background = phase.accent
    dot.style.boxShadow  = `0 0 7px rgba(${phase.accentRgb}, 0.7)`
  }
  if (label) label.textContent = phase.label
}

function tick() {
  apply(getPhase(new Date().getHours()))
}

tick()
setInterval(tick, 60000)
