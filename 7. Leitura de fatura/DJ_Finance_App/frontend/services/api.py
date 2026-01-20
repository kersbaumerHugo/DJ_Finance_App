import requests

BASE_URL = "http://localhost:8000/api"

def get_resumo():
   #print(f"{BASE_URL}/resumo")
   response = requests.get(BASE_URL+"/resumo")
   if response.status_code != 200:
      st.write('Status code:',resp.status_code)
      st.write('Resposta bruta:',resp.text)
   else:
      data = requests.get(BASE_URL+"/resumo").json()
      return data
def criar_lancamento(data:dict):
   return requests.post(BASE_URL+"/lancamentos",
                        json=data
                        )
def atualizar_lancamento(id, data):
   return requests.put(
            BASE_URL+"/lancamentos/"+str(id),
            json=data
      )
