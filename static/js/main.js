// basic UX helpers
console.log("Monastery360 loaded");

let currentSlide = 0;
const slides = document.querySelectorAll(".slider img");

function showSlide(index) {
  slides.forEach((s, i) => {
    s.classList.remove("active");
    if (i === index) s.classList.add("active");
  });
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

if (slides.length > 0) {
  showSlide(currentSlide);
  setInterval(nextSlide, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
  const ticker = document.getElementById("eventTicker");

  fetch("/static/js/events.json")   // <-- make sure file is inside static/data/
    .then(res => res.json())
    .then(events => {
      if (!events || events.length === 0) {
        ticker.textContent = "No upcoming events.";
        return;
      }

      // Turn each event into a text line
      const text = events.map(e => {
        // Format date (YYYY-MM-DD → 17 Feb 2026)
        const date = new Date(e.date);
        const dateStr = date.toLocaleDateString("en-IN", {
          year: "numeric", month: "short", day: "numeric"
        });

        return `${dateStr} · ${e.title} @ ${e.location} — ${e.description}`;
      }).join("   |   ");

      ticker.textContent = text;
    })
    .catch(err => {
      ticker.textContent = "Error loading events.";
      console.error("Ticker fetch error:", err);
    });
});



