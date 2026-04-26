package com.example.demo.model;

import jakarta.persistence.*;

@Entity
public class Transaction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private double amount;
    private boolean flagged;

    public Long getId() { return id; }

    public double getAmount() { return amount; }

    public void setAmount(double amount) { this.amount = amount; }

    public boolean isFlagged() { return flagged; }

    public void setFlagged(boolean flagged) { this.flagged = flagged; }
}