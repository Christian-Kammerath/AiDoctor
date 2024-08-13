document.getElementById('logout').addEventListener('click',async () =>{

    await fetch('/logout', { method: 'GET' });
    setTimeout(() => {
        window.location.href = '/?nocache=' + new Date().getTime();
    }, 100);
});