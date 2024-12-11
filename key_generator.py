import tink
from tink import aead
from tink import JsonKeysetWriter, JsonKeysetReader, tink_config

# Tink initialization
tink_config.register()

# Generation of the master key
master_keyset_handle = tink.new_keyset_handle(aead.aead_key_templates.AES128_GCM_SIV)

# Serialization of the master key into a JSON file (unprotected)
with open("master_key.json", "w") as master_key_file:
    writer = JsonKeysetWriter(master_key_file)
    json_keyset = master_keyset_handle._keyset  # Direct access to the serialized key (unprotected)
    writer.write(json_keyset)

print("Master key saved in master_key.json")


# Creating the AEAD primitive from the master key
master_aead = master_keyset_handle.primitive(aead.Aead)

# Generation of the keyset to protect
keyset_handle = tink.new_keyset_handle(aead.aead_key_templates.AES128_GCM_SIV)

# Writing the keyset into a JSON file, protected by the master key
with open("encrypted_keyset.json", "w") as keyset_file:
    writer = JsonKeysetWriter(keyset_file)
    keyset_handle.write(writer, master_aead)

print("Encrypted keyset saved in encrypted_keyset.json")