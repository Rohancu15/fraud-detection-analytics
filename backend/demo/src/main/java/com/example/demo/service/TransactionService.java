package com.example.demo.service;

import com.example.demo.model.Transaction;
import java.util.List;

public interface TransactionService {

    List<Transaction> getAllTransactions();

    Transaction saveTransaction(Transaction t);

    void deleteTransaction(Long id);

    Transaction processTransaction(Transaction t);
}