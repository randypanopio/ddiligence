import './App.css';
import React, {useState, useEffect} from 'react'
import BannerMessage from './components/adviceBanner'
import LineGraph from './components/LineStockChart';
import OHLC_Chart from './components/OHLCStockChart';
import OverlayLineGraph from './components/OverlayLineChart';

import { data as mockData, data2 as comparedData } from './components/testData'


function App() {
  // TODO replace me with cleaned API data
  const mappedFirstSet = mockData.entries.map((entry) => ({
    date: new Date(entry.date),
    data: entry.data.AdjClose
  }))

  const mappedSecondSet = comparedData.entries.map((entry) => ({
    date: new Date(entry.date),
    data: entry.data.AdjClose
  }))

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
        <OverlayLineGraph first_dataset={mappedFirstSet} second_dataset={mappedSecondSet}/>
      </header>
    </div>
  );
}

export default App;
