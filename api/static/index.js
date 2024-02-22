const inputElement = document.getElementById('searchbar');
const responseElement = document.getElementById('response-text');

let today = new Date();
let year = today.getFullYear();
let month = String(today.getMonth() + 1).padStart(2, '0');
let day = String(today.getDate()).padStart(2, '0');

let formattedDate = `${year}-${month}-${day}`;

var systemPrompt = `You are ChatGPT, a large language model trained by OpenAI, based on the GPT-3.5 architecture. Knowledge cutoff: 2022-01. Current date: `+formattedDate;
systemPrompt = `You are ChatGPT, a large language model trained by OpenAI, based on the GPT-3.5 architecture. Answer all the users queries like the sort of text that is found on Wikipedia. Your answers should be in paragraphs, and deeply explain the subject, WHILE STILL BEING SOMEWHAT CONCISE.`;
var messages = [{"role":"system","content":systemPrompt}]

async function fetchData() {
    const url = '/get_resp';
    const data = {
        "messages":messages
    };

    try {
        const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
        });

        if (!response.ok) {
        throw new Error('Network response was not ok.');
        }

        const textResponse = await response.json();
        console.log('Raw text response:', textResponse["contentRaw"]);
        console.log('Formatted text response:', textResponse["content"]);
        receiveResponse(textResponse["content"],textResponse["contentRaw"],textResponse["success"]);
    } catch (error) {
        console.error('There was a problem fetching the data:', error);
    }
}

function receiveResponse(response,raw,success=true){
    if (!success){
        displayRawTextResponse("GPT API ran an in to an error: <strong>"+response+"</strong>")
        messages.push({"role":"assistant","content":"Ran in to an error, sorry!"});
        return;
    }
    displayRawTextResponse(response)
    messages.push({"role":"assistant","content":raw});
}

function displayRawTextResponse(text){
    responseElement.innerHTML = text
}

function displayTextResponse(text){
    responseElement.innerText = text
}

inputElement.onkeydown =  function(event) {
    if (event.code === "Enter") {
        console.log("Enter pressed");
        if ((messages.length > 0 && messages[messages.length - 1].role != "user") && !event.shiftKey) {
            var inputValue = inputElement.value.trim();
            messages.push({"role":"user","content":inputValue});
            inputElement.value = "";
            displayRawTextResponse('...');
            fetchData();
            return false;
        }else {
            console.log("new line");
        }
  }
};

document.addEventListener('DOMContentLoaded', function() {
    inputElement.focus();
});