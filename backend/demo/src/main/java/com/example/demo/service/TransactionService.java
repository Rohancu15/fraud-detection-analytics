package com.example.demo.service;

import com.example.demo.model.Transaction;
import com.example.demo.repository.TransactionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TransactionService {

    @Autowired
    private TransactionRepository repository;

    // ✅ GET all transactions
    public List<Transaction> getAllTransactions() {
        return repository.findAll();
    }

    // ✅ PROCESS + SAVE transaction (Fraud Logic)
    public Transaction processTransaction(Transaction txn) {

        // 🔥 FRAUD RULE
        if (txn.getAmount() > 10000) {
            txn.setFlagged(true);
        } else {
            txn.setFlagged(false);
        }

        return repository.save(txn);
    }
}