package com.example.demo.service;

import com.example.demo.model.FileEntity;
import com.example.demo.repository.FileRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.*;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.*;
import java.util.*;

@Service
public class FileService {

    private final String uploadDir = "uploads/";

    @Autowired
    private FileRepository fileRepository;

    // 🔹 Upload
    public FileEntity uploadFile(MultipartFile file) throws IOException {

        // Validate size (<10MB)
        if (file.getSize() > 10 * 1024 * 1024) {
            throw new RuntimeException("File size exceeds 10MB");
        }

        // Validate type
        List<String> allowedTypes = Arrays.asList(
                "image/png",
                "image/jpeg",
                "application/pdf"
        );

        if (!allowedTypes.contains(file.getContentType())) {
            throw new RuntimeException("Invalid file type");
        }

        // Create folder if not exists
        Path uploadPath = Paths.get(uploadDir);
        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }

        // Generate UUID name
        String storedName = UUID.randomUUID() + "_" + file.getOriginalFilename();

        // Save file
        Path filePath = uploadPath.resolve(storedName);
        Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);

        // Save metadata in DB
        FileEntity entity = new FileEntity();
        entity.setOriginalName(file.getOriginalFilename());
        entity.setStoredName(storedName);
        entity.setFileType(file.getContentType());
        entity.setSize(file.getSize());

        return fileRepository.save(entity);
    }

    // 🔹 Download
    public Resource getFile(Long id) throws IOException {

        FileEntity entity = fileRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("File not found"));

        Path path = Paths.get(uploadDir + entity.getStoredName());
        Resource resource = new UrlResource(path.toUri());

        if (!resource.exists()) {
            throw new RuntimeException("File not found");
        }

        return resource;
    }
}