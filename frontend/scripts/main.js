
let ui = {
    htmlGenerateButton: document.querySelector("#generate-button"),
    htmlPrompt: document.querySelector("#prompt"),
    htmlGallery: document.querySelector("#gallery"),
    htmlImagesLeft: document.querySelector("#img-left"),
    htmlNumberInQueue: document.querySelector("#number-in-queue")
}

let locking = false;

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

async function run() {
    let networking = false;

    let FingerprintJS = await import('https://openfpcdn.io/fingerprintjs/v4');
    let fp = await FingerprintJS.load();
    let result = await fp.get();
    let visitorId = result.visitorId;
    let userInfo = await (await fetch("/user/get-user", {
        method: "POST",
        mode: "cors",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            { visitor_id: visitorId }
        )
    })).json();

    console.log(userInfo);
}


run();