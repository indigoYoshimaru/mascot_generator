
let ui = {
    htmlGenerateButton: document.querySelector("#generate-button"),
    htmlPrompt: document.querySelector("#prompt"),
    htmlGallery: document.querySelector("#gallery"),
    htmlImagesLeft: document.querySelector("#img-left"),
    htmlNumberInQueue: document.querySelector("#number-in-queue"), 
    htmlImgGallery: document.querySelector("#img-gallery"), 
}

let locking = false;
let updating;

function lock() {
    locking = true;

    for (let key in ui) {
        ui[key].disabled = true;
    }
}

function unlock() {
    locking = false;

    for (let key in ui) {
        ui[key].disabled = false;
    }
}

async function register() {
    let FingerprintJS = await import('https://openfpcdn.io/fingerprintjs/v4');
    let fp = await FingerprintJS.load();
    let visitorId = (await fp.get()).visitorId;
    let result = await (await fetch("/user/get-user", {
        method: "POST",
        mode: "cors",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            { visitor_id: visitorId }
        )
    })).json();
    return result;
}

async function reset() {
    try {
        let result = await (await fetch("/user/delete-session", {
            method: "POST",
            mode: "cors",
            headers: {
                'Content-Type': 'application/json',
            },
        })).json();
        return result;
    }
    catch {
        return;
    }
}

async function update() {
    updating = fetch("/get-current-info");
    let current = updating;

    let info = await (await current).json();

    // if (!info){
    //     result = await register();
    // }

    if (current != updating)
        return;

    if (info.user) {
        ui.htmlImagesLeft.textContent = info.user.gen_left;
        ui.htmlNumberInQueue.textContent = info.generation_info.queue_no;
    }

    if (info.generation_info){
        ui.htmlGallery.innerHTML="";
        ui.htmlGallery.appendChild(document.createElement("img")).src = info.generation_info.image.path;
        getImageHistory();
    }

}

async function getSamplePrompt() {
    let sample = await (await fetch("/txt2img/get-example-prompt")).json();

    ui.htmlPrompt.placeholder = sample;
}

async function getImageHistory(){
    let images = await (await fetch("/get-image-history")).json();
    ui.htmlImgGallery.innerHTML="";
    for (let idx in images){
        let image = images[idx]
        ui.htmlImgGallery.appendChild(document.createElement("img")).src=image;
    }
}

async function run() {
    lock();
    update();
    getSamplePrompt();
    await getImageHistory();
    let _ = await reset();
    let result = await register();

    if (!result)
        throw new Error("Error running app");

    ui.htmlGenerateButton.addEventListener("click", async function () {
        if (locking || !ui.htmlPrompt.value)
            return;

        lock();

        let res = null;
        try {
            while (!res) {
                let response = await fetch("/txt2img/generate", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        prompt: ui.htmlPrompt.value,
                        option: document.querySelector("input[name=option]:checked").value | 0
                    })
                });
                if (response.status==403)
                    continue;
                res = await(response.json());
                
            }
            console.log(res)
            update();
        }
        finally {
            unlock();
            if (res.detail)
                ui.htmlPrompt.value = res.detail;
        }
    });

    ui.htmlPrompt.addEventListener("dblclick", function (e) {
        if (e.ctrlKey && !ui.htmlPrompt.value.includes(ui.htmlPrompt.placeholder))
            ui.htmlPrompt.value += ui.htmlPrompt.placeholder;
    });
    unlock();
    setInterval(update, 6000);
    console.log(result);

}

lock();

setTimeout(run, 1000);