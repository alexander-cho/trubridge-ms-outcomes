import './App.css';

async function getData() {
  const BASE_URL = "/api";
  const response = await fetch(BASE_URL);
  const result = await response.json();
  console.log(result);
}

function App() {

  return (
    <>
      <div className="card">
        <button onClick={getData}>
          Get Data from "/"
        </button>
      </div>
    </>
  );
}

export default App;
