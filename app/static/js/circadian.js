// circadian.js — Rose Pine Moon × Phosphor Noir
// Four named themes. No noise. Updates every 60s.

const PHASES = {
  rose: {
    range:      [21, 30],  // 21–06 (hours <6 get +24)
    bg:         '#1a1826',
    surface:    '#232136',
    overlay:    '#2a273f',
    accent:     '#ea9a97',
    accentDark: '#c47a77',
    accentRgb:  '234,154,151',
    muted:      '#6e6a86',
    label:      'nyx',
  },
  ocean: {
    range:      [6, 11],
    bg:         '#090f1a',
    surface:    '#0f1926',
    overlay:    '#162233',
    accent:     '#5ec8ed',
    accentDark: '#3aa8cc',
    accentRgb:  '94,200,237',
    muted:      '#3d6a80',
    label:      'choice',
  },
  gold: {
    range:      [11, 17],
    bg:         '#1f1d2e',
    surface:    '#26233a',
    overlay:    '#312e4a',
    accent:     '#f6c177',
    accentDark: '#d4a356',
    accentRgb:  '246,193,119',
    muted:      '#908caa',
    label:      'desire',
  },
  iris: {
    range:      [17, 21],
    bg:         '#191724',
    surface:    '#1f1d2e',
    overlay:    '#26233a',
    accent:     '#c4a7e7',
    accentDark: '#9c7dc7',
    accentRgb:  '196,167,231',
    muted:      '#6e6a86',
    label:      'still-pine',
  },
}

function getPhase(h) {
  const hour = h < 6 ? h + 24 : h
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

  // phase-dot is deliberately NOT set here anymore — it's a fixed mercury-silver
  // color (--mercury-dot in style.css) so it always reads distinct from the
  // phase-tinted ☿⚕ glyphs on either side of it, not another phase indicator.
  const label = document.getElementById('phase-label')
  if (label) {
    label.textContent = phase.label
    label.style.color = phase.accent
    label.style.textShadow = `0 0 9px rgba(${phase.accentRgb}, 0.45)`
  }
}

function tick() {
  apply(getPhase(new Date().getHours()))
}

tick()
setInterval(tick, 60000)
