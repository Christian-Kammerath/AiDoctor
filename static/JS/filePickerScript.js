async function loadFiles() {

    let path = document.getElementById('filePickerPath');

    if(path.value.length < 1){
        path = await fetch('http://0.0.0.0:8000/basePath')
        path = await path.json();
    }
    else{
        path = path.value;
    }

    const response = await fetch('http://0.0.0.0:8000/getFilesDivs', {
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
        const container = document.getElementById('fileView');
        container.innerHTML = ""

        const result = data['result'];

        result.forEach(element => {
            const div = document.createElement('div');
            div.className = 'fileX';
            div.dataset.sourcePath = element['path'];
            div.dataset.isSelect = false;


            div.addEventListener('dblclick', () => {
                document.getElementById('filePickerPath').value = element['path'];
                container.innerHTML = ""
                loadFiles();
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

loadFiles();
