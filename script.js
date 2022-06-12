const buttons = document.querySelectorAll('.buttonLed');
const realTimeButton = document.querySelector(".realTime");
const createAlgorithm = document.querySelector(".createAlgorithm");

function getDataFromLed(id) {
    const btn = document.getElementById(id);
    if (btn.className === 'buttonLed') {
        sendCommandToServer("button_" + id)
    }
}

// getDataFromLed()


function sendCommandToServer(command) {
    fetch("http://127.0.0.1:5000/calculator", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(command)
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Error');
        } else console.log(response)
    })

}

