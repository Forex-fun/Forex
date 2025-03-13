import React from 'react';
import Plot from 'react-plotly.js';
import { useQuery } from 'react-query';
import axios from 'axios';

interface PredictionChartProps {
    symbol: string;
    chartType: 'price' | 'technical';
}

export const PredictionChart: React.FC<PredictionChartProps> = ({ symbol, chartType }) => {
    const { data, isLoading, error } = useQuery(
        ['chart', symbol, chartType],
        async () => {
            const response = await axios.get(`/api/chart/${symbol}?chart_type=${chartType}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            return response.data;
        }
    );

    if (isLoading) return <div>Loading chart...</div>;
    if (error) return <div>Error loading chart</div>;

    return (
        <div className="chart-container">
            <Plot
                data={data.data}
                layout={data.layout}
                useResizeHandler={true}
                style={{ width: '100%', height: '600px' }}
            />
        </div>
    );
}; 