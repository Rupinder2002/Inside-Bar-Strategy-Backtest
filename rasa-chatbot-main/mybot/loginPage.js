function Submit()
{
var http = new XMLHttpRequest()
var url ="http://localhost:3000/api/users/login"
var username = document.getElementById("userName").value
var password = document.getElementById("password").value
 console.log("username,password",username,password)
http.open('POST',url,true);
http.setRequestHeader("Accept", "application/json");
http.setRequestHeader('Content-type','application/json')
http.onreadystatechange = function() {//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {
        console.log("httpResponse---",http.response)
        if(http.response)
        {
        let userCredentialObject = JSON.parse(http.response)
        localStorage.setItem("userCredential",JSON.stringify(userCredentialObject))
        console.log(userCredentialObject['id'])
        window.location.href = "ChatPage.html"
        }
    }
}
var params = {"username":username,"password":password}
http.send(JSON.stringify(params));
}