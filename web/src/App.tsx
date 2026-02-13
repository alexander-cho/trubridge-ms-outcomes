import './App.css';

async function getData() {
  const url = "http://localhost:8000";
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
