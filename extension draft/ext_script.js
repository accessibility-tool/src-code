// ==UserScript==
// @name        wiki_script1
// @namespace   Violentmonkey Scripts
// @match       *://*wikipedia*/*
// @grant       none
// @version     1.0
// @author      -
// @require     http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js

// @description 22/11/2021, 02:41:03
// ==/UserScript==

API_URL = "https://55cd-49-156-77-5.ngrok.io/";

//get the url of the page
let url = window.location.href;
console.log(url);

//check if it wikipedia
const regex = new RegExp(".*://.*wikipedia.*/wiki/.*");
console.log(regex.test(url));

if (regex.test(url)) {
    const rep_regex = new RegExp(".*://.*wikipedia.*/wiki/");
    let content = url.replace(rep_regex, "").replaceAll("_", " "); //if its a wiki page,
    console.log(content); //extract the name of the page

    let wikisubdiv = document.getElementById("siteSub"); // "From wikipedia the free encyclopedia" div
    let chatdiv = document.createElement("div");
    let linkdiv = document.createElement("div");
    wikisubdiv.appendChild(chatdiv);
    let chatoutput = document.createElement("div");
    wikisubdiv.appendChild(chatoutput);
    wikisubdiv.appendChild(linkdiv);
  
    let chatinput = document.createElement("input");
    chatinput.setAttribute("type", "text");
    chatinput.id = "inputform";
    chatinput.style.border = "solid #D4F1F4";
    chatinput.style.borderRadius = "5px";
    chatinput.style.marginRight = "10px";
    chatdiv.appendChild(chatinput);
    let linksoutput = document.createElement("div");

    let btn = document.createElement("button");
    let t = document.createTextNode("Submit");
    btn.id = "button";
    btn.style.backgroundColor = "#D4F1F4";
    btn.style.font = "16px Calibri";
    btn.style.borderRadius = "5px";
    btn.style.borderWidth = "thin";
    btn.style.borderColor = "#D4F1F4";
    btn.appendChild(t);
    btn.style.boxShadow = "1px 1px 1px gray";
    chatdiv.appendChild(btn);
  
    let linksinput = document.createElement("input");
    linksinput.setAttribute("type", "text");
    linksinput.id = "linkinput";
    linksinput.style.border = "solid #D4F1F4";
    linksinput.style.borderRadius = "5px";
    linksinput.style.marginRight = "10px";
    linkdiv.appendChild(linksinput);
    let btn2 = document.createElement("button");
    let t2 = document.createTextNode("Get links");
    btn2.id = "linkbutton";
    btn2.style.backgroundColor = "#D4F1F4";
    btn2.style.font = "16px Calibri";
    btn2.style.borderRadius = "5px";
    btn2.style.borderWidth = "thin";
    btn2.style.borderColor = "#D4F1F4";
    btn2.style.boxShadow = "1px 1px 1px gray";
    btn2.appendChild(t2);
    linkdiv.appendChild(btn2);

    let mees = "hi"; 
    let numb = '10';

    chatoutput.textContent = "Loading";
    
    wikisubdiv.appendChild(linksoutput);

  
   async function train() {
        let resp = await fetch(API_URL + `chatbot/${content}`); //async function to handle call
        let data = await resp.json();
        return data;
    }

    async function get_resp() {
        
        let resp = await fetch(API_URL +`chatbot/get?` + new URLSearchParams({ msg: mees })); //async function to handle call
        let data = await resp.json();
        return data;
    }
  
    //var messag = prompt("chatbot test"); // prompt user to enter chatbot question
    train().then((data) => {
        //making call to api
        console.log(data);
        document.getElementById("button").addEventListener("click", function() {
          console.log(document.getElementById('inputform').value);
        mees = document.getElementById('inputform').value;
        get_resp().then((data) => {
            //making call to api
            console.log(data);
            chatoutput.textContent = data.message;
        });
    });
        
    });
  async function get_name(){
    let resp = await fetch(API_URL +`page_name/${content}`);
    let data = await resp.json();
    return data;
  }
  async function get_resp_clus() {
        let resp = await fetch(API_URL +`cluster/${content}/${numb}`); //async function to handle call
        let data = await resp.json();
        return data;
    }
  
  
  get_name().then((data) => {
    document.getElementById("linkbutton").addEventListener("click", function() {
    console.log("clicked");
    
    numb = document.getElementById('linkinput').value;
    if (numb == ""){
      
      numb = '10';
      console.log(numb);

    }
    get_resp_clus().then((data) => {
      console.log(data);
      linksoutput.textContent = data.recommendations;
    });
    });
  });
                  
  
}
