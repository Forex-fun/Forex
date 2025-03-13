import React from 'react';
import { PredictionChart } from '../components/PredictionChart';
import { PredictionForm } from '../components/PredictionForm';
import { useQuery } from 'react-query';
import axios from 'axios';

export const Dashboard: React.FC = () => {
    const [selectedSymbol, setSelectedSymbol] = React.useState('BTC-USD');
    const [chartType, setChartType] = React.useState<'price' | 'technical'>('price');

    const { data: predictions } = useQuery('predictions', async () => {
        const response = await axios.get('/api/predictions', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        return response.data;
    });

    const handlePredictionSuccess = (prediction: any) => {
        // Refresh predictions or update UI
    };

    return (
        <div className="dashboard">
            <div className="controls">
                <select
                    value={selectedSymbol}
                    onChange={(e) => setSelectedSymbol(e.target.value)}
                >
                    <option value="BTC-USD">Bitcoin</option>
                    <option value="ETH-USD">Ethereum</option>
                </select>
                <select
                    value={chartType}
                    onChange={(e) => setChartType(e.target.value as 'price' | 'technical')}
                >
                    <option value="price">Price Chart</option>
                    <option value="technical">Technical Indicators</option>
                </select>
            </div>
            
            <div className="chart-section">
                <PredictionChart
                    symbol={selectedSymbol}
                    chartType={chartType}
                />
            </div>
            
            <div className="prediction-section">
                <PredictionForm
                    symbol={selectedSymbol}
                    onSuccess={handlePredictionSuccess}
                />
            </div>
            
            {predictions && (
                <div className="predictions-history">
                    <h3>Prediction History</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Predicted Price</th>
                                <th>Confidence</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {predictions.map((pred: any) => (
                                <tr key={pred.id}>
                                    <td>{pred.symbol}</td>
                                    <td>{pred.predicted_price}</td>
                                    <td>{pred.confidence_score}</td>
                                    <td>{pred.status}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}; 