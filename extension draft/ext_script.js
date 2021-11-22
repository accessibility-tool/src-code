// ==UserScript==
// @name        wiki_script
// @namespace   Violentmonkey Scripts
// @match       *://*wikipedia*/*
// @grant       none
// @version     1.0
// @author      -
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

    let heading = document.getElementById("siteSub");
    let newElement = document.createElement("div");
    newElement.textContent = "Hello";
    heading.appendChild(newElement);

    async function train() {
        let resp = await fetch(API_URL + `chatbot/${content}`); //async function to handle call
        let data = await resp.json();
        return data;
    }

    async function get_resp() {
        let resp = await fetch(
            API_URL +
                `chatbot/get?` +
                new URLSearchParams({ msg: "What is carnegie mellon?" })
        ); //async function to handle call
        let data = await resp.json();
        return data;
    }

    train().then((data) => {
        //making call to api
        console.log(data);
        get_resp().then((data) => {
            //making call to api
            console.log(data);
            newElement.textContent = data.message;
        });
    });
}
