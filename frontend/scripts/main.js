
let ui = {
    htmlGenerateButton: document.querySelector("#generate-button"),
    htmlPrompt: document.querySelector("#prompt"),
    htmlGallery: document.querySelector("#gallery"),
    htmlImagesLeft: document.querySelector("#img-left"),
    htmlNumberInQueue: document.querySelector("#number-in-queue")
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

async function update() {
    updating = fetch("/get-current-info");
    let current = updating;

    let info = await (await current).json();

    if (current != updating)
        return;

    ui.htmlImagesLeft.textContent = info.user.gen_left;
    ui.htmlNumberInQueue.textContent = info.generation_info.queue_no;

    if (info.image.path)
        ui.htmlGallery.appendChild(document.createElement("img")).src = info.image.path;
}

async function run() {
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

    if (!result)
        throw new Error("Error running app");

    ui.htmlGenerateButton.addEventListener("click", async function () {
        if (locking)
            return;

        lock();

        try {
            await fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    prompt: ui.htmlPrompt.textContent,
                    option: document.querySelector("input[name=option]:checked").value | 0
                })
            });

            update();
        }
        finally {
            unlock();
        }
    });

    setInterval(update, 5000);
    console.log(result);
}


run();