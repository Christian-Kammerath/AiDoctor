

async function loadMenu(){
    let test = await fetch('/server/get_file_from_plugin/{"path":"extensions,plugins,Admin,menu,menuSettings.json"}');
    let x = await test.json();

    console.log(x);
    
    Object.keys(x.entries).forEach(key => {
        const entry = x.entries[key];

        newDiv = document.createElement('div');
        newDiv.className = 'menuItem';
        newImg = document.createElement('img');
        newImg.className = 'menuIcon';
        newTextNode = document.createTextNode(key);

        newDiv.addEventListener("click", () => {
            const showDiv = document.getElementById('show');
            showDiv.src = entry.htmlPath;
        });

        newImg.src = entry.iconPath;
        newDiv.appendChild(newImg);
        newDiv.appendChild(newTextNode);

        const showDiv = document.getElementById('menue');
        showDiv.appendChild(newDiv);

    });

}

loadMenu();


