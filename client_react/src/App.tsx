import './App.css';
import React, {useState, useEffect} from 'react'
import BannerMessage from './components/adviceBanner'


function App() {
  const [data, setData] = useState([{}])

  useEffect(() => {
    // get json data from flask api
    fetch('/api/hello').then(
      res => res.json()
    ).then (
      data => {
        setData(data)
        console.log(data)
      }

    )
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <BannerMessage/>

      </header>
    </div>
  );
}

export default App;