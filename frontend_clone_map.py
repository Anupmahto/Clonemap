# Install dependencies: `npm install react-map-gl axios`

import React, { useState } from "react";
import Map, { Marker, Source, Layer } from "react-map-gl";
import axios from "axios";

const MAPBOX_TOKEN = "your_mapbox_access_token"; // Replace with your Mapbox token

const App = () => {
  const [viewport, setViewport] = useState({
    latitude: 12.9716,
    longitude: 77.5946,
    zoom: 12,
  });
  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);
  const [path, setPath] = useState(null);

  const handleMapClick = (event) => {
    const [lng, lat] = event.lngLat;
    if (!origin) {
      setOrigin({ lat, lng });
    } else if (!destination) {
      setDestination({ lat, lng });
    }
  };

  const computePath = async () => {
    if (origin && destination) {
      try {
        const response = await axios.post("http://localhost:5000/shortest-path", {
          origin,
          destination,
        });
        setPath(response.data.path);
      } catch (error) {
        console.error("Error fetching path:", error);
      }
    }
  };

  const pathLayer = {
    id: "path",
    type: "line",
    paint: {
      "line-color": "#FF0000",
      "line-width": 4,
    },
  };

  return (
    <div>
      <h1>Google Maps Clone - Bengaluru</h1>
      <Map
        initialViewState={viewport}
        style={{ width: "100%", height: "500px" }}
        mapStyle="mapbox://styles/mapbox/streets-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
        onClick={handleMapClick}
      >
        {origin && (
          <Marker latitude={origin.lat} longitude={origin.lng} color="green" />
        )}
        {destination && (
          <Marker latitude={destination.lat} longitude={destination.lng} color="red" />
        )}
        {path && (
          <Source type="geojson" data={{
            type: "Feature",
            geometry: {
              type: "LineString",
              coordinates: path.map((coord) => [coord[1], coord[0]]),
            },
          }}>
            <Layer {...pathLayer} />
          </Source>
        )}
      </Map>
      <button onClick={computePath} disabled={!origin || !destination}>
        Compute Shortest Path
      </button>
    </div>
  );
};

export default App;
