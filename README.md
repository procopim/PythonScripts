keystore.py
  - requires packages:  cryptography, os, json, sys
  - Usage: `python keystore.py <store|retrieve> <service_name>`
  - Description: this program allows you to store secret keys and retrieve them for various services as will. It will create a master key stored in the execution directory for your user (linux focused), and uses symmetrical encryption to store those secrets in a non-clear text fashion.
