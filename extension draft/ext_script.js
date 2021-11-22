// ==UserScript==
// @name        wiki_script
// @namespace   Violentmonkey Scripts
// @match       *://*wikipedia*/*
// @grant       none
// @version     1.0
// @author      -
// @require     http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js

// @description 22/11/2021, 02:41:03
// ==/UserScript==

API_URL = "https://e0b3-124-253-120-242.ngrok.io/";

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

    let heading1 = document.getElementById("siteSub"); 
    let heading = document.createElement("div");
    heading1.appendChild(heading);
    let newElement = document.createElement("div");
    let newElement1 = document.createElement("input");
    newElement1.setAttribute("type", "text");
    newElement1.id = "inputform";
    heading.appendChild(newElement1);
    let newElement2 = document.createElement("div");
  
    let btn = document.createElement("button");
    let t = document.createTextNode("Submit");
    btn.id = "button";
    btn.appendChild(t);
    heading.appendChild(btn);
    
    let btn2 = document.createElement("button");
    let t2 = document.createTextNode("Get links");
    btn2.id = "linkbutton";
    btn2.appendChild(t2);
    heading.appendChild(btn2);  

    let mees = "hi";

    newElement.textContent = "Loading";
    heading1.appendChild(newElement);
    heading1.appendChild(newElement2);

  
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
            newElement.textContent = data.message;
        });
    });
        
    });
  async function get_name(){
    let resp = await fetch(API_URL +`page_name/${content}`);
    let data = await resp.json();
    return data;
  }
  async function get_resp_clus() {
        let resp = await fetch(API_URL +`cluster/${content}/10`); //async function to handle call
        let data = await resp.json();
        return data;
    }
  
  
  get_name().then((data) => {
    document.getElementById("linkbutton").addEventListener("click", function() {
          console.log("clicked");
    get_resp_clus().then((data) => {
      console.log(data);
      newElement2.textContent = data.recommendations;
    });
    });
  });
                  
  
}

















