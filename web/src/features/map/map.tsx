import React from "react";
import { useEffect, useState } from "react";

interface Tract {
  geoid: string;
  namelsad: string;
  intptlat: string;
  intptlon: string;
  // geom: Record<any, any>
}

const TractInfo = ({ geoid, namelsad, intptlat, intptlon }: Tract) => (
  <div>
    <p>{geoid}</p>
    <p>{namelsad}</p>
    <p>{intptlat}</p>
    <p>{intptlon}</p>
    {/*<p>{geom}</p>*/}
  </div>
);

async function getTracts(): Promise<Tract[]> {
  const BASE_URL = "/api";
  const MAP_URL = BASE_URL + "/tracts?state_fp=28&tolerance=0.01"
  const response = await fetch(MAP_URL);
  return await response.json();
}

export default function Map() {
  const [tractData, setTractData] = useState<Tract[]>([]);

  useEffect(() => {
    getTracts().then(result => {
      setTractData(result);
    });
  }, []);

  return (
    <>
      <div className="card">
        {tractData.map((tract) => {
          return (
            <React.Fragment key={tract.geoid}>
              <TractInfo
                {...tract}
              />
              <br/>
            </React.Fragment>
          );
        })}
      </div>
    </>
  );
}