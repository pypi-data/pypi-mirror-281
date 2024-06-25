DESCRIPTION

After years of trying to convert screenplay PDFs to a machine-readable format consistently
using Final Draft and PDF Python tools, we decided to create our own screenplay PDF to JSON
converter using OpenAI vision transformers. The results are much more reliable for our purposes.

The package converts a Screenplay PDF into a JSON file using the OpenAI API,
returns JSON and writes it to a local file whose name is the screenplay filename.json
The process currently costs about 50 cents via the OpenAI API to convert an hour-long pilot,
but will not doubt go down in price exponentially over time.

Below is an example of the JSON structure output to file:
[
    {
        "type": "Dialogue",
        "Name": "JOHN",
        "Modifier": "(V.O.)",
        "Speech": "Hello, how are you?",
        "page": 1
    },
    {
        "type": "Action",
        "text": "John walks into the room.",
        "page": 3
    },
    {
        "type": "Dialogue",
        "Name": "MARY",
        "Parenthetical": "(smiling)",
        "Speech": "I'm good, thank you!",
        "page": 4
    },
    {
        "type": "Dialogue",
        "Name": "JOHN",
        "Speech": "That's great to hear.",
        "page": 4
    },
    {
        "type": "Scene",
        "text": "INT. LIVING ROOM - DAY",
        "page": 5
    }
]

GETTING STARTED

Installation:
pip install screenplay_pdf_to_json

OpenAI:
You will need to provide you own OpenAI key.
Follow the instructions here: https://platform.openai.com/docs/quickstart

Known Issues:
Because it uses a statistical model, sometimes \n\n split action lines will be combined into a single JSON Action element and sometimes into multiple Action elements.
Also, if slug-lines are used WITHOUT INT and EXT then their behaviour is unpredictable but easily detectable.

QUICKSTART

1. CONVERT WHOLE SCREENPLAY

from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJson(api_key=<your_openai_key>)
data = sptj.convert('TheEmpireStrikesBack.pdf')

2. CONVERT FIRST 3 PAGES OF A SCREENPLAY

from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJson(api_key=<your_openai_key>)
data = sptj.convert('TheEmpireStrikesBack.pdf', end_page=3)

3. ESTIMATE COST OF CONVERTING A SCREENPLAY

from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJson(api_key=<your_openai_key>)
cost = sptj.estimate_cost('TheEmpireStrikesBack.pdf')
print(f"Estimated cost to convert screenplay: ${cost:.2f}")

4. CONVERT SCREENPLAY WITH NO TITLE PAGE

from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJSON(api_key=KEY, skip_title_page=False)
data3 = sptj.convert('screenplay_with_no_title_page.pdf')


