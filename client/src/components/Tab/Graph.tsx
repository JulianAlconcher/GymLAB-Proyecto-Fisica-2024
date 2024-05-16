import Plot from 'react-plotly.js';

interface GraphProps {
    title : string
    type : any
    xAxisName : string
    yAxisName : string
    x : number []
    y : number []
}

function Graphic( {title, type, xAxisName, yAxisName, x, y}: GraphProps) : JSX.Element{
    
    return(
        <div className='w-full h-full'>
            <Plot 
                data={[
                    {
                        x: x,
                        y: y,
                        type: type,
                        mode: 'lines',
                        marker: { color: 'blue' },
                    }
                ]}
                layout={{title : title,
                         xaxis: { title: xAxisName },
                         yaxis: { title: yAxisName }
                }}
                style={{ width: '100%', height: '400px' }}
                config={{ responsive: true }}
                useResizeHandler={true}
            />
        </div>
    )
}

export default Graphic;