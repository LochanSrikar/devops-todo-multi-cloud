package com.example.user;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;  // Add this import

@Entity

@Table(name = "users")  // Rename table to "users" to avoid reserved word
public class User {
    @Id
    private Long id;
    private String name;
    private String token;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }
}