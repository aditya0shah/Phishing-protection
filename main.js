let fromAddress = "";
let body = "";

setInterval(async () => {
    let newAddress = "";

    let emailNodes = document.getElementsByClassName("go");
    if (emailNodes && emailNodes.length > 0 && emailNodes[0]) {
        newEmail = emailNodes[0].innerText;
        if (newEmail !== fromAddress) {
            fromAddress = newEmail;

            let bodyNodes = document.getElementsByClassName("gs");
            if (bodyNodes && bodyNodes.length > 0) {
                body = bodyNodes[0].getInnerHTML();
            }
            let maxBodyLength = Math.min(body.length, 2000);
            body = body.substring(0, maxBodyLength);
            body = escapeHtml(body);

            let content = `From: ${fromAddress}\nBody:\n${body}\n\n\n`;

            let response = await getIsPhishing(content);
            console.log(response);
            try {
                if(parseInt(response) > 50) {
                    // console.log("scam")
                    let div = document.createElement("div");
                    document.getElementsByClassName("nH V8djrc byY")[0].appendChild(div);
                    div.innerText = "Likely a phishing email. Proceed with caution."
                    div.style.color = "red"
                } else {
                    let div = document.createElement("div");
                    document.getElementsByClassName("nH V8djrc byY")[0].appendChild(div);
                    div.innerText = "Email looks to be safe."
                    div.style.color = "green"
                }
            } catch (e) {
                console.log(e);
            }
        }
    }
}, 2 * 1000);

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
