from clientPackage import connecter,envoyer,fermer
from infoFetch import get_system_info
import json

connecter()

# preparer les informations systeme a envoyer
dict = {}
system_info = get_system_info(dict)

try:
    # envoyer les information au systeme
    envoyer(json.dumps(system_info))
    print("System information sent successfully.")
except json.JSONDecodeError as e:
    print(f"Error encoding system info to JSON: {e}")

fermer()
