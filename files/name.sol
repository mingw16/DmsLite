// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileHashStorage {
    struct FileInfo {
        bytes32 hash;
        address uploader;
        uint256 timestamp;
    }

    mapping(string => FileInfo) private fileInfos;

    event HashStored(string indexed fileName, bytes32 indexed fileHash, address indexed uploader);
    event HashDeleted(string indexed fileName, address indexed requester);

    // Zapisuje hash tylko jeśli jeszcze nie istnieje
    function storeHash(string memory fileName, bytes32 fileHash) public {
        require(fileInfos[fileName].uploader == address(0), "Hash already stored for this file");

        fileInfos[fileName] = FileInfo({
            hash: fileHash,
            uploader: msg.sender,
            timestamp: block.timestamp
        });

        emit HashStored(fileName, fileHash, msg.sender);
    }

    // Sprawdza, czy podany hash zgadza się z zapisanym
    function verifyHash(string memory fileName, bytes32 fileHash) public view returns (bool) {
        return fileInfos[fileName].hash == fileHash;
    }

    // Usuwa hash tylko jeśli wywołuje to oryginalny uploader
    function deleteHash(string memory fileName) public {
        require(fileInfos[fileName].uploader != address(0), "No hash stored for this file");
        require(msg.sender == fileInfos[fileName].uploader, "Only the uploader can delete the hash");

        delete fileInfos[fileName];
        emit HashDeleted(fileName, msg.sender);
    }

    // Opcjonalnie: pobranie danych o pliku
    function getFileInfo(string memory fileName) public view returns (bytes32, address, uint256) {
        FileInfo memory info = fileInfos[fileName];
        return (info.hash, info.uploader, info.timestamp);
    }
}