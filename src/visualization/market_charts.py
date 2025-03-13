import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

class MarketVisualizer:
    @staticmethod
    def create_price_prediction_chart(historical_data: pd.DataFrame, predictions: list):
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=('Price', 'Volume'),
            row_heights=[0.7, 0.3]
        )

        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=historical_data.index,
                open=historical_data['Open'],
                high=historical_data['High'],
                low=historical_data['Low'],
                close=historical_data['Close'],
                name='OHLC'
            ),
            row=1, col=1
        )

        # Add volume bar chart
        fig.add_trace(
            go.Bar(
                x=historical_data.index,
                y=historical_data['Volume'],
                name='Volume'
            ),
            row=2, col=1
        )

        # Add predictions
        if predictions:
            pred_dates = [p['timestamp'] for p in predictions]
            pred_values = [p['predicted_price'] for p in predictions]
            fig.add_trace(
                go.Scatter(
                    x=pred_dates,
                    y=pred_values,
                    mode='markers+lines',
                    name='Predictions',
                    line=dict(color='red', dash='dot')
                ),
                row=1, col=1
            )

        # Update layout
        fig.update_layout(
            title='Market Price and Predictions',
            yaxis_title='Price',
            yaxis2_title='Volume',
            xaxis_rangeslider_visible=False
        )

        return fig

    @staticmethod
    def create_technical_indicators_chart(data: pd.DataFrame):
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price & MA', 'RSI', 'MACD'),
            row_heights=[0.5, 0.25, 0.25]
        )

        # Price and Moving Averages
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Close'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['SMA_20'],
                name='SMA 20'
            ),
            row=1, col=1
        )

        # RSI
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['RSI'],
                name='RSI'
            ),
            row=2, col=1
        )

        # MACD
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['MACD'],
                name='MACD'
            ),
            row=3, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Signal_Line'],
                name='Signal Line'
            ),
            row=3, col=1
        )

        # Update layout
        fig.update_layout(
            title='Technical Indicators',
            height=900
        )

        return fig 