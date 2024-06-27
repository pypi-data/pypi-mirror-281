# getSecrets package


getSecrets is a simple package that reads a secret from a Hashicorp vault

usage:

```
from get_secrets import get_secret

data = get_secret(<id>)
```

Vault parameters are stored in a config file ~/.config/.vault/.vault.yml
```
vault:
  token: "<access token>"
  vault_addr: "https://vault:8200"
  certs: "<path>/bundle.pem"
```