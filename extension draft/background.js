

//Listen for messages
chrome.runtime.onMessage.addListener((msg, sender, response) => {

  if(msg.name == "fetchWords"){

      const apiCall = 'https://a6d1-124-253-248-169.ngrok.io/';
  
      //We call api..
      fetch(apiCall).then(function(res){
        //wait for response..
        if (res.status !== 200) {
          response({word: 'test'});
          return;
        }
        res.json().then(function(data) {
          //send the response...
          //Response
          response(data);
        });
      })
    
  }
  return true;
});
