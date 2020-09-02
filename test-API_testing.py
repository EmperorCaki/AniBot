import requests

# Here we define our query as a multi-line string
query = '''
query ($id: Int) { # Define which variables will be used in the query (id)
  Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    id
    title {
      romaji
      english
      native
    }
  }
}
'''

# Define our query variables and values that will be used in the query request
variables = {
    'id': 15125
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})
data = response.text
print(response)
# print(data["Media"])
print(data)
print("\n\n\n\n\n")

for k, v in variables.items():
    print(k)
    print(v)

dictionary = {'abc': 123, 'RAY': 69, 'Gary': 1111, 'Nelson': 201, 'one': 1}
dict2 = {}
for key, value in dictionary.items():
    dict2[value] = key
print(dict2)
