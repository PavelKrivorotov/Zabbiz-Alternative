
const SERVER_IP = '127.0.0.1'
const SERVER_PORT = 8000

const GET_REQUEST_PATH_JVM_MEMORY = '/jvm-memory/3'


const pageCharts = {
    chart1: { elemetId: 'canvas-id-1', instanceName: 'HOST-1', chartObj: null },
    chart2: { elemetId: 'canvas-id-2', instanceName: 'HOST-2', chartObj: null },
    chart3: { elemetId: 'canvas-id-3', instanceName: 'HOST-3', chartObj: null }
}


window.onload = async (event) =>{
    console.log("onLoad started!")
    draw()
}



function urlConstructor(ip, port, path) {
    return `http://${ip}:${port}${path}`
}

async function getJvmMemory(instance) {
    try {
        let res = await fetch(
            urlConstructor(
                SERVER_IP,
                SERVER_PORT,
                GET_REQUEST_PATH_JVM_MEMORY
            ),
            {
                headers: {
                    "Instance": instance
                }
            }
        )

        if (res.ok) { return await res.json() }
        else { throw new Error(res.statusText); }

    } catch (error) {
        console.error(error)

        return JSON.stringify({
            labels: [],
            values: []
        })
    }
}


async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function convertMemory(memory) {
    var mem = memory / (2**10)
    if (mem < 1024) { return mem.toFixed(1) + 'Kb' }

    mem = mem / (2**10)
    if (mem < 1024) { return mem.toFixed(1) + 'Mb' }

    mem = mem / (2**10)
    return mem.toFixed(1) + 'Gb'
}


async function drawChart(chart) {
    const data = await getJvmMemory(chart['instanceName'])
    await clearChart(chart)

    const chartLine = new Chart(
        document.getElementById(chart['elemetId']),
        {
            type: 'line',
            data: {
                labels: data.labels.map(val => new Date(val*1000).toLocaleString()),
                datasets: [
                    {
                        label: `JVM Memory Heap (${chart['instanceName']})`,
                        data: data.values
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        ticks: {
                            callback: function(value, index, ticks) {
                                return convertMemory(value)
                            }
                        }
                    }
                }
            }
        }
    );

    chart['chartObj'] = chartLine
}

async function clearChart(chart) {
    if (chart['chartObj']) {
        chart['chartObj'].destroy()
        chart['chartObj'] = null
    }
}


async function draw() {
    while (true) {
        drawChart(pageCharts.chart1)
        drawChart(pageCharts.chart2)
        drawChart(pageCharts.chart3)

        await sleep(60*1000)
    }
}

