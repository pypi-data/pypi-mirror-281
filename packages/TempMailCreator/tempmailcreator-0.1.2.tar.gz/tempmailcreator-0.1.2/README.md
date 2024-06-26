# Fast-Email

Library for creating and managing temporary email accounts with the mail.tm API.

## Installation

You can install the library using `pip`:

```bash
pip install TempMailCreator
```

# Usage
## Get available domains

```bash
domains = Lmi.domains()
print(f"Available domains: {domains}")
```
## Register a new account

```bash
new_account = Lmi.register()
print(f"Registered account: {new_account}")
```
## Get an authentication token

```bash
token = Lmi.get_token(new_account['email'], new_account['password'])
print(f"Authentication token: {token}")
```
## Get email messages

```bash
messages = Lmi.get_sms(token)
print(f"Messages: {messages}")
```