import boto3

from src.shared.environments import Environments


class s3_client:

    def __init__(self):
        self.__envs = Environments.get_envs()
        stage = self.__envs.stage.value
        if stage == "TEST":
            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=self.__envs.client_id,
                aws_secret_access_key=self.__envs.client_secret,
                endpoint_url=self.__envs.bucket_endpoint_url,
                region_name=self.__envs.region,
                config=boto3.session.Config(signature_version="s3v4"),
            )
        else:
            self.s3 = boto3.client("s3")

    def upload_file(self, key, file_type, decode_string):
        print(f"DEBUG upload_file - key: {key}")
        print(f"DEBUG upload_file - file_type: {file_type}")
        print(f"DEBUG upload_file - decode_string type: {type(decode_string)}")
        print(f"DEBUG upload_file - decode_string length: {len(decode_string)}")
        
        # Content type correto para Excel
        content_types = {
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
        }
        
        content_type = content_types.get(file_type, 'application/octet-stream')
        print(f"DEBUG upload_file - content_type: {content_type}")
        
        try:
            print("DEBUG upload_file - Chamando s3.put_object...")
            response = self.s3.put_object(
                Bucket=self.__envs.s3_bucket_name,
                Key=key,
                Body=decode_string,  # Este deve ser bytes
                ContentType=content_type,
            )
            print("DEBUG upload_file - put_object executado com sucesso")
            
            return {
                's3_response': response,
                'key': key
            }
            
        except Exception as e:
            print(f"DEBUG upload_file - ERRO no put_object: {str(e)}")
            print(f"DEBUG upload_file - Tipo do erro: {type(e)}")
            print(f"DEBUG upload_file - Bucket: {self.__envs.s3_bucket_name}")
            raise e

    def delete_file(self):
        pass
    def get_all_files(self):
        pass
    def get_file(self):
        pass
    def generate_presigned_url(self, expiration_time: int, object_name: str, method: str, content_type: str):
        pass


