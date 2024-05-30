import Plot from 'react-plotly.js';
import { ScatterData } from 'plotly.js';

interface GraphProps {
    title: string;
    type: 'scatter' | 'bar' | 'line';
    xAxisName: string;
    yAxisName: string;
    x: number[];
    y: number[];
    currentTime: number;
}

function Graphic({ title, type, xAxisName, yAxisName, x, y, currentTime }: GraphProps): JSX.Element {
    const highlightPoint = (): Partial<ScatterData> => {
        const closestIndex = x.reduce((prev, curr, index) => {
            return Math.abs(curr - currentTime) < Math.abs(x[prev] - currentTime) ? index : prev;
        }, 0);
        return {
            x: [x[closestIndex]],
            y: [y[closestIndex]],
            type: 'scatter',
            mode: 'markers',
            marker: { color: 'red', size: 12 },
            showlegend: false
        };
    };

    const annotations = [
        {
            x: x.find((_, index) => index === x.reduce((prev, curr, index) => (Math.abs(curr - currentTime) < Math.abs(x[prev] - currentTime) ? index : prev), 0)),
            y: y.find((_, index) => index === x.reduce((prev, curr, index) => (Math.abs(curr - currentTime) < Math.abs(x[prev] - currentTime) ? index : prev), 0)),
            text: `${y[x.reduce((prev, curr, index) => (Math.abs(curr - currentTime) < Math.abs(x[prev] - currentTime) ? index : prev), 0)]} m/s`,
            showarrow: true,
            arrowhead: 2,
            ax: 0,
            ay: -40
        }
    ];

    return (
        <div className="w-full h-full">
            <Plot 
                data={[
                    {
                        x: x,
                        y: y,
                        type: type,
                        mode: 'lines',
                        marker: { color: 'black' }
                    } as Partial<ScatterData>,
                    highlightPoint()
                ]}
                layout={{
                    title: title,
                    xaxis: { title: xAxisName },
                    yaxis: { title: yAxisName },
                    font: { color: 'black' },
                    annotations: annotations,
                    showlegend: false
                }}
                style={{ width: '100%', height: '400px' }}
                config={{ responsive: true }}
                useResizeHandler={true}
            />
        </div>
    );
}

export default Graphic;