package com.example.demo.service;

import com.example.demo.model.Transaction;
import java.util.List;

public interface TransactionService {

    Transaction saveTransaction(Transaction transaction);

    List<Transaction> getAllTransactions();

    Transaction getTransactionById(Long id);

    Transaction updateTransaction(Long id, Transaction transaction);

    void deleteTransaction(Long id);
}