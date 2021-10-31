var socketurl = "http://localhost:5005/"
 function openPage(language)
 {
    if(language == "English")
    {
    socketurl = "http://localhost:5005/"
    // https://chatboten-dot-trustdspace.uc.r.appspot.com/
    !(function () {
            let e = document.createElement("script"),
              t = document.head || document.getElementsByTagName("head")[0];
            (e.src =
              "https://cdn.jsdelivr.net/npm/rasa-webchat/lib/index.js"),
              // Replace 1.x.x with the version that you want
              (e.async = !0),
              (e.onload = () => {
                window.WebChat.default(
                  {
                    // customData: {"loginData":JSON.parse(localStorage.getItem("userCredential"))['userId']},
                    socketUrl: socketurl,
                    // add other props here
                  },
                  null
                );
              }),
              t.insertBefore(e, t.firstChild);
          })();
    } else {
        socketurl = "http://35.225.138.189:5001/"
        // https://chatbotfr-dot-trustdspace.uc.r.appspot.com/
        !(function () {
          let e = document.createElement("script"),
            t = document.head || document.getElementsByTagName("head")[0];
          (e.src =
            "https://cdn.jsdelivr.net/npm/rasa-webchat/lib/index.js"),
            // Replace 1.x.x with the version that you want
            (e.async = !0),
            (e.onload = () => {
              window.WebChat.default(
                {
                  customData: {"loginData":JSON.parse(localStorage.getItem("userCredential"))['userId']},
                  socketUrl: socketurl,
                  // add other props here
                },
                null
              );
            }),
            t.insertBefore(e, t.firstChild);
        })();
    } 
}
