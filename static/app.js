const calculators = [
  { id:"newton2", topic:"Forces", title:"Newton’s Second Law", formula:"F = ma", note:"Enter any two values and leave one blank.", fields:[["F","Net force (F)","N"],["m","Mass (m)","kg"],["a","Acceleration (a)","m/s²"]] },
  { id:"newton3", topic:"Forces", title:"Newton’s Third Law", formula:"F₂ = −F₁", note:"Enter one force. The reaction is equal and opposite.", fields:[["F1","Action force (F₁)","N"],["F2","Reaction force (F₂)","N"]] },
  { id:"momentum", topic:"Momentum", title:"Linear Momentum", formula:"p = mv", note:"Enter any two values and leave one blank.", fields:[["p","Momentum (p)","kg·m/s"],["m","Mass (m)","kg"],["v","Velocity (v)","m/s"]] },
  { id:"impulse", topic:"Momentum", title:"Impulse", formula:"J = FΔt", note:"Enter any two values and leave one blank.", fields:[["J","Impulse (J)","N·s"],["F","Average force (F)","N"],["t","Time interval (Δt)","s"]] },
  { id:"collision", topic:"Momentum", title:"Conservation of Momentum", formula:"m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂", note:"Enter both masses and three velocities. Leave one velocity blank.", fields:[["m1","Mass 1 (m₁)","kg"],["u1","Initial velocity 1 (u₁)","m/s"],["v1","Final velocity 1 (v₁)","m/s"],["m2","Mass 2 (m₂)","kg"],["u2","Initial velocity 2 (u₂)","m/s"],["v2","Final velocity 2 (v₂)","m/s"]] },
  { id:"projectile", topic:"Projectile", title:"Angled Projectile", formula:"T = 2u sinθ/g • R = u² sin2θ/g", note:"Enter speed and angle. Gravity defaults to 9.81 m/s².", fields:[["u","Launch speed (u)","m/s"],["theta","Launch angle (θ)","°"],["g","Gravity (g)","m/s²","9.81"]] },
  { id:"horizontal", topic:"Projectile", title:"Horizontal Launch", formula:"t = √(2h/g) • R = ut", note:"Enter horizontal speed and height. Gravity defaults to 9.81 m/s².", fields:[["u","Horizontal speed (u)","m/s"],["h","Height (h)","m"],["g","Gravity (g)","m/s²","9.81"]] },
  { id:"work", topic:"Energy", title:"Work Done", formula:"W = Fd cosθ", note:"Enter known values. Angle defaults to 0°.", fields:[["W","Work (W)","J"],["F","Force (F)","N"],["d","Displacement (d)","m"],["theta","Angle (θ)","°","0"]] },
  { id:"kinetic", topic:"Energy", title:"Kinetic Energy", formula:"Eₖ = ½mv²", note:"Enter any two values and leave one blank.", fields:[["E","Kinetic energy (Eₖ)","J"],["m","Mass (m)","kg"],["v","Speed (v)","m/s"]] },
  { id:"potential", topic:"Energy", title:"Gravitational Potential Energy", formula:"Eₚ = mgh", note:"Leave one unknown blank. Gravity defaults to 9.81 m/s².", fields:[["E","Potential energy (Eₚ)","J"],["m","Mass (m)","kg"],["g","Gravity (g)","m/s²","9.81"],["h","Height (h)","m"]] },
];

const topics = ["All", "Forces", "Momentum", "Projectile", "Energy"];
let activeTopic = "All";
const grid = document.querySelector("#calculator-grid");
const tabs = document.querySelector(".tabs");
const themeToggle = document.querySelector("#theme-toggle");
const themeIcon = themeToggle.querySelector(".theme-icon");
const themeText = themeToggle.querySelector(".theme-text");
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

function savedTheme() {
  try {
    return localStorage.getItem("dinglo-theme");
  } catch {
    return null;
  }
}

function applyTheme(theme, save = false) {
  const dark = theme === "dark";
  document.documentElement.dataset.theme = dark ? "dark" : "light";
  themeToggle.setAttribute("aria-pressed", String(dark));
  themeToggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
  themeIcon.textContent = dark ? "☀" : "☾";
  themeText.textContent = dark ? "Light" : "Dark";

  if (save) {
    try {
      localStorage.setItem("dinglo-theme", dark ? "dark" : "light");
    } catch {
      // The selected theme still works when storage is unavailable.
    }
  }
}

applyTheme(document.documentElement.dataset.theme || (systemTheme.matches ? "dark" : "light"));

themeToggle.addEventListener("click", () => {
  const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(nextTheme, true);
});

systemTheme.addEventListener("change", event => {
  if (!savedTheme()) {
    applyTheme(event.matches ? "dark" : "light");
  }
});

function renderTabs() {
  tabs.innerHTML = topics.map(topic => `<button type="button" class="${topic === activeTopic ? "active" : ""}" data-topic="${topic}">${topic}</button>`).join("");
  tabs.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    activeTopic = button.dataset.topic;
    renderTabs();
    renderCards();
  }));
}

function cardTemplate(calc) {
  const fields = calc.fields.map(([key,label,unit,placeholder]) => `
    <label>
      <span>${label}</span>
      <div class="input-wrap">
        <input type="number" inputmode="decimal" step="any" name="${key}" placeholder="${placeholder || "Leave blank if unknown"}" aria-label="${label} in ${unit}">
        <b>${unit}</b>
      </div>
    </label>`).join("");
  return `<article class="calculator-card" data-id="${calc.id}">
    <small>${calc.topic}</small><h3>${calc.title}</h3><div class="formula-label">${calc.formula}</div><p>${calc.note}</p>
    <form><div class="fields">${fields}</div><div class="actions"><button class="solve" type="submit">Solve question</button><button class="clear" type="button">Clear</button></div></form>
    <div class="message" hidden></div>
  </article>`;
}

function renderCards() {
  grid.innerHTML = calculators.filter(calc => activeTopic === "All" || calc.topic === activeTopic).map(cardTemplate).join("");
  grid.querySelectorAll(".calculator-card").forEach(card => {
    const form = card.querySelector("form");
    const message = card.querySelector(".message");
    form.addEventListener("submit", async event => {
      event.preventDefault();
      message.hidden = true;
      const values = Object.fromEntries(new FormData(form));
      const response = await fetch("/api/solve", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({calculator:card.dataset.id, values}),
      });
      const result = await response.json();
      message.hidden = false;
      if (!response.ok) {
        message.className = "message error";
        message.textContent = result.error;
        return;
      }
      message.className = "message solution";
      message.innerHTML = `<small>Dinglo solution</small><h4>${result.answer}</h4><ol>${result.steps.map(step => `<li>${step}</li>`).join("")}</ol>`;
    });
    card.querySelector(".clear").addEventListener("click", () => {
      form.reset();
      message.hidden = true;
    });
  });
}

renderTabs();
renderCards();
