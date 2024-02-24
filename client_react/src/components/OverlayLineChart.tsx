import React from 'react';
import { Chart as ChartJS, TimeScale, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2'
ChartJS.register(TimeScale, ...registerables);

interface OverlayEntry {
    date: Date
    data: number
}

interface OverlayLineGraphProps {
    first_dataset: OverlayEntry[]
    second_dataset: OverlayEntry[]
}

const OverlayLineGraph: React.FC<OverlayLineGraphProps> = (input) => {
    const chartData = {
        labels: input.first_dataset.map((d) =>
            // NOTE should this function assume the x Axis are aligned? for now probably fine
            // TODO this is gross, maybe I shouldn't take Date objects, or can I get chartJS to just display MDY?
            d.date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })),
        datasets: [
            {
                label: 'Dataset 1',
                data: input.first_dataset.map((d) => d.data),
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                yAxisID: 'y',
            },
            {
                label: 'Dataset 2',
                data: input.second_dataset.map((d) => d.data),
                borderColor: 'rgb(53, 162, 235)',
                backgroundColor: 'rgba(53, 162, 235, 0.5)',
                yAxisID: 'y1',
            }],
    };

    const options = {
        responsive: true,
        interaction: {
            mode: 'index' as const,
            intersect: false,
        },
        stacked: false,
        plugins: {
            title: {
                display: true,
                text: 'Chart.js Line Chart - Multi Axis',
            },
        },
        scales: {
            y: {
                type: 'linear' as const,
                display: true,
                position: 'left' as const,
            },
            y1: {
                type: 'linear' as const,
                display: true,
                position: 'right' as const,
                grid: {
                    drawOnChartArea: false,
                },
            },
        },
    };

    return <Line data={chartData} options={options} />;
};


export default OverlayLineGraph;
