import requests
import json
dummy_knows_query = """
asdasdasd 
SELECT DISTINCT ?s ?p ?o ?o
WHERE {
?s ?p ?o
}
asdasdasd
"""

knows_query=""
# Direct to the ollama
for byte_response in requests.get(url="http://tentris-ml.cs.upb.de:8000/api/ollama",
                                  headers={"accept": "application/json", "Content-Type": "application/json"},
                                  json={"model": "codestral:latest",
                                        "prompt": f"Extract the SPARQL query from this following text\n"
                                                  f"Text: [ {dummy_knows_query} ]\n"
                                                  "Do not provide any other information. Only and only print the SPARQL query",
                                        "options": {"seed": 1, "temperature": 0},
                                        "stream": True},
                                  stream=True).iter_lines():
    delta = json.loads(byte_response.decode())
    knows_query+=delta["response"]
import rdflib
g = rdflib.Graph()
g.parse("KGs/Family/family-benchmark_rich_background.owl")
g2 = rdflib.Graph() + g

results = ""
for raw_iterable in g2.query(knows_query):
    results+=" ".join([value.toPython()  for binding, value in raw_iterable.asdict().items()])+"\n"
print(results)