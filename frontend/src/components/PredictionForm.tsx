import React, { useState } from 'react';
import { useMutation } from 'react-query';
import axios from 'axios';

interface PredictionFormProps {
    symbol: string;
    onSuccess: (prediction: any) => void;
}

export const PredictionForm: React.FC<PredictionFormProps> = ({ symbol, onSuccess }) => {
    const [stakeAmount, setStakeAmount] = useState<number>(0.1);

    const mutation = useMutation(
        async () => {
            const response = await axios.post('/api/predict', {
                symbol,
                stake_amount: stakeAmount
            }, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            return response.data;
        },
        {
            onSuccess: (data) => {
                onSuccess(data);
            }
        }
    );

    return (
        <div className="prediction-form">
            <h3>Make Prediction for {symbol}</h3>
            <div className="form-group">
                <label>Stake Amount:</label>
                <input
                    type="number"
                    value={stakeAmount}
                    onChange={(e) => setStakeAmount(Number(e.target.value))}
                    min={0.1}
                    step={0.1}
                />
            </div>
            <button
                onClick={() => mutation.mutate()}
                disabled={mutation.isLoading}
            >
                {mutation.isLoading ? 'Submitting...' : 'Submit Prediction'}
            </button>
            {mutation.isError && (
                <div className="error-message">
                    Error submitting prediction
                </div>
            )}
        </div>
    );
}; 