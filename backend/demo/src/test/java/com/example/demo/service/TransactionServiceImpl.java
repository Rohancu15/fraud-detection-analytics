package com.example.demo.service;

import com.example.demo.model.Transaction;
import com.example.demo.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TransactionServiceImpl implements TransactionService {

    @Autowired
    private TransactionRepository repository;

    // ✅ Save
    @Override
    public Transaction saveTransaction(Transaction transaction) {
        return repository.save(transaction);
    }

    // ✅ Get all
    @Override
    public List<Transaction> getAllTransactions() {
        return repository.findAll();
    }

    // ✅ Get by ID
    @Override
    public Transaction getTransactionById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Transaction not found with id: " + id));
    }

    // ✅ Update
    @Override
    public Transaction updateTransaction(Long id, Transaction transaction) {
        Transaction existing = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Transaction not found with id: " + id));

        // You can update fields here if needed
        return repository.save(transaction);
    }

    // ✅ Delete (FIXED METHOD)
    @Override
    public void deleteTransaction(Long id) {
        if (!repository.existsById(id)) {
            throw new RuntimeException("Transaction not found with id: " + id);
        }

        repository.deleteById(id);
    }
}