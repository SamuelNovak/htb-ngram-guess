import nexmo
from pprint import pprint

client = nexmo.Client(
    application_id="e8c35f41-475e-4540-afca-f5ccd40d6eec",
    private_key="hack/private.key",
)

response = client.create_call({
  'to': [{'type': 'phone', 'number': "+447858989733"}],
  'from': {'type': 'phone', 'number': "+447858989733"},
  'answer_url': ['https://developer.nexmo.com/ncco/tts.json']
})

pprint(response)