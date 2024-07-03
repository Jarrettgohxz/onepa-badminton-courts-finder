mapboxgl.accessToken = window.MAPBOXGL_ACCESS_TOKEN;

const map = new mapboxgl.Map({
  container: "map",
  center: [103.8185, 1.4491],
  zoom: 12,
  style: "mapbox://styles/mapbox/navigation-night-v1",
});

const marker = new mapboxgl.Marker().setLngLat([103.8185, 1.4491]).addTo(map);
