chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (
    message.action === "tabUpdated" &&
    message.url.startsWith("https://mail.google.com/mail/u/0/#inbox")
  ) {
    console.log("tab updated.")
    chrome.tabs.executeScript(sender.tab.id, { file: "gmailVerify.js" });
  }
});

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.status === "complete") {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var url = tabs[0].url;
        if (url.startsWith("https://mail.google.com/mail/u/0/#inbox")) {
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: () => {
              const messageListElem = document.querySelector('[role="main"]'); 
              if (messageListElem != null) {
                messageListElem.addEventListener("click", function (event) {
                  let targetElem = event.target;
  
                  while (
                    targetElem &&
                    targetElem.getAttribute("data-message-id") === null
                  ) {
                    targetElem = targetElem.parentElement;
                  }
  
                  if (targetElem) {
                    const messageId = targetElem.getAttribute("data-message-id");
                    console.log("Clicked message ID:", messageId);
  
                    gapi.client.gmail.users.messages
                      .get({
                        'userId': "me",
                        'id': messageId,
                        'format': "full",
                      })
                      .then(function (response) {
                        var param = response.result.payload.body.data;
                        chrome.tabs.executeScript(tabId, {
                            file: 'gmailVerify.js'
                        }, function() {
                            chrome.tabs.sendMessage(tabId, {parameter: param})
                        })
                      });
                  }
                });
              }
            },
          });
        }
      });
    }
  });
