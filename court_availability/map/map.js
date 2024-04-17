mapboxgl.accessToken = window.MAPBOXGL_ACCESS_TOKEN;

const retrieveData = async () => {
  const data = await fetch("http://localhost:5000/", {
    headers: { Accept: "application/json" },
  }).then(async (res) => {
    const data = await res.json();

    return data;
  });

  const date = data.date;
  const found_locations = data.found_locations;

  const map = new mapboxgl.Map({
    container: "map",
    center: [103.8185, 1.4491],
    zoom: 12,
    style: "mapbox://styles/mapbox/navigation-night-v1",
  });

  found_locations.forEach(({ id, lat, lng, label }) => {
    const marker = new mapboxgl.Marker({ color: "maroon" })
      .setLngLat([lng, lat])
      .addTo(map);

    marker.getElement().addEventListener("click", () => {
      const url = `https://www.onepa.gov.sg/facilities/availability?facilityId=${id}_BADMINTONCOURTS&date=${date}&time=all`;

      window.open(url, "_blank").focus();
    });

    const popup = new mapboxgl.Popup({
      offset: 25,
      closeButton: false,
    }).setText(label);

    marker.getElement().addEventListener("mouseover", () => {
      marker.getElement().style.cursor = "pointer";

      popup.setLngLat([lng, lat]).addTo(map);
    });

    marker.getElement().addEventListener("mouseleave", () => {
      popup.remove();
    });
  });
};

retrieveData();
