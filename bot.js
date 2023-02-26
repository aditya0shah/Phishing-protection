let prepromt = "Is this a phising email? Reply in terms of probability from 0 to 100. Only reply with a number.\n\n"

let apiKey = "API_KEY";
let baseUrl = "https://api.openai.com";
let url = `https://api.openai.com/v1/completions`;

getIsPhishing = async (content) => {
    try {
        if (!content) {
            return "No content provided";
        }
        let promt = prepromt.concat(content);
        return await executePrompt(promt);
    } catch (e) {
        console.log(e);
    }
}

executePrompt = async (promt) => {
    try {
        if(!promt) return "No prompt"
        
        const rheaders = new Headers();
        rheaders.set('Authorization', `Bearer ${apiKey}`);
        rheaders.set('Content-Type', 'application/json');

        const response = await fetch(url, {
            method: 'POST',
            headers: rheaders,
            body: JSON.stringify(generateOpenAIPayload(promt))
        });

        if(!response.ok) {
            return `HTTP Code: ${response.status} - ${response.statusText}`;
        } else {
            const completion = await response.json();
            if(!completion || !completion.choices || !completion.choices[0] || !completion.choices[0].text) {
                return 'No response'
            } else {
                const result = completion.choices[0].text;
                return result;
            }
        }
    } catch (e) {
        console.log(e);
    }
}

generateOpenAIPayload = (prompt) => {
    return {
        prompt: prompt,
        max_tokens: 2000,
        temperature: 0,
        top_p: 1,
        frequency_penalty: 0.5,
        presence_penalty: 0,
        model: "text-davinci-003"
    };
};