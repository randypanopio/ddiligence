import React from 'react';
import { data as mockData } from './testData'
import { Chart as ChartJS, TimeScale, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2'
ChartJS.register(TimeScale, ...registerables);

const LineGraph: React.FC = () => {
 const adjCloseData = mockData.entries.map((entry: any) => ({
   x: entry.date, // NOTE I used to import it as a date object, but since its already in format i want its probs fine
   y: entry.data['AdjClose'],
 }));

 const chartData = {
   labels: adjCloseData.map((d) => d.x),
   datasets: [
     {
       label: 'Adjusted Close',
       data: adjCloseData.map((d) => d.y),
       fill: false,
       borderColor: 'rgb(75, 192, 192)',
       tension: 0.1,
     },
   ],
 };

 const options = {
    scales: {
      x: {
        display: true
      },
    },
   };

 return <Line data={chartData} options={options}/>;
};

function StockChart() {
   return (
       <LineGraph/>
   )
}

export default StockChart;
