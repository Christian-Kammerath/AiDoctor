async function loadFiles(mode,targetDiv) {

    let path = "";
    let pathDiv = "";
    
    let settings = await fetch('/module/publicSettings.json');
    settings = await settings.json();

    basic_address = "";
    

    if(mode === 'client'){
        basic_address = `${settings['connect']['client_ip']}:${settings['connect']['client_port']}`;
        path = document.getElementById('filePickerPathClient');
        pathDiv = "filePickerPathClient";

    }
    else if (mode === 'server'){
        basic_address = `${settings['connect']['server_ip']}:${settings['connect']['server_port']}`;
        path = document.getElementById('filePickerPathServer');
        pathDiv = "filePickerPathServer";

    }


    if(path.value.length < 1){
        path = await fetch(`http://${basic_address}/${mode}/basePath`)
        path = await path.json();
    }
    else{
        path = path.value;
    }

    let test = `http://${basic_address}/${mode}/getFilesDivs`;
    console.log(test);
    const response = await fetch(test, {
        method: "POST",
        body: JSON.stringify({
            path: path
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
    if (response.ok) {
        const data = await response.json();
        const container = document.getElementById(targetDiv);
        container.innerHTML = ""

        const result = data['result'];

        result.forEach(element => {
            const div = document.createElement('div');
            div.className = 'fileX';
            div.dataset.sourcePath = element['path'];
            div.dataset.isSelect = false;


            div.addEventListener('dblclick', () => {
                document.getElementById(pathDiv).value = element['path'];
                container.innerHTML = ""
                loadFiles(mode,targetDiv);
            });
            div.addEventListener('click', () => {

                if(div.dataset.isSelect === "true"){
                    div.dataset.isSelect = false;
                    div.style = "background-color: rgba(16, 30, 95, 0)";
                }
                else{
                    div.style = "background-color: rgb(16, 31, 95);";
                    div.dataset.isSelect = true;
                }
                
            });

            const img = document.createElement('img')
            img.src =  'http://0.0.0.0:8000/' +element['icon_path'];
            div.appendChild(img);

            const text = document.createTextNode(element['name']);
            div.appendChild(text);

            container.appendChild(div);

        });


    } else {
        console.error('Error:', response.statusText);
    }
}


async function select(){
    const container = document.getElementById('fileView');
    
    const divs = container.getElementsByClassName('fileX');
    const selectedDivs = Array.from(divs).filter(div => div.dataset.isSelect === "true");
    return selectedDivs;
}



loadFiles('client','client');
loadFiles('server','server');

