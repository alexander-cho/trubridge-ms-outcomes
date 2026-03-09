import Map
  // , { Source }
  from 'react-map-gl/maplibre';
import { useState, useEffect } from "react";
import 'maplibre-gl/dist/maplibre-gl.css';


interface Tract {
  geoid: string;
  namelsad: string;
  intptlat: string;
  intptlon: string;
  geom: string;
}

async function getTracts(): Promise<Tract[]> {
  const BASE_URL = "/api";
  const MAP_URL = BASE_URL + "/tracts?state_fp=28&tolerance=0.01"
  const response = await fetch(MAP_URL);
  return await response.json();
}

export default function MapComponent() {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [tractData, setTractData] = useState<Tract[]>([]);
  const [tractDataIsLoaded, setTractDataIsLoaded] = useState<boolean>(false);

  useEffect(() => {
    getTracts().then(result => {
      setTractData(result);
      setIsLoading(false);
      setTractDataIsLoaded(true);
      console.log("Calling api...");
      console.log(tractData);
    });
  }, []);

  return (
    <>
      {isLoading || !tractDataIsLoaded ?
        <h1>Loading...</h1>
        :
        <Map
          initialViewState={{
            longitude: -89.5,
            latitude: 32.7,
            zoom: 5.5
          }}
          style={{ width: 600, height: 400 }}
          mapStyle="https://tiles.openfreemap.org/styles/liberty"
        >
          {/*<Source type="geojson" data={tractData[0].geom.toString()}/>*/}
        </Map>
      }
    </>
  );
}