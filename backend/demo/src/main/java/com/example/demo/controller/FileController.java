package com.example.demo.controller;

import com.example.demo.model.FileEntity;
import com.example.demo.service.FileService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/files")
public class FileController {

    @Autowired
    private FileService fileService;

    // 🔹 Upload API
    @PostMapping("/upload")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file) {
        try {
            FileEntity response = fileService.uploadFile(file);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    // 🔹 Download API
    @GetMapping("/{id}")
    public ResponseEntity<Resource> getFile(@PathVariable Long id) {
        try {
            Resource file = fileService.getFile(id);

            return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .header(HttpHeaders.CONTENT_DISPOSITION,
                            "attachment; filename=\"" + file.getFilename() + "\"")
                    .body(file);

        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }
}