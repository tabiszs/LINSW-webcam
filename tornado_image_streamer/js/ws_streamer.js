
$(document).ready(function() {

    time_0 = (new Date()).getTime();
    ws_imagestream = null;
    image = null;
    counter = 0;
    is_stream = 0;

    update_fps = function() {
        counter += 1;
        if ((counter % 10) == 0) {
            tdif = (new Date()).getTime() - time_0;
            time_0 = (new Date()).getTime();
            fps = Math.round(10 * 1.0 / (tdif / 1000.0));
            $('#actual').text(fps);
        }
    }

    $('#fps').on('change', function() {
        var cmd = 'interval=' + $(this).val();
        console.log(cmd);
        ws_imagestream.send(cmd);
    });

    $('#alret_close').on('click', function() {
        alert=document.getElementById('alert')
        alert.style.display = 'none';
    })

    $('#photo').on('click', function() {
        
        function httpGetAsync(theUrl)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.responseType.document
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 &&  xmlHttp.status == 200) {                    
                    image = xmlHttp.responseText

                    alert=document.getElementById('alert')
                    alert.style.display = 'block'

                    a=document.getElementById('download_link')
                    a.href = 'image/'+ image
                    a.download = image
                }   
            }
            xmlHttp.open("GET", theUrl, true); // true for asynchronous 
            xmlHttp.send(null);
        }

        console.log('make photo');
        httpGetAsync('/photo')
    })

    $('#stream').on('click', function() {
               
        if(is_stream == 0)
        {
            console.log('start stream'); 
            is_stream = 1;
            ws_imagestream = set_web_socket();
            stream.innerText = 'Stop Stream'
            stream.style.backgroundColor = '#dc3545';
            stream.style.borderColor = '#dc3545';
            stream_view.style.display = 'block';
        }
        else
        {
            console.log('stop stream'); 
            is_stream = 0;
            ws_imagestream.close();
            stream.innerText = 'Start Stream'
            stream.style.backgroundColor = '#0d6efd';
            stream.style.borderColor = '#0d6efd';
            stream_view.style.display = 'none';
        }
    })
});

function set_web_socket() {
    ws_imagestream = new_web_socket('imagestream');

    ws_imagestream.onmessage = function(e) {
        var interval = parseInt($('#fps').val());
        if (e.data instanceof Blob) {
            update_fps()
            image.src = URL.createObjectURL(e.data);
            image.onload = function() {
                URL.revokeObjectURL(image.src);
            }
        }
        if (window.stream_mode == "get") {
            setTimeout(function(){ws_imagestream.send('?')}, interval);
        }
    }

    ws_imagestream.onopen = function() {
        console.log('connected ws_imagestream...');
        ws_imagestream.send('?');
    };
    ws_imagestream.onclose = function() {
        console.log('closed ws_imagestream');
    };
    return ws_imagestream;
}

function new_web_socket(uri_path) {
    var protocol = 'ws:';
    if (window.location.protocol === 'https:') {
        protocol = 'wss:';
    }
    var host = window.location.host;
    var path = window.location.pathname;
    var url = protocol + '//' + host + path + uri_path;
    var ws = new WebSocket(url);
    console.log(url);
    return ws;
}