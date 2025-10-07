from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import File
from django.test import override_settings
from django.http import JsonResponse
import shutil, os, uuid, json
from web3 import Web3
TEST_DIR = 'test_data'



class FileUploadTest(TestCase):


    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_upload_file(self):
        file = SimpleUploadedFile('test.txt', b'file content')
        file2 = SimpleUploadedFile('test2.pdf',b'pdf document')
        obj=File.objects.create(file=file, name=os.path.basename(file.name))
        obj2 = File.objects.create(file=file2, name=os.path.basename(file2.name))
        query = File.objects.all()
        file.seek(0)
        file2.seek(0)
        self.assertEqual(query[0].name, os.path.basename(file.name))
        self.assertEqual(query[1].name, os.path.basename(file2.name))
        self.assertEqual(query[0].file.read(), file.read())
        self.assertEqual(query[1].file.read(), file2.read())


    def tearDown(self):
        print("delete temp dir")
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print("nie udało się usunać temp files")


class FileManipulation(TestCase):

    @override_settings(MEDIA_ROOT = (TEST_DIR))
    def test_list_files(self):
        user_id = uuid.uuid4()
        user_id2 = uuid.uuid4()
        file = SimpleUploadedFile('test.txt', b'file content')
        file2 = SimpleUploadedFile('test2.pdf',b'pdf document')
        file3 = SimpleUploadedFile('test3.txt', b'test 3 file some docs sectre text')
        print("checkpoint 1")
        obj=File.objects.create(file=file, name=os.path.basename(file.name), owner_id= user_id)
        obj2 = File.objects.create(file=file2, name=os.path.basename(file2.name), owner_id = user_id)
        obj3 = File.objects.create(file=file3, name=os.path.basename(file3.name), owner_id=user_id2)
        print("checkpoint2")
        client1 = self.client.get('/file/owner/'+ str(user_id))
        client2 = self.client.get('/file/owner/'+ str(user_id2))
        print('checkpoint3')
        print(client1.json())
        print(client2.json())
        self.assertEqual(client1.json()['names'], ['test.txt', 'test2.pdf'])
        self.assertEqual(client2.json()['names'], ['test3.txt'])

    @override_settings(MEDIA_ROOT = (TEST_DIR))
    def test_list_files_by_group(self):
        user_id = uuid.uuid4()
        user_id2 = uuid.uuid4()
        group_id = uuid.uuid4()
        group_id2 = uuid.uuid4()
        file = SimpleUploadedFile('test.txt', b'file content')
        file2 = SimpleUploadedFile('test2.pdf',b'pdf document')
        file3 = SimpleUploadedFile('test3.txt', b'test 3 file some docs sectre text')
        print("checkpoint 1")
        obj=File.objects.create(file=file, name=os.path.basename(file.name), owner_id= user_id,group_id=group_id)
        obj2 = File.objects.create(file=file2, name=os.path.basename(file2.name), owner_id = user_id, group_id=group_id2)
        obj3 = File.objects.create(file=file3, name=os.path.basename(file3.name), owner_id=user_id2, group_id=group_id)
        print("checkpoint2")
        client1 = self.client.get('/file/group/'+ str(group_id))
        client2 = self.client.get('/file/group/'+ str(group_id2))
        print('checkpoint3')
        print(client1.json())
        print(client2.json())
        self.assertEqual(client1.json()['names'], ['test.txt', 'test3.txt'])
        self.assertEqual(client2.json()['names'], ['test2.pdf'])

    @override_settings(MEDIA_ROOT = (TEST_DIR))
    def get_file(self):
        user_id = uuid.uuid4()
        user_id2 = uuid.uuid4()
        file = SimpleUploadedFile('test.txt', b'file content')
        file2 = SimpleUploadedFile('test2.pdf',b'pdf document')
        file3 = SimpleUploadedFile('test3.txt', b'test 3 file some docs sectre text')
        print("checkpoint 1")
        obj=File.objects.create(file=file, name=os.path.basename(file.name), owner_id= user_id)
        obj2 = File.objects.create(file=file2, name=os.path.basename(file2.name), owner_id = user_id)
        obj3 = File.objects.create(file=file3, name=os.path.basename(file3.name), owner_id=user_id2)
        print("checkpoint2")
        client1 = self.client.get('/file/'+ str(obj.id))
        client2 = self.client.get('/file/'+ str(obj2.id))
        print('checkpoint3')
        print(client1.json())
        print(client2.json())
        self.assertEqual(client1.json()['names'], ['test.txt', 'test2.pdf'])
        self.assertEqual(client2.json()['names'], ['test3.txt'])

    @override_settings(MEDIA_ROOT = (TEST_DIR))
    def send_file(self):

        # Try to send files 1 2 3 4 5 6 7 8 9 10 from 3 diffrent users and 2 different groups
        
        f = SimpleUploadedFile('1.txt', b'some file content')
        f2 = SimpleUploadedFile('2.pdf', b'some pdf file content')
        f3 = SimpleUploadedFile('3.pdf', b'some pdf file content')
        f4 = SimpleUploadedFile('4.pdf', b'some pdf file content')
        f5 = SimpleUploadedFile('5.pdf', b'some pdf file content')
        f6 = SimpleUploadedFile('6.pdf', b'some pdf file content')
        f7 = SimpleUploadedFile('7.pdf', b'some pdf file content')
        f8 = SimpleUploadedFile('8.pdf', b'some pdf file content')
        f9 = SimpleUploadedFile('9.pdf', b'some pdf file content')
        f10 = SimpleUploadedFile('10.pdf', b'some pdf file content')
        
        user_id = uuid.uuid4()
        user_id2 = uuid.uuid4()
        user_id3 = uuid.uuid4()

        group_id = uuid.uuid4()
        group_id2 = uuid.uuid4()

        send = self.client.post('/file/', {'file':f,'owner_id':user_id,'group_id':group_id2})

        send = self.client.post('/file/', {'file':f2,'owner_id':user_id,'group_id':group_id})

        send = self.client.post('/file/', {'file':f3,'owner_id':user_id,'group_id':group_id})

        send = self.client.post('/file/', {'file':f4,'owner_id':user_id2,'group_id':group_id2})

        send = self.client.post('/file/', {'file':f5,'owner_id':user_id2,'group_id':group_id})

        send = self.client.post('/file/', {'file':f6,'owner_id':user_id2,'group_id':group_id})

        send = self.client.post('/file/', {'file':f7,'owner_id':user_id3,'group_id':group_id2})

        send = self.client.post('/file/', {'file':f8,'owner_id':user_id3,'group_id':group_id})

        send = self.client.post('/file/', {'file':f9,'owner_id':user_id3,'group_id':group_id})

        send = self.client.post('/file/', {'file':f10,'owner_id':user_id3,'group_id':group_id2})

        self.assertEqual(send.status_code, 200)
        response = self.client.get('/file/owner/'+str(user_id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['names'], ['1.txt', '2.pdf', '3.pdf'])

        response = self.client.get('/file/owner/'+str(user_id2))
        data = json.loads(response.content)
        self.assertEqual(data['names'], ['4.pdf', '5.pdf', '6.pdf'])

        response = self.client.get('/file/owner/'+ str(user_id3))
        data = json.loads(response.content)
        self.assertEqual(data['names'], ['7.pdf', '8.pdf', '9.pdf', '10.pdf'])

        response = self.client.get('/file/group/'+str(group_id))
        data = json.loads(response.content)
        self.assertEqual(data['names'], ['2.pdf', '3.pdf', '5.pdf', '6.pdf', '8.pdf', '9.pdf'])

        response = self.client.get('/file/group/'+str(group_id2))
        data = json.loads(response.content)
        self.assertEqual(data['names'], ['1.txt', '4.pdf', '7.pdf', '10.pdf'])


    def tearDown(self):
        print("clean up")
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print("can not delete temp files")


    
class GanacheConnTest(TestCase):

    def ganacheConn(self):
    # Importy
        from web3 import Web3
        from solcx import compile_source, install_solc, set_solc_version
        import hashlib
        import os

        # 1. Instalacja i konfiguracja kompilatora Solidity
        install_solc('0.8.0')
        set_solc_version('0.8.0')

        # 2. Kod źródłowy kontraktu
        contract_source_code = """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.0;

        contract FileHashStorage {
            mapping(string => bytes32) private fileHashes;
            event HashStored(string indexed fileName, bytes32 fileHash);

            function storeHash(string memory fileName, bytes32 fileHash) public {
                fileHashes[fileName] = fileHash;
                emit HashStored(fileName, fileHash);
            }

            function getHash(string memory fileName) public view returns (bytes32) {
                return fileHashes[fileName];
            }
        }
        """

        # 3. Kompilacja kontraktu
        compiled_sol = compile_source(contract_source_code, output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_sol.popitem()
        bytecode = contract_interface['bin']
        abi = contract_interface['abi']

        # 4. Połączenie z Ganache
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        assert w3.is_connected(), "Brak połączenia z blockchainem"
        w3.eth.default_account = w3.eth.accounts[0]

        # 5. Wdrożenie kontraktu
        FileHashStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = FileHashStorage.constructor().transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # 6. Utworzenie instancji kontraktu
        file_hash_storage = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        # 7. Utworzenie i hashowanie pliku testowego
        test_file = "test_file.txt"
        with open(test_file, "w") as f:
            f.write("To jest testowa zawartość pliku.")
        
        def calculate_file_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.digest()

        file_hash = calculate_file_hash(test_file)
        bytes32_hash = Web3.keccak(file_hash)  # Zwraca bytes
        
        # 8. Konwersja do hex tylko dla wyświetlenia
        hex_hash = Web3.to_hex(bytes32_hash)
        print(f"Hash pliku (hex): {hex_hash}")
        
        # 9. Zapis hasha na blockchainie (w formie bytes)
        tx_hash = file_hash_storage.functions.storeHash(test_file, bytes32_hash).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # 10. Odczyt hasha z blockchainu
        stored_hash = file_hash_storage.functions.getHash(test_file).call()
        print(f"Hash z blockchainu (bytes): {stored_hash}")
        print(f"Hash z blockchainu (hex): {Web3.to_hex(stored_hash)}")
        
        # 11. Weryfikacja (porównanie w formie bytes)
        assert stored_hash == bytes32_hash, "Hashes nie są identyczne!"
        
        # 12. Sprzątanie
        os.remove(test_file)
        print("Test zakończony pomyślnie!")




    def addHashTest(self):
         
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))


        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Oblicz hash pliku
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = Web3.keccak(sha256_hash.digest())  # Zwraca bytes32
        
        # Zapisz hash w kontrakcie
        tx_hash = contract.functions.storeHash(os.path.basename(file_path), file_hash).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Dodano hash pliku {file_path} do blockchainu!")



