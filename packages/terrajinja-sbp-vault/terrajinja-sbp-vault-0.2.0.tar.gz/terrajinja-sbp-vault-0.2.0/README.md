# terrajinja-sbp-vault

This is an extension to the vault provider for the following modules.
The original documentation can be found [here](https://registry.terraform.io/providers/hashicorp/vault/latest/docs)

# SBP Specific implementations
Here is a list of supported resources and their modifications

## sbp.vault.kv_secret_v2
Original provider: [vault.kv_secret_v2](https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/kv_secret_v2)

This custom provider adds the following:
- automaticly convert data to json as input for the resource
- automaticly create random passwords if requested

| old parameter | new parameter | description                                                           |
| ------ | ------ |-----------------------------------------------------------------------|
| data_json | data | the data field is automaticly converted to json                       |
| lifecycle | - | default is set to ignore all changes only if random passwords are used |

additional to the above the data structure expected is in the format:
```
{ 
    "key": "value",
    "key2": "value2",
}
```
if any of the values contains the word "random" then a rendomly generated password is created of 30 characters

example:
```
{
    "my_secret": "random"
}
```
will result in a random string being created as password for my_secret

### terrajinja-cli example
the following is a code snipet you can used in a terrajinja-cli template file.
This created both the hashicorp vault with the name `generic`, and adds a secret in it in the path `application` with key `admin` that contains a random password
```
terraform:
  resources:
    - task: vault-mount-generic
      module: vault.mount
      parameters:
        path: "generic"
        type: "kv"
        options:
            version: "2"

    - task: vault-application-password
      module: sbp.vault.kv_secret_v2
      parameters:
        mount: $vault-mount-generic.path
        name: "application"
        data:
          admin: "random"
```

