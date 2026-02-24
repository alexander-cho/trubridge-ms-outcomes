import './App.css';

async function getData() {
  const url = "/api";
  const response = await fetch(url);
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
