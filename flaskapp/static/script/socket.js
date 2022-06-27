document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('message', data => {
        const p = document.createElement('p');
        const br = document.createElement('br');
        p.innerHTML = data;
        document.querySelector('#view-message').append('p');
    })
    document.querySelector('#send').onclick() = () => {
        socket.send(document.querySelector('#message').value);
    }
})
