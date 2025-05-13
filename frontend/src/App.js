import logo from './logo.svg';
import './App.css';

function App() {
  const handleImageUpload = async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
  
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      body: formData,
    });
  
    const result = await response.json();
    console.log(result);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
