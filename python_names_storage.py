from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "famous-tree-382223",
  "private_key_id": "80152af5185fdfe938f80cbdc4b3d695a54fcccc",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDSSXTh1pAKVXaH\nmqybTEb4zFoO/KZPSUdh+MYlyHcd8ajXrdLG4UV9utJUu81rc5LUeBW/Lrl/wqQX\n5VV94xgJm7gaV4vYlzsMPhYDXa3NoTP43u1ajdY9SjvgsIF1P4pnPWuyvhl/F+W/\n8ScmjjVwY2NMrtZUKcasDN2BBSHo9/nSdJWtn1rDQ3dVdX62o88iJCcLx/I7NsG4\nCUib/8ylEb+p1MciwjV+0+6I56tgoNI75cIoA3aMaksbTM8xUZwMDPxvD0rZ51NV\nMvxnyPJm3VUSkIcLIf2UFhEWhbAX3RjmsdMX0f0arTnaPmFjG/vRm0WVNpDBz8+5\nUDWAmpspAgMBAAECggEAA2Fd6SF3WEsuaBii7K4pt+clDXefPsgJRzhmCwZxb8BK\nPAlVyY+me9JsfiM0tqT5d8PkaZnZLoYU+DNeD/N+F+1yZK4Cl/06XESFOxGe8R7F\nxJrkyt9b0clnNAHyWs2mLmms2Qc4RrQ+I7s/K13+2usmFf37gQfY4zwjtWa9OE74\ntfS+oxX2uJFmmISajvoJJx1D07EYAEHs6Xs3G5d+7+g2zAV3WU9Qb6ujtZLb9Gp0\ntxCsYIVbcDOdtRfWyfDcRj9AiZuIwS1elKcZJfYiIMYOYTM5u5RkbqwvxDhz6bGc\n0W3TbWt81RoXbHZmNQE/HT9tsVXRixJoGaxIxftGwQKBgQDo28ZgnwiV4WCa+DVt\nOuJgT+SWGSe628MLR2LhUC7y8bILDQpN23Vf6Zlg1aAgelYaZtOZ4S9bh20YlwY4\nmU9w7ZVUpvoI0zGGcGSUQZHu7AyKCIMW9z/fuKHxDV3ygx9nqmimiSNuSn2cZ6K2\npAYLhVr5a7RXXlUjgdU4qR+zcQKBgQDnL26EzVGuwv7jMCAYY6z9TdVjwqcYThhs\n1XbBAoa6f7MgU1dS0UjD2QHXpFF/p56kgjw11mJkRQGX6w2iMJNuCgyLgZiC2w/E\n3pD57zqD7Xd0Gss8m+6/7BH314exZTp4PfOsULzVYgETC9y/6SLJ58KuZDC6NHiQ\nvQll/vSXOQKBgQCQcYv78Yq01mpDlwYlLKqyDb0A8re3bIzvmSeYFlIZN542xq8G\nnsSPa2tOKxW6L8jrda96u7nRsA8Xes9MGqWxql7AdReSk9cbyupJIOdyapBYq3EN\ntO+1SmWCDsWhIn8/ofBqpZUJ3EFQ3OSNIO/zA5TsNUhYDdcIQIhQLnDQsQKBgQCI\nCV0bQEYkdBHQVe1M7LpKg5ZhkZUJtEqjICk1AeuNqr8Y8nGcBhKvS+7NmZ9rYpLz\ncr9DXtee8Qwy/NmU6siWI8ul+6hmt8jbq6vbpm3kW8PCylF1ZLxkquEX2fe65zo0\nrx/H8epsFbNUJdLMCr+x13Kzc7lImL+pS9NP9Wqv4QKBgDUInn2R1ecCWp1bIIVY\ngxi6idMiWaozReYtVXABZvb727BIrYGh3pFHxxXPgE/vVLAzb1GGEUOHi0J6a3RL\nQp+rESM/YEj3bR9gRRB46gKqXu5whcl+4mW3V3aDNmkt7eywodcsHkmzLQhW6Vo2\nasUfv7peGKSWWHz57/8eCQW8\n-----END PRIVATE KEY-----\n",
  "client_email": "myaccount@famous-tree-382223.iam.gserviceaccount.com",
  "client_id": "112693924477486376161",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/myaccount%40famous-tree-382223.iam.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('bucket_atv4') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
