import httpx
from typing import Dict, Any, List

class NutanixBackupClientSDK:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        self._authenticate()

    def _authenticate(self):
        url = f"{self.base_url}/token"
        data = {"username": self.username, "password": self.password}
        response = httpx.post(url, data=data)
        response.raise_for_status()
        self.token = response.json().get("access_token")

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def list_users(self, admin_user: str, admin_password: str) -> List[str]:
        url = f"{self.base_url}/admin/list_users/"
        params = {"admin_user": admin_user, "admin_password": admin_password}
        response = httpx.post(url, params=params)
        response.raise_for_status()
        return response.json().get("users")

    def add_user(self, admin_user: str, admin_password: str, username: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/admin/add_user/"
        params = {
            "admin_user": admin_user,
            "admin_password": admin_password,
            "username": username,
            "password": password
        }
        response = httpx.post(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def delete_user(self, admin_user: str, admin_password: str, username: str) -> Dict[str, Any]:
        url = f"{self.base_url}/admin/delete_user/"
        params = {"admin_user": admin_user, "admin_password": admin_password, "username": username}
        response = httpx.post(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def reset_user_sessions(self, admin_user: str, admin_password: str, username: str) -> Dict[str, Any]:
        url = f"{self.base_url}/admin/reset_user_sessions/"
        params = {"admin_user": admin_user, "admin_password": admin_password, "username": username}
        response = httpx.post(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def get_db_collections_docs(self, db_name: str, collection_name: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/admin/get_db_collections_docs"
        params = {"db_name": db_name, "collection_name": collection_name}
        response = httpx.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def add_session(self) -> Dict[str, Any]:
        url = f"{self.base_url}/add_session"
        response = httpx.post(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def list_sessions(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/list_sessions"
        response = httpx.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def switch_session(self, session_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/switch_session"
        params = {"session_id": session_id}
        response = httpx.post(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def get_current_session_details(self) -> Dict[str, Any]:
        url = f"{self.base_url}/get_current_session_details"
        response = httpx.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def health_check(self) -> str:
        url = f"{self.base_url}/health"
        response = httpx.get(url)
        response.raise_for_status()
        return response.text

    def add_cluster(self, add_cluster_obj: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/add_cluster"
        response = httpx.post(url, headers=self._get_headers(), json=add_cluster_obj)
        response.raise_for_status()
        return response.json()

    def discover(self) -> Dict[str, Any]:
        url = f"{self.base_url}/discover"
        response = httpx.post(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def add_target(self, target_point: str, diskSizeGB: int) -> Dict[str, Any]:
        url = f"{self.base_url}/add_target"
        data = {"target_point": target_point, "diskSizeGB": diskSizeGB}
        response = httpx.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        return response.json()

    def backup(self, backupspec: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/backup"
        response = httpx.post(url, headers=self._get_headers(), json=backupspec)
        response.raise_for_status()
        return response.json()

    def create_backup_schedule(self, spec: Dict[str, Any]) -> str:
        url = f"{self.base_url}/create_backup_schedule"
        response = httpx.post(url, headers=self._get_headers(), json=spec)
        response.raise_for_status()
        return response.text

    def delete_backup_schedule(self, backup_schedule_pid: int) -> Dict[str, Any]:
        url = f"{self.base_url}/delete_backup_schedule"
        data = {"backup_schedule_pid": backup_schedule_pid}
        response = httpx.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        return response.json()

    def get_backup_info(self, get_backup_spec: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/get_backup_info"
        response = httpx.post(url, headers=self._get_headers(), json=get_backup_spec)
        response.raise_for_status()
        return response.json()

# Usage example:
sdk = NutanixBackupClientSDK(base_url="http://localhost:8082", username="anirudh", password="anirudh123")

users = sdk.list_users(admin_user="admin", admin_password="Nutanix.123")
print(users)

health_resp = sdk.health_check()
print(health_resp)

sessions = sdk.list_sessions()
print(sessions)

add_cluster_obj = {
  "cluster_pc_ip": "10.96.32.74",
  "cluster_pe_ip": "10.96.5.70",
  "cluster_user": "admin",
  "cluster_password": "Nutanix.123",
  "ssh_user": "nutanix",
  "ssh_password": "RDMCluster.123",
  "proxy_vm_extId": "ae770545-c610-4bd3-bdaa-d10a81dd4d47",
  "proxy_vm_ip": "10.96.44.135",
  "proxy_vm_user": "root",
  "proxy_vm_password": "nutanix/4u"
}

session_add = sdk.add_session()
print(session_add)

cluster_resp = sdk.add_cluster(add_cluster_obj)
print(cluster_resp)

current_session = sdk.get_current_session_details()
print(current_session)