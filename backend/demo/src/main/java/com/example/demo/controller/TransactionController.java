package com.example.demo.controller;

import com.example.demo.model.Transaction;
import com.example.demo.service.TransactionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/transactions")
public class TransactionController {

    @Autowired
    private TransactionService service;

    // ✅ GET all transactions
    @GetMapping
    public List<Transaction> getAll() {
        return service.getAllTransactions();
    }

    // ✅ POST create transaction
    @PostMapping
    public Transaction create(@RequestBody Transaction txn) {
        return service.processTransaction(txn);
    }
}