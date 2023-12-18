import React from 'react';
import { data as mockData, data2 as comparedData } from './testData'
import { Chart as ChartJS, TimeScale, registerables } from 'chart.js';
import { Chart } from "react-chartjs-2";
ChartJS.register(TimeScale,...registerables);

// TODO I would probably have to bake my own bar graph, might be good practice to do anyways. 
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
      // animation: false
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
    return (<Chart type="bar" options={options} data={chartData} />);
};

export default OHLC_Chart