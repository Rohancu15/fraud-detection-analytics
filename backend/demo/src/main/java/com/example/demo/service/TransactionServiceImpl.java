package com.example.demo.service;

import com.example.demo.model.Transaction;
import com.example.demo.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TransactionServiceImpl implements TransactionService {

    @Autowired
    private TransactionRepository transactionRepository;

    @Override
    @Cacheable(value = "transactions")
    public List<Transaction> getAllTransactions() {
        return transactionRepository.findAll();
    }

    @Override
    @CacheEvict(value = "transactions", allEntries = true)
    public Transaction saveTransaction(Transaction t) {
        return transactionRepository.save(t);
    }

    @Override
    @CacheEvict(value = "transactions", allEntries = true)
    public void deleteTransaction(Long id) {
        transactionRepository.deleteById(id);
    }

    @Override
    public Transaction processTransaction(Transaction t) {
        if (t.getAmount() > 10000) {
            t.setFlagged(true);
        } else {
            t.setFlagged(false);
        }
        return transactionRepository.save(t);
    }
}