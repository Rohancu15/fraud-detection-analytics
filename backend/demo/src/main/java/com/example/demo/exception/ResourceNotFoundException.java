package com.example.demo.exception;

// Custom Exception for handling resource not found cases
public class ResourceNotFoundException extends RuntimeException {

    // Default Constructor
    public ResourceNotFoundException() {
        super("Resource not found");
    }

    // Constructor with custom message
    public ResourceNotFoundException(String message) {
        super(message);
    }

    // Constructor with message and cause
    public ResourceNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}