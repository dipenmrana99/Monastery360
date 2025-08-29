function initMap(elId, dataUrl, opts={}){
  const el = document.getElementById(elId);
  if(!el){ return; }
  const center = opts.center || [27.533, 88.512]; // Sikkim approx
  const zoom = opts.zoom || 8;
  const map = L.map(elId).setView(center, zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
  }).addTo(map);

  fetch(dataUrl).then(r=>r.json()).then(points=>{
    points.forEach(m => {
      const marker = L.marker([m.lat, m.lng]).addTo(map);
      const svBtn = m.street_view_url ? `<a class="btn" target="_blank" href="${m.street_view_url}">Street View</a>` : '';
      const popup = `
        <div style="min-width:220px">
          <strong>${m.name}</strong><br/>
          <span style="color:#9ca3af">${m.district}</span><br/>
          <div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap">
            <a class="btn" href="/monastery/${m.id}">Open Page</a>
            ${svBtn}
          </div>
        </div>`;
      marker.bindPopup(popup);
    });
  });
}
