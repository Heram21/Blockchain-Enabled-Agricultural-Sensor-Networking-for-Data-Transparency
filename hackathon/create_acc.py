from aptos_sdk.account import Account

# Generate a new account
account = Account.generate()

# Print the private key and public address
print("Private Key:", account.private_key)
print("Public Address:", account.address())