import React from 'react';
import { data as mockData } from './testData'
import { Chart as ChartJS, TimeScale, registerables } from 'chart.js';
import {CandlestickController, CandlestickElement} from 'chartjs-chart-financial';
import { Chart } from "react-chartjs-2";
ChartJS.register(CandlestickElement, CandlestickController, TimeScale,...registerables);

interface OHLC_ChartProps {
  data: any[]; //  TODO build me
}

const OHLC_Chart: React.FC<OHLC_ChartProps> = (props) => {
    // props.data;
    const adjCloseData = mockData.entries.map((entry: any) => ({
        x: entry.date,
        y: entry.data['AdjClose'],
      }));

    const options = {

    }

    const chartData = {
        labels: adjCloseData.map((d) => d.x),
        datasets: [
          {
            label: 'Adjusted Close',
            data: [{
              x: new Date('2022-08-10').setHours(0, 0, 0, 0),
              o: 1.00,
              h: 1.35,
              l: 0.90,
              c: 1.20,
      
            }],
          },
        ],
      };
    return (<Chart type="candlestick" options={options} data={chartData} />);
};

export default OHLC_Chart

function DummyOHLC() {
  const adjCloseData = mockData.entries.map((entry: any) => ({
    x: entry.date,
    y: entry.data['AdjClose'],
  }));
  const data = {
    datasets: [{
      label: 'CHRT - Chart.js Corporation',
      data: [{
        x: new Date('2022-08-10').setHours(0, 0, 0, 0),
        o: 1.00,
        h: 1.35,
        l: 0.90,
        c: 1.20,

      }],
    }]
  }
  const chartData = {
    labels: adjCloseData.map((d) => d.x),
    datasets: [
      {
        label: 'Adjusted Close',
        data: [{
          x: new Date ('2022-08-10').setHours(0, 0, 0, 0),
          o: 1.00,
          h: 1.35,
          l: 0.90,
          c: 1.20,

      }],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };
  return (<Chart type="candlestick" data={data} />)
}


