import requests
import os

class ChibisafeWrapper:
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if exists
        self.token = None

    def login(self):
        url = f'{self.base_url}/api/auth/login'
        headers = {'Content-Type': 'application/json'}
        data = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            self.token = response.json().get('token')
            print("Login successful.")
        else:
            print(f'Failed to log in. Status code: {response.status_code}')
            print(response.text)
        return response

    def upload_file(self, file_path):
        if not self.token:
            print("Please log in first.")
            return None
        
        url = f'{self.base_url}/api/upload'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'name': os.path.basename(file_path)
        }

        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                print("File uploaded successfully.")
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
                print(response.text)
            return response

    def list_file_links(self):
        if not self.token:
            print("Please log in first.")
            return None

        url = f'{self.base_url}/api/links'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_albums(self):
        if not self.token:
            print("Please log in first.")
            return None

        url = f'{self.base_url}/api/albums'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def create_album(self, album_name):
        if not self.token:
            print("Please log in first.")
            return None

        url = f'{self.base_url}/api/album/create'
        payload = {"name": album_name}
        headers = {
            "Content-Type": "application/json",
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def get_album_id_from_name(self, album_name):
        if not self.token:
            print("Please log in first.")
            return None

        response = self.get_albums()
        albums = response['albums']
        for album in albums:
            if album['name'] == album_name:
                return album['uuid']
        return None

    def upload_file_to_album(self, file_path, album_name):
        if not self.token:
            print("Please log in first.")
            return None

        response = self.upload_file(file_path)
        uuid = response.json().get('uuid')
        album_uuid = self.get_album_id_from_name(album_name)
        return self.add_file_to_album(album_uuid, uuid)

    def get_files_list(self):
        if not self.token:
            print("Please log in first.")
            return None

        url = f'{self.base_url}/api/files'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_file_uuid_by_name(self, file_name):
        if not self.token:
            print("Please log in first.")
            return None

        response = self.get_files_list()
        files = response['files']
        for file in files:
            if file['original'] == file_name:
                return file['uuid']
        return None

    def download_file(self, file_name):
        if not self.token:
            print("Please log in first.")
            return None

        uuid = self.get_file_uuid_by_name(file_name)
        if not uuid:
            print(f"File '{file_name}' not found.")
            return None

        url = f'{self.base_url}/api/file/{uuid}/download'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        
        return response

    def add_file_to_album(self, album_uuid, file_uuid):
        if not self.token:
            print("Please log in first.")
            return None

        url = f'{self.base_url}/api/file/{file_uuid}/album/{album_uuid}'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(url, headers=headers)
        return response.json()

def main():
    # Replace with your login credentials and base URL
    username = 'admin'
    password = 'admin'
    base_url = 'http://localhost:24424'
    file_path = 'protocol-[2024.04.01-14.37.46].csv'
    album_name = 'DLC'
    file_name = os.path.basename(file_path)

    wrapper = ChibisafeWrapper(username, password, base_url)
    response = wrapper.login()

    if response and wrapper.token:
        # response = wrapper.upload_file(file_path)
        response = wrapper.list_file_links()
        response = wrapper.get_albums()
        response = wrapper.create_album(album_name)
        response = wrapper.get_album_id_from_name(album_name)
        response = wrapper.upload_file_to_album(file_path, album_name)
        response = wrapper.get_files_list()
        response = wrapper.get_file_uuid_by_name(file_name)
        response = wrapper.download_file(file_name)
    return response

if __name__ == "__main__":
    main()
